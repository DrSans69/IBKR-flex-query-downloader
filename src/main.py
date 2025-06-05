import logging

from ibkr_requests import *
from data import *
from config import CREDS_FILENAME, XML_FILENAME, CSV_FILENAME, REPORTS_DIR

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

    return get_statement(token, ref_code)


def main():
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
            filename = f"{XML_FILENAME}_{name}"
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
        filename = f"{CSV_FILENAME}_{i}"
        save_report(text, filename)


if __name__ == "__main__":
    main()
    input()
