# MantoFlota — Etapa 2 (Fullstack)

Aplicación para **gestionar el mantenimiento preventivo** de una flotilla interna: unidades, historial de servicios y estado operativo.

**Stack de desarrollo:** API **FastAPI** + **MySQL** (MAMP en local) + interfaz **Next.js** (shadcn/ui).

## Requisitos

- Python **3.10+** (recomendado 3.12)
- **MAMP** con MySQL en **`localhost:8889`**, usuario/contraseña por defecto `root` / `root`
- **Node.js** + **pnpm**
- Bases `mantoflota` y `mantoflota_test` (se crean con el script `ensure_db`)

## Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
python scripts/ensure_db.py
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000` · OpenAPI: `/docs`
- Tests: `pytest -W error --cov=app --cov-fail-under=100`
- Credenciales y datos demo: ver `backend/README.md` y ejecutar `make seed` tras migrar.

## Frontend

```bash
cd frontend
pnpm install
cp .env.local.example .env.local
pnpm dev
```

- UI: `http://localhost:3000`
- Variable `NEXT_PUBLIC_API_URL` apunta al backend (por defecto `http://localhost:8000`).

## Comandos raíz

| Comando          | Descripción                                      |
|------------------|--------------------------------------------------|
| `make backend-install` | Crea venv e instala backend                |
| `make frontend-install`| `pnpm install` en frontend                 |
| `make migrate`   | Crea DBs + `alembic upgrade head`                |
| `make seed`      | Usuarios demo + vehículos/mantenimientos de prueba (`backend/scripts/seed_users.py`) |
| `make test`      | Pytest (backend) + vitest/lint/tsc (frontend)   |
| `make check`     | `make test` + build Next + Playwright e2e        |
| `make dev`       | Instrucciones para levantar API + UI             |

## Documentación

- Entrega académica Etapa 2: [docs/ETAPA2.md](docs/ETAPA2.md)

## Nombre del proyecto

Usar **MantoFlota** de forma consistente en portada y contenido (evitar “MantoCar”).
