run:
  fastapi dev main.py


format:
  uv run ruff format .


lint: format
  uv run ruff check .

test:
  uv run pytest

type-check:
  uv run ty check

ci: lint test type-check
  @echo  "CI passed"
