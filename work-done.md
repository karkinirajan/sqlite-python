# Work done: sqlite-python

Branch: `chore/modernize` (local, not pushed). Date: 2026-10-29. The repo had no uncommitted work.

## What was there
Seven small tutorial scripts around a `customers` table (`create_table.py`, `insert_into.py`, `insert_many.py`, `database.py`, `our_db.py`, `database_app.py`, `our_app.py`), a tracked `customer.db` with 7 sample rows, no tests, no dependency file, no `.gitignore`, and a generic README. `show_all` existed twice (`database.py` and `our_db.py`), and each function opened its own connection and printed instead of returning data. `bot.py` (298 lines) is a Discord self-bot script that has nothing to do with SQLite.

## Changes by file
| File | Before | Change |
|---|---|---|
| `src/sqlite_python/db.py` | absent | New: `connect` (commit/rollback/close), `init_db`, `add_one`, `add_many` (atomic), `all_customers`, `email_lookup`, `delete_one`, `seed`; `Customer` dataclass; same schema as the original |
| `src/sqlite_python/__main__.py` | absent | New CLI (`init`, `seed`, `list`, `add`, `lookup`, `delete`) |
| `create_table.py`, `insert_into.py`, `insert_many.py`, `database.py`, `our_db.py`, `database_app.py`, `our_app.py` | seven overlapping scripts | Deleted: their functionality is in the package (`init_db`, `add_one`, `add_many`/`seed`, `all_customers`, `email_lookup`, `delete_one`). Nothing outside this set imported them |
| `delete_one` behavior | `execute(sql, id)` with `id` a string, which binds each character separately: it worked only for single-digit ids | Takes an integer id and binds it correctly (tested with ids 10 and 11) |
| `customer.db` | tracked binary database | Untracked (file stays on disk); `seed` recreates the sample rows |
| `tests/` | absent | New: 14 tests (CRUD, atomicity, rollback and close, injection text, legacy DB, CLI) |
| `pyproject.toml`, `uv.lock`, `.python-version` | absent | New: installable package, Python 3.13, no runtime dependencies |
| `.github/workflows/ci.yml`, `.gitignore` | absent | New |
| `README.md` | generic text | Rewritten from the code |
| `VERSIONS.md`, `work-done.md` | absent | New |

## Left untouched on purpose
`bot.py` is a Discord self-bot (user-account automation), which breaks Discord's terms of service and is built for automated bulk activity. I did not modify, lint, test or document it, and it is excluded from the tooling. Consider removing it from this repository.

## Verification (actual runs)
- `uv run pytest -q`: 14 passed. `uv run ruff check .` and `ruff format --check .`: clean.
- `git status` confirms `bot.py` is unchanged.

## Needs your attention
- `bot.py` (see above); if it carries any real tokens or API keys, treat them as exposed and rotate them. I did not read past its first lines.
- Nothing pushed. To publish: `git push -u origin chore/modernize`
