import logging
import argparse

from ibkr_requests import *
from data import *
from config import CREDS_FILENAME, XML_FILENAME, CSV_FILENAME, REPORTS_DIR

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

creds = Credentials()


def get_report(token: str, query_id: str) -> requests.Response | None:
    logging.info("Request to IBKR send")

    ref_code = send_request(token, query_id)

    if not ref_code:
        return None

    logging.info(
        f"Request success, downloading report, reference code - {ref_code}")

    return get_statement(token, ref_code)


def process_reports():
    creds = Credentials()

    if not creds:
        logging.error(
            f"File with credentials ({CREDS_FILENAME}) is empty or incorrectly structured")
        return

    reports: List[str] = []

    for name, cred in creds.items():
        token = cred.token
        query_id = cred.query_id

        logging.info(f"Processing {name}")
        logging.info(f"token: {token}, id: {query_id}")

        report = get_report(token, query_id)

        if not report:
            continue

        content_type = report.headers.get("Content-Type", "")
        content = report.text.strip()

        if "xml" in content_type.lower():
            logging.warning("Report is xml")
            filename = f"{name}_{XML_FILENAME}"
            save_report(content, filename)

        else:
            reports.append(content)

    if not reports:
        logging.info("No csv reports")
        return

    logging.info("Merging reports")

    reports = merge_csv_texts(reports)

    save_report(reports[0], CSV_FILENAME)

    for i, text in enumerate(reports[1:], start=1):
        filename = f"{i}_{CSV_FILENAME}"
        save_report(text, filename)


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


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # Add
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('--name', required=True)
    parser_add.add_argument('--token', required=True)
    parser_add.add_argument('--query-id', required=True)
    parser_add.set_defaults(func=add_cli)

    # List
    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=list_cli)

    # Delete
    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('--name', required=True)
    parser_delete.set_defaults(func=delete_cli)

    args = parser.parse_args()
    if args.command:
        args.func(args)
        creds.write()
    else:
        process_reports()


if __name__ == "__main__":
    main()
