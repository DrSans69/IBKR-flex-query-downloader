from typing import List

import requests

import src.data as data
from src.config import CREDS_FILENAME, CSV_FILENAME, XML_FILENAME
from src.data import Credentials
from src.ibkr_requests import fetch_report, send_request
from src.my_logging import logger_main as logger


def get_report(token: str, query_id: str) -> requests.Response | None:
    logger.info("Request to IBKR send")

    ref_code = send_request(token, query_id)

    if not ref_code:
        return None

    logger.info(
        f"Request success, downloading report, reference code - {ref_code}"
    )

    return fetch_report(token, ref_code)


def process_reports(creds: Credentials):

    if not creds:
        logger.error(
            f"File with credentials ({CREDS_FILENAME}) is empty or incorrectly structured"
        )
        return

    reports: List[str] = []

    for name, cred in creds.items():
        token = cred.token
        query_id = cred.query_id

        logger.info(f"Processing {name}")
        logger.info(f"token: {token}, id: {query_id}")

        report = get_report(token, query_id)

        if not report:
            continue

        content_type = report.headers.get("Content-Type", "")
        content = report.text.strip()

        if "xml" in content_type.lower():
            filename = f"{name}_{XML_FILENAME}"
            data.save_report(content, filename)

        else:  # csv (probably)
            filename = f"{name}_{CSV_FILENAME}"
            data.save_report(content, filename)

            reports.append(content)

    if not reports:
        logger.info("No csv reports")
        return

    logger.info("Merging csv reports")

    reports = data.merge_csv_texts(reports)

    data.save_report(reports[0], CSV_FILENAME)

    if len(reports) > 1:
        logger.warning("Some csv reports were not merged")
