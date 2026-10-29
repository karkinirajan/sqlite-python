import sqlite3

import pytest

from sqlite_python import (
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


@pytest.fixture
def path(tmp_path):
    p = tmp_path / "test.db"
    init_db(p)
    return p


def test_init_is_idempotent_and_creates_the_original_schema(path):
    init_db(path)
    with connect(path) as conn:
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(customers)")]
    assert cols == ["first_name", "last_name", "email"]


def test_add_one_returns_rowid_and_roundtrips(path):
    rowid = add_one("Laura", "Smith", "laura@smith.com", path)
    assert rowid == 1
    assert all_customers(path) == [Customer(1, "Laura", "Smith", "laura@smith.com")]


def test_add_many_adds_all_rows_and_reports_count(path):
    rows = [("A", "B", "a@b.c"), ("C", "D", "c@d.e"), ("E", "F", "e@f.g")]
    assert add_many(rows, path) == 3
    assert [c.email for c in all_customers(path)] == ["a@b.c", "c@d.e", "e@f.g"]


def test_add_many_is_atomic(path):
    with pytest.raises(sqlite3.ProgrammingError):
        add_many([("ok", "row", "ok@x.y"), ("bad", "row")], path)  # second row has 2 values
    assert all_customers(path) == []


def test_email_lookup_is_exact(path):
    add_many([("A", "B", "a@b.c"), ("C", "D", "c@d.e")], path)
    assert [c.first_name for c in email_lookup("a@b.c", path)] == ["A"]
    assert email_lookup("a@b", path) == []


def test_sql_injection_text_is_stored_as_data(path):
    evil = "x'); DROP TABLE customers;--"
    add_one("Eve", "Hacker", evil, path)
    assert [c.email for c in all_customers(path)] == [evil]
    assert email_lookup(evil, path)[0].first_name == "Eve"


def test_delete_one_with_multi_digit_ids(path):
    for i in range(12):
        add_one(f"n{i}", "x", f"{i}@x.y", path)
    assert delete_one(10, path) is True  # the original passed a str, which broke for ids > 9
    assert delete_one("11", path) is True
    assert delete_one(999, path) is False
    assert len(all_customers(path)) == 10


def test_seed_adds_the_tutorial_customers(tmp_path):
    p = tmp_path / "seeded.db"
    assert seed(p) == 7
    assert email_lookup("john@codemy.com", p)[0].last_name == "Elder"


def test_connect_rolls_back_on_error_and_closes(path):
    with pytest.raises(RuntimeError):
        with connect(path) as conn:
            conn.execute("INSERT INTO customers VALUES ('a','b','c')")
            raise RuntimeError("boom")
    assert all_customers(path) == []
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("SELECT 1")  # connection was closed


def test_reads_a_database_created_by_the_original_script(tmp_path):
    p = tmp_path / "legacy.db"
    conn = sqlite3.connect(p)
    conn.execute(
        "CREATE TABLE customers (\n\t\tfirst_name text,\n\t\tlast_name text,\n\t\temail text\n\t)"
    )
    conn.execute("INSERT INTO customers VALUES ('Mary', 'Brown', 'mary@codemy.com')")
    conn.commit()
    conn.close()
    assert all_customers(p) == [Customer(1, "Mary", "Brown", "mary@codemy.com")]
