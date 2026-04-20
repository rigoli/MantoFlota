.PHONY: migrate test check dev seed backend-install frontend-install

backend-install:
	cd backend && python3 -m venv .venv && ./.venv/bin/pip install -e ".[dev]"

frontend-install:
	cd frontend && pnpm install

migrate:
	cd backend && ./.venv/bin/python scripts/ensure_db.py && ./.venv/bin/alembic upgrade head

test-backend:
	cd backend && ./.venv/bin/pytest -W error --cov=app --cov-fail-under=100 -q

test-frontend:
	cd frontend && pnpm test && pnpm lint && pnpm typecheck

test: test-backend test-frontend

e2e:
	cd frontend && pnpm e2e

check: test
	cd frontend && pnpm build
	cd frontend && pnpm e2e

dev:
	@echo "MAMP MySQL :8889 → luego:"
	@echo "  Terminal A: cd backend && ./.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
	@echo "  Terminal B: cd frontend && pnpm dev"

seed:
	cd backend && ./.venv/bin/python scripts/seed_users.py
