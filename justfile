run:
  uv run fastapi dev src/main.py

format:
  uv run ruff format .

lint:
  uv lock --check
  uv run ruff check .

test:
  uv run pytest

type-check:
  uv run ty check

schemathesis:
  @echo "Running schemathesis tests. As of now, only local"
  uv run schemathesis run http://127.0.0.1:8000/openapi.json

ci: lint test type-check
  @echo  "CI passed"
