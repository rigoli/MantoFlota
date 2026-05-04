# Manual técnico — MantoFlota

## Arquitectura

- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, componentes UI (shadcn/Base UI), TanStack Query, react-hook-form, Zod.
- **Backend:** FastAPI, Pydantic v2, SQLAlchemy 2 async (`asyncmy`), JWT para autenticación.
- **Base de datos:** MySQL (desarrollo típico: MAMP en `localhost:8889`).
- **Migraciones:** Alembic (motor síncrono `pymysql`).

El prefijo de la API es **`/api/v1`**.

## Estructura de carpetas (resumen)

| Ruta | Contenido |
|------|-----------|
| `backend/app/api/v1/routers/` | Routers FastAPI (auth, dashboard, export, unidades, mantenimientos). |
| `backend/app/crud/` | Lógica de acceso a datos. |
| `backend/app/models/` | Modelos SQLAlchemy. |
| `backend/app/schemas/` | Esquemas Pydantic (entrada/salida). |
| `backend/app/validators.py` | Funciones de validación reutilizables. |
| `backend/tests/` | Pruebas pytest. |
| `frontend/app/` | Rutas y layouts Next.js. |
| `frontend/lib/` | Cliente API, auth, esquemas Zod, tipos. |
| `frontend/components/` | Componentes reutilizables. |

## Variables de entorno (backend)

Copiar desde `.env.example`. Las esenciales:

- `DATABASE_URL_ASYNC` — conexión async a MySQL.
- `DATABASE_URL_SYNC` — conexión síncrona (Alembic).
- `JWT_SECRET_KEY` — secreto para firmar tokens.
- `CORS_ORIGINS` — orígenes permitidos (p. ej. `http://localhost:3000`).

## Variables de entorno (frontend)

- `NEXT_PUBLIC_API_URL` — URL base del API (p. ej. `http://localhost:8000`).

## Instalación y arranque


**Bases de datos y migraciones:**

```bash
cd backend && uv run python scripts/ensure_db.py
cd backend && uv run alembic upgrade head
```

O desde la raíz: `make migrate`.

**Seed de usuarios demo:**

```bash
make seed
```

**Backend:**

```bash
cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**

```bash
cd frontend && pnpm install && pnpm dev
```

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/auth/login` | Login (JSON: email, password). |
| GET | `/api/v1/auth/me` | Usuario autenticado. |
| GET | `/api/v1/dashboard/inicio` | Próximos sugeridos y unidades en taller. |
| GET | `/api/v1/export/unidades` | Exportación JSON de todas las unidades (lista `UnidadRead`). |
| GET | `/api/v1/export/unidades/csv` | Mismo contenido en CSV (UTF-8 con BOM). |
| GET | `/api/v1/export/mantenimientos` | Historial global en JSON (`limit` 1–500, default 500). |
| GET | `/api/v1/export/mantenimientos/csv` | Historial global en CSV (mismo `limit`). |
| GET/POST | `/api/v1/unidades` | Listar / crear unidad. |
| GET/PATCH/DELETE | `/api/v1/unidades/{id}` | Detalle / actualizar / eliminar (DELETE: rol administrador). |
| PATCH | `/api/v1/unidades/{id}/kilometraje` | Solo kilometraje. |
| GET/POST | `/api/v1/unidades/{id}/mantenimientos` | Historial / alta de mantenimiento. |
| GET | `/api/v1/mantenimientos` | Listado global (query `limit`). |
| GET/PATCH/DELETE | `/api/v1/mantenimientos/{id}` | Detalle / actualizar / eliminar. |

Los endpoints protegidos requieren cabecera `Authorization: Bearer <token>`.

## Modelo de datos (resumen)

- **unidades:** id, número económico, placas, marca, modelo, año, tipo_vehiculo, kilometraje_actual, estado (`activa` \| `taller` \| `baja`), timestamps.
- **mantenimientos:** id, unidad_id (FK en cascada), tipo, fecha_servicio, kilometraje, costo, proveedor, observaciones, responsable, timestamps.
- **usuarios:** gestión de acceso (ver modelos y seed).

## Heurística del dashboard

Definida en `app/crud/dashboard.py`: a partir del último mantenimiento por fecha (o fecha de alta si no hay historial), se calculan **próxima fecha estimada** (+90 días) y **próximo kilometraje estimado** (+10 000 km). No hay motor de “vencido/crítico” ni “lo primero que ocurra”.

## Pruebas

```bash
make test-backend
```

```bash
cd frontend && pnpm test && pnpm lint && pnpm typecheck
```

Cobertura backend: 100 % sobre el paquete `app` (excluye routers HTTP y algunos módulos de wiring según `pyproject.toml`).

## Evidencia E3

Ver [`docs/evidencia/README.md`](evidencia/README.md) y archivos de salida en la misma carpeta.
