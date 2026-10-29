# sqlite-python

A small, tested reference for using SQLite from Python's standard library: a `customers` table with safe create/read/delete helpers and a command-line tool. No third-party dependencies.

## What it shows

- Parameterised queries everywhere (no string-built SQL), including values that look like SQL injection.
- A `connect()` context manager that commits on success, rolls back on error and always closes the connection.
- Atomic bulk inserts (`add_many` either adds every row or none).
- Typed results (`Customer` dataclass) instead of printing inside the data layer.
- Compatibility with the original tutorial database (same `customers(first_name, last_name, email)` schema).

## Install

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/kneeraazon404/sqlite-python.git
cd sqlite-python
uv sync
```

## Use as a library

```python
from sqlite_python import add_one, add_many, all_customers, email_lookup, delete_one, init_db

init_db("customer.db")
add_one("Laura", "Smith", "laura@smith.com", "customer.db")
add_many([("Wes", "Brown", "wes@brown.com")], "customer.db")
print(all_customers("customer.db"))      # [Customer(rowid=1, ...), ...]
print(email_lookup("wes@brown.com", "customer.db"))
delete_one(1, "customer.db")             # True if a row was removed
```

Every function takes an optional database path (default `customer.db`, or `SQLITE_PYTHON_DB`).

## Command line

```bash
uv run python -m sqlite_python seed                      # create table + 7 sample customers
uv run python -m sqlite_python list
uv run python -m sqlite_python add Laura Smith laura@smith.com
uv run python -m sqlite_python lookup laura@smith.com
uv run python -m sqlite_python delete 3
uv run python -m sqlite_python --db other.db list        # use a different file
```

## Testing

```bash
uv run pytest -q
uv run ruff check . && uv run ruff format --check .
```

14 tests cover the helpers, atomicity, rollback and closing, SQL-injection text, multi-digit ids, a database created by the original script, and the CLI.

## Project structure

```
src/sqlite_python/   db.py (data access), __main__.py (CLI)
tests/               pytest suite
```

## Note on `bot.py`

`bot.py` is unrelated to SQLite and is not part of this project; it has been left exactly as it was and is excluded from linting and documentation.

## License

Apache License 2.0. See [LICENSE](LICENSE).
