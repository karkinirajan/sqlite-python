"""Data access for the `customers` table.

All queries are parameterised, every connection is closed (and committed or rolled back) by the
``connect`` context manager, and nothing prints: functions return data and the CLI decides how to
show it.
"""

import os
import sqlite3
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DB = Path(os.environ.get("SQLITE_PYTHON_DB", "customer.db"))

# Same schema as the original tutorial database, so existing customer.db files keep working.
SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    first_name TEXT,
    last_name  TEXT,
    email      TEXT
)
"""

SAMPLE_CUSTOMERS = [
    ("John", "Elder", "john@codemy.com"),
    ("Tim", "Smith", "tim@codemy.com"),
    ("Mary", "Brown", "mary@codemy.com"),
    ("Wes", "Brown", "wes@brown.com"),
    ("Steph", "Kuewa", "steph@kuewa.com"),
    ("Brenda", "Smitherton", "brenda@smitherton.com"),
    ("Joshua", "Raintree", "josh@raintree.com"),
]


@dataclass(frozen=True)
class Customer:
    rowid: int
    first_name: str
    last_name: str
    email: str


def _to_customer(row: sqlite3.Row) -> Customer:
    return Customer(row["rowid"], row["first_name"], row["last_name"], row["email"])


@contextmanager
def connect(path: str | os.PathLike = DEFAULT_DB) -> Iterator[sqlite3.Connection]:
    """Open the database; commit on success, roll back on error, always close."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(path: str | os.PathLike = DEFAULT_DB) -> None:
    """Create the customers table if it does not exist (safe to call repeatedly)."""
    with connect(path) as conn:
        conn.execute(SCHEMA)


def add_one(first: str, last: str, email: str, path: str | os.PathLike = DEFAULT_DB) -> int:
    """Insert one customer and return its rowid."""
    with connect(path) as conn:
        cursor = conn.execute("INSERT INTO customers VALUES (?, ?, ?)", (first, last, email))
        return cursor.lastrowid


def add_many(rows: Iterable[tuple[str, str, str]], path: str | os.PathLike = DEFAULT_DB) -> int:
    """Insert many (first, last, email) rows atomically; return how many were added."""
    with connect(path) as conn:
        cursor = conn.executemany("INSERT INTO customers VALUES (?, ?, ?)", list(rows))
        return cursor.rowcount


def all_customers(path: str | os.PathLike = DEFAULT_DB) -> list[Customer]:
    with connect(path) as conn:
        rows = conn.execute("SELECT rowid, * FROM customers ORDER BY rowid").fetchall()
    return [_to_customer(r) for r in rows]


def email_lookup(email: str, path: str | os.PathLike = DEFAULT_DB) -> list[Customer]:
    with connect(path) as conn:
        rows = conn.execute(
            "SELECT rowid, * FROM customers WHERE email = ? ORDER BY rowid", (email,)
        ).fetchall()
    return [_to_customer(r) for r in rows]


def delete_one(rowid: int, path: str | os.PathLike = DEFAULT_DB) -> bool:
    """Delete by rowid; return True if a row was removed."""
    with connect(path) as conn:
        cursor = conn.execute("DELETE FROM customers WHERE rowid = ?", (int(rowid),))
        return cursor.rowcount > 0


def seed(path: str | os.PathLike = DEFAULT_DB) -> int:
    """Create the table and add the tutorial's sample customers. Returns the number added."""
    init_db(path)
    return add_many(SAMPLE_CUSTOMERS, path)
