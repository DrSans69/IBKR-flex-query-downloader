import argparse
from data import Credentials

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


def setup_parser():
    parser = argparse.ArgumentParser()
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
