"""Small, safe examples of working with SQLite from Python (a `customers` table)."""

from .db import (
    DEFAULT_DB,
    Customer,
    add_many,
    add_one,
    all_customers,
    connect,
    delete_one,
    email_lookup,
    init_db,
    seed,
)

__all__ = [
    "DEFAULT_DB",
    "Customer",
    "add_many",
    "add_one",
    "all_customers",
    "connect",
    "delete_one",
    "email_lookup",
    "init_db",
    "seed",
]
