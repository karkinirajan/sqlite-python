from sqlite_python.__main__ import main


def run(db, *args):
    return main(["--db", str(db), *args])


def test_seed_then_list(tmp_path, capsys):
    db = tmp_path / "c.db"
    assert run(db, "seed") == 0
    capsys.readouterr()
    assert run(db, "list") == 0
    out = capsys.readouterr().out
    assert out.count("\n") == 7 and "Joshua\tRaintree" in out


def test_commands_work_on_a_fresh_file_without_init(tmp_path, capsys):
    db = tmp_path / "fresh.db"
    assert run(db, "add", "Ann", "Lee", "ann@lee.io") == 0
    assert run(db, "lookup", "ann@lee.io") == 0
    assert "Ann\tLee\tann@lee.io" in capsys.readouterr().out


def test_delete_reports_missing_ids(tmp_path, capsys):
    db = tmp_path / "d.db"
    run(db, "add", "A", "B", "a@b.c")
    capsys.readouterr()
    assert run(db, "delete", "1") == 0
    assert run(db, "delete", "1") == 1
    assert "No customer with id 1" in capsys.readouterr().err


def test_lookup_with_no_match_prints_nothing(tmp_path, capsys):
    db = tmp_path / "e.db"
    assert run(db, "lookup", "nobody@x.y") == 0
    assert capsys.readouterr().out == ""
