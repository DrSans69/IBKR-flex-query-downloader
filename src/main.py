import logging
from typing import List

from ibkr_requests import *
from data import Credentials
import data
from config import CREDS_FILENAME, XML_FILENAME, CSV_FILENAME, REPORTS_DIR
import cli

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


def get_report(token: str, query_id: str) -> requests.Response | None:
    logging.info("Request to IBKR send")

    ref_code = send_request(token, query_id)

    if not ref_code:
        return None

    logging.info(
        f"Request success, downloading report, reference code - {ref_code}")

    return fetch_report(token, ref_code)


def process_reports(creds: Credentials):

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
            data.save_report(content, filename)

        else:
            reports.append(content)

    if not reports:
        logging.info("No csv reports")
        return

    logging.info("Merging reports")

    reports = data.merge_csv_texts(reports)

    data.save_report(reports[0], CSV_FILENAME)

    for i, text in enumerate(reports[1:], start=1):
        filename = f"{i}_{CSV_FILENAME}"
        data.save_report(text, filename)


def main():
    creds = Credentials()

    parser = cli.setup_parser()
    args = parser.parse_args()
    if args.command:
        args.func(args)
        creds.write()
        return

    process_reports(creds)


if __name__ == "__main__":
    main()
