"""Pruebas directas de capa CRUD con sesión real."""

from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.crud import mantenimiento as cm
from app.crud import unidad as cu
from app.models.enums import EstadoUnidad
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate
from app.schemas.unidad import UnidadCreate, UnidadUpdate


@pytest.mark.asyncio
async def test_crud_unidad_flujo(session):
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="CR-1",
            placas="CR-PL1",
            marca="M",
            modelo="Mo",
            anio=2020,
            tipo_vehiculo="Van",
            kilometraje_actual=100,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    got = await cu.obtener_unidad_por_id(session, u.id)
    assert got is not None

    lst = await cu.listar_unidades(session)
    assert len(lst) >= 1

    upd = await cu.actualizar_unidad(
        session,
        u.id,
        UnidadUpdate(placas="CR-PL2"),
    )
    await session.commit()
    assert upd is not None and upd.placas == "CR-PL2"

    km = await cu.actualizar_kilometraje(session, u.id, 500)
    await session.commit()
    assert km is not None and km.kilometraje_actual == 500


@pytest.mark.asyncio
async def test_crud_unidad_duplicado(session):
    await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="D1",
            placas="P1",
            marca="M",
            modelo="M",
            anio=2021,
            tipo_vehiculo="T",
            kilometraje_actual=0,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    with pytest.raises(ValueError):
        await cu.crear_unidad(
            session,
            UnidadCreate(
                numero_economico="D1",
                placas="P2",
                marca="M",
                modelo="M",
                anio=2021,
                tipo_vehiculo="T",
                kilometraje_actual=0,
                estado=EstadoUnidad.activa,
            ),
        )


@pytest.mark.asyncio
async def test_listar_mantenimientos_global_limite(session):
    """Tapa límite superior interno (500) en listado global."""
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="GLIM",
            placas="GL-P",
            marca="M",
            modelo="M",
            anio=2022,
            tipo_vehiculo="T",
            kilometraje_actual=1,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    await cm.crear_mantenimiento(
        session,
        u.id,
        MantenimientoCreate(
            tipo="T",
            fecha_servicio="2026-01-01",
            kilometraje=1,
            costo=1,
            proveedor="P",
            responsable="R",
        ),
    )
    await session.commit()
    rows = await cm.listar_mantenimientos_global(session, limit=9_999)
    assert len(rows) >= 1


@pytest.mark.asyncio
async def test_crud_mantenimiento(session):
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="MANT",
            placas="MN-01",
            marca="M",
            modelo="M",
            anio=2022,
            tipo_vehiculo="T",
            kilometraje_actual=1,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    m = await cm.crear_mantenimiento(
        session,
        u.id,
        MantenimientoCreate(
            tipo="A",
            fecha_servicio="2026-01-01",
            kilometraje=2,
            costo=10,
            proveedor="P",
            observaciones=None,
            responsable="R",
        ),
    )
    await session.commit()

    hist = await cm.listar_mantenimientos_por_unidad(session, u.id)
    assert len(hist) == 1

    mo = await cm.actualizar_mantenimiento(
        session,
        m.id,
        MantenimientoUpdate(observaciones="OK"),
    )
    await session.commit()
    assert mo is not None and mo.observaciones == "OK"

    assert await cm.eliminar_mantenimiento(session, m.id) is True
    await session.commit()


@pytest.mark.asyncio
async def test_crud_no_existe(session):
    assert await cu.obtener_unidad_por_id(session, 999999) is None
    assert await cu.eliminar_unidad(session, 999999) is False
    assert await cm.obtener_mantenimiento(session, 999999) is None
    assert await cm.eliminar_mantenimiento(session, 999999) is False


@pytest.mark.asyncio
async def test_actualizar_unidad_no_existe(session):
    assert (
        await cu.actualizar_unidad(session, 999999, UnidadUpdate(placas="ZZZ"))
        is None
    )


@pytest.mark.asyncio
async def test_actualizar_unidad_duplicado_integrity(session):
    await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="U-DUP-A",
            placas="PP-A",
            marca="M",
            modelo="M",
            anio=2021,
            tipo_vehiculo="T",
            kilometraje_actual=0,
            estado=EstadoUnidad.activa,
        ),
    )
    u2 = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="U-DUP-B",
            placas="PP-B",
            marca="M",
            modelo="M",
            anio=2021,
            tipo_vehiculo="T",
            kilometraje_actual=0,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    with pytest.raises(ValueError, match="duplicados"):
        await cu.actualizar_unidad(session, u2.id, UnidadUpdate(placas="PP-A"))
    await session.rollback()


@pytest.mark.asyncio
async def test_actualizar_unidad_salta_explicit_none(session):
    """Rama ``if valor is None: continue`` en ``actualizar_unidad``."""
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="SKIP-N",
            placas="SKIP-P",
            marca="Original",
            modelo="Mo",
            anio=2021,
            tipo_vehiculo="T",
            kilometraje_actual=10,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    upd = await cu.actualizar_unidad(
        session,
        u.id,
        UnidadUpdate.model_validate({"marca": None, "modelo": "  Nuevo  "}),
    )
    await session.commit()
    assert upd is not None
    assert upd.marca == "Original"
    assert upd.modelo == "Nuevo"


@pytest.mark.asyncio
async def test_actualizar_unidad_ramas_strip_y_estado(session):
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="STRIP-1",
            placas="ST-PL",
            marca="Marca",
            modelo="Mo",
            anio=2020,
            tipo_vehiculo="Tipo",
            kilometraje_actual=100,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    upd = await cu.actualizar_unidad(
        session,
        u.id,
        UnidadUpdate(
            numero_economico="  NE-X  ",
            placas="  PL-Y  ",
            marca="  M  ",
            modelo="  MODEL  ",
            tipo_vehiculo="  CAM  ",
            estado=EstadoUnidad.taller,
        ),
    )
    await session.commit()
    assert upd is not None
    assert upd.numero_economico == "NE-X"
    assert upd.placas == "PL-Y"
    assert upd.marca == "M"
    assert upd.estado == EstadoUnidad.taller


@pytest.mark.asyncio
async def test_eliminar_unidad_ok(session):
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="DEL-U",
            placas="DEL-P",
            marca="M",
            modelo="M",
            anio=2020,
            tipo_vehiculo="T",
            kilometraje_actual=1,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    assert await cu.eliminar_unidad(session, u.id) is True
    await session.commit()


@pytest.mark.asyncio
async def test_actualizar_kilometraje_no_unidad(session):
    assert await cu.actualizar_kilometraje(session, 888888001, 100) is None


@pytest.mark.asyncio
async def test_actualizar_kilometraje_invalido_crud(session):
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="KM-X",
            placas="KM-P",
            marca="M",
            modelo="M",
            anio=2021,
            tipo_vehiculo="T",
            kilometraje_actual=500,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    with pytest.raises(ValueError, match="kilometraje"):
        await cu.actualizar_kilometraje(session, u.id, 100)


@pytest.mark.asyncio
async def test_crear_mantenimiento_sin_unidad(session):
    with pytest.raises(ValueError, match="no existe"):
        await cm.crear_mantenimiento(
            session,
            777777701,
            MantenimientoCreate(
                tipo="T",
                fecha_servicio="2026-01-01",
                kilometraje=1,
                costo=1,
                proveedor="P",
                responsable="R",
            ),
        )


@pytest.mark.asyncio
async def test_crear_mantenimiento_integrity_error(session, monkeypatch):
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="INT-M",
            placas="INT-P",
            marca="M",
            modelo="M",
            anio=2022,
            tipo_vehiculo="T",
            kilometraje_actual=10,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()

    async def boom_flush():
        raise IntegrityError(None, None, Exception("dup"))

    monkeypatch.setattr(session, "flush", boom_flush)

    with pytest.raises(ValueError, match="No se pudo registrar"):
        await cm.crear_mantenimiento(
            session,
            u.id,
            MantenimientoCreate(
                tipo="T",
                fecha_servicio="2026-02-02",
                kilometraje=11,
                costo=2,
                proveedor="Pr",
                responsable="Rp",
            ),
        )


@pytest.mark.asyncio
async def test_actualizar_mantenimiento_no_existe(session):
    assert (
        await cm.actualizar_mantenimiento(
            session,
            88888002,
            MantenimientoUpdate(tipo="Z"),
        )
        is None
    )


@pytest.mark.asyncio
async def test_actualizar_mantenimiento_campos_varios(session):
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="AM-U",
            placas="AM-P",
            marca="M",
            modelo="M",
            anio=2023,
            tipo_vehiculo="T",
            kilometraje_actual=20,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    m = await cm.crear_mantenimiento(
        session,
        u.id,
        MantenimientoCreate(
            tipo="Tipo",
            fecha_servicio="2026-03-03",
            kilometraje=25,
            costo=99.5,
            proveedor="Prov",
            observaciones="algo",
            responsable="Resp",
        ),
    )
    await session.commit()

    md = await cm.actualizar_mantenimiento(
        session,
        m.id,
        MantenimientoUpdate(
            tipo="  Nuevo tipo  ",
            fecha_servicio="04/04/2026",
            kilometraje=400,
            costo=120.0,
            proveedor="  Otra prov  ",
            observaciones="   ",
            responsable="  Otro  ",
        ),
    )
    await session.commit()
    assert md is not None
    assert md.tipo == "Nuevo tipo"
    assert md.kilometraje == 400
    assert md.observaciones is None
    assert md.proveedor == "Otra prov"

    md2 = await cm.actualizar_mantenimiento(
        session,
        m.id,
        MantenimientoUpdate(observaciones="  txt  "),
    )
    await session.commit()
    assert md2 is not None and md2.observaciones == "txt"


@pytest.mark.asyncio
async def test_actualizar_observaciones_valor_no_str(session):
    """Rama ``else`` interna cuando ``observaciones`` no es ``str`` (dump sin validar tipo)."""
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="OBS-U",
            placas="OBS-P",
            marca="M",
            modelo="M",
            anio=2025,
            tipo_vehiculo="T",
            kilometraje_actual=5,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    m = await cm.crear_mantenimiento(
        session,
        u.id,
        MantenimientoCreate(
            tipo="t",
            fecha_servicio="2026-06-06",
            kilometraje=6,
            costo=1,
            proveedor="p",
            responsable="r",
        ),
    )
    await session.commit()
    fake_upd = MagicMock(spec=MantenimientoUpdate)
    fake_upd.model_dump = MagicMock(return_value={"observaciones": 42})
    md = await cm.actualizar_mantenimiento(session, m.id, fake_upd)
    await session.commit()
    assert md is not None
    assert md.observaciones == 42


@pytest.mark.asyncio
async def test_actualizar_mantenimiento_tipo_none_explicito(session):
    """Rama ``continue`` cuando el valor del campo es ``None`` en el dump."""
    u = await cu.crear_unidad(
        session,
        UnidadCreate(
            numero_economico="TN-U",
            placas="TN-P",
            marca="M",
            modelo="M",
            anio=2024,
            tipo_vehiculo="T",
            kilometraje_actual=1,
            estado=EstadoUnidad.activa,
        ),
    )
    await session.commit()
    m = await cm.crear_mantenimiento(
        session,
        u.id,
        MantenimientoCreate(
            tipo="T0",
            fecha_servicio="2026-05-05",
            kilometraje=2,
            costo=3,
            proveedor="P",
            responsable="R",
        ),
    )
    await session.commit()

    upd = MantenimientoUpdate.model_construct(tipo=None)
    assert await cm.actualizar_mantenimiento(session, m.id, upd) is not None
    await session.commit()
