import argparse
import logging

import src.core as core
import src.gui as gui
from src.data import Credentials

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


creds = Credentials()


def add_cli(args):
    creds.add(args.name, args.token, args.query_id)
    print(f"Credential {args.name} added")


def list_cli(args):
    print("Credentials")
    for name, credential in creds.items():
        print(f"{name} - {credential.token}, {credential.query_id}")


def delete_cli(args):
    creds.remove(args.name)
    print(f"Credential {args.name} removed")


def reports_cli(args):
    if not args.silent:
        gui.run_gui(creds)
        return

    core.process_reports(creds)
    print("Processed")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=reports_cli)
    parser.add_argument('--silent', action='store_true')
    subparsers = parser.add_subparsers(dest='command')

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('--name', required=True)
    parser_add.add_argument('--token', required=True)
    parser_add.add_argument('--query-id', required=True)
    parser_add.set_defaults(func=add_cli)

    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=list_cli)

    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('--name', required=True)
    parser_delete.set_defaults(func=delete_cli)

    return parser


def main():
    parser = create_parser()

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
