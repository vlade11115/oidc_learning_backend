run:
  fastapi dev main.py

lint:
  uv run ruff check .

format:
  uv run ruff format .

test:
  uv run pytest

type-check:
  uv run ty check
