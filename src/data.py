from config import REPORTS_DIR, XML_FILENAME, CSV_FILENAME, CREDS_FILENAME

import os
import csv
import logging
from dataclasses import dataclass
from typing import List


@dataclass
class Credential:
    name: str
    token: str
    query_id: str


credentials: List[Credential] = []


def save_xml(xml_data):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    xml_path = os.path.join(REPORTS_DIR, XML_FILENAME)
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_data)


def save_csv(csv_data):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    csv_path = os.path.join(REPORTS_DIR, CSV_FILENAME)
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(csv_data)


def load_credentials():
    credentials.clear()

    creds_path = CREDS_FILENAME
    if not os.path.exists(creds_path):
        logging.error(f"No {CREDS_FILENAME} found")
        return

    with open(creds_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            name = row.get("name")
            token = row.get("token")
            query_id = row.get("query_id")

            if not name or not token or not query_id:
                continue

            if not token.isdigit() or not query_id.isdigit():
                continue

            cred = Credential(name=name,
                              token=token,
                              query_id=query_id)

            credentials.append(cred)
