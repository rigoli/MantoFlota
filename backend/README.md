# MantoFlota — Backend

Servicio REST para gestión de unidades y mantenimientos preventivos. En desarrollo local se usa MySQL en MAMP (`localhost:8889`).

## Setup

```bash
cp .env.example .env
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python scripts/ensure_db.py
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

## Datos de desarrollo (`make seed`)

Script: `scripts/seed_users.py` (usuarios + **unidades y mantenimientos demo**).

### Usuarios

| Correo | Contraseña | Rol |
|--------|------------|-----|
| `admin@manto.local` | `Admin123!` | administrador |
| `operador@manto.local` | `Operador123!` | operador |
| `consulta@manto.local` | `Consulta123!` | consulta |

### Flota demo (tras el seed)

- **DEMO-ECO-01** — Toyota Hiace (activa), con 2 mantenimientos de ejemplo.
- **DEMO-ECO-02** — Ford Transit (activa), con 2 mantenimientos.
- **DEMO-ECO-03** — Mercedes Sprinter (en taller), con 1 mantenimiento.

Si una unidad ya tiene historial, el seed **no duplica** mantenimientos (idempotente).

## Tests

Requiere MySQL activo en el puerto **8889**.

```bash
pytest -W error --cov=app --cov-fail-under=100
```
