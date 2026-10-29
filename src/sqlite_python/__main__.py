"""Command line: ``python -m sqlite_python [--db FILE] {init,seed,list,add,lookup,delete}``."""

import argparse
import sys

from . import db


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sqlite_python", description=__doc__)
    parser.add_argument(
        "--db", default=str(db.DEFAULT_DB), help="database file (default: %(default)s)"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="create the customers table")
    sub.add_parser("seed", help="create the table and add the sample customers")
    sub.add_parser("list", help="show all customers")
    add = sub.add_parser("add", help="add a customer")
    add.add_argument("first")
    add.add_argument("last")
    add.add_argument("email")
    lookup = sub.add_parser("lookup", help="find customers by exact email")
    lookup.add_argument("email")
    delete = sub.add_parser("delete", help="delete a customer by id")
    delete.add_argument("id", type=int)
    return parser


def _show(customers: list[db.Customer]) -> None:
    for c in customers:
        print(f"{c.rowid}\t{c.first_name}\t{c.last_name}\t{c.email}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    db.init_db(args.db)  # idempotent, so every command works on a fresh file
    if args.command == "init":
        db.init_db(args.db)
        print(f"Initialised {args.db}")
    elif args.command == "seed":
        print(f"Added {db.seed(args.db)} sample customers to {args.db}")
    elif args.command == "list":
        _show(db.all_customers(args.db))
    elif args.command == "add":
        print(f"Added customer {db.add_one(args.first, args.last, args.email, args.db)}")
    elif args.command == "lookup":
        _show(db.email_lookup(args.email, args.db))
    elif args.command == "delete":
        if not db.delete_one(args.id, args.db):
            print(f"No customer with id {args.id}", file=sys.stderr)
            return 1
        print(f"Deleted customer {args.id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
