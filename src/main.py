import logging

from ibkr_requests import *
from data import *
from config import CREDS_FILENAME

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

    if not len(creds):
        logging.warning(
            f"File with credentials ({CREDS_FILENAME}) is empty or incorrectly structured")

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
            save_xml_report(content)
            logging.info("XML data saved to trade_history.xml")

        else:
            save_csv_report(content)
            logging.info("CSV data saved to trade_history.csv")

        logging.info("Report saved")


if __name__ == "__main__":
    main()
    input()
