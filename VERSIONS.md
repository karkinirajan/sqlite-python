# Versions

Checked 2026-10-29. The repository previously had no dependency file.

| Component | Version | Note |
|---|---|---|
| Python | 3.13 | `requires-python >=3.13`; uses only the standard library (`sqlite3`) |
| SQLite library | whatever ships with Python | not pinned |
| Runtime dependencies | none | |

Dev: pytest, ruff (resolved in `uv.lock`).
