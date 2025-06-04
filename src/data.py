import os
import csv
import logging
from dataclasses import dataclass
from typing import Any, List, Iterator, Dict, Iterable, Tuple

from config import REPORTS_DIR, XML_FILENAME, CSV_FILENAME, CREDS_FILENAME, FIELDS
from helpers import log_and_raise


@dataclass
class Credential:
    token: str
    query_id: str


class Credentials:
    def __init__(self) -> None:
        self._data: Dict[str, Credential] = {}

    def __iter__(self) -> Iterator[Credential]:
        return iter(self._data.values())

    def __len__(self) -> int:
        return len(self._data)

    def items(self) -> Iterable[Tuple[str, Credential]]:
        return self._data.items()

    def add(self, name: str, token: str, query_id: str) -> None:
        if name in self._data:
            logging.error(f"Credential with name '{name}' already exists.")
            return

        # if not token.isdigit():
        #     msg = f"Token {token} is incorrect"
        #     log_and_raise(msg, ValueError)

        # if not query_id.isdigit():
        #     msg = f"Query_id {query_id} is incorrect"
        #     log_and_raise(msg, ValueError)

        self._data[name] = Credential(token, query_id)

    def remove(self, name: str) -> None:
        if name not in self._data:
            logging.error(f"No credential found with name '{name}'.")
            return

        del self._data[name]

    def read(self):
        credentials = read_csv(CREDS_FILENAME)
        if not credentials:

            return

        for credential in credentials:
            name = credential.get("name")
            token = credential.get("token")
            query_id = credential.get("query_id")

            if not name or not token or not query_id:
                logging.error("Name or token or query_id is missing")
                continue

            self.add(name, token, query_id)

    def write(self):
        credentials = [
            {"name": name, "token": cred.token, "query_id": cred.query_id} for name, cred in self._data.items()]
        write_csv(CREDS_FILENAME, FIELDS, credentials)


def read_csv(path: str) -> List[Dict[str, str]] | None:

    if not os.path.exists(path):
        logging.error(f"No {path} found")
        return None

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def write_csv(path: str, fields: List[str], data: Iterable[Dict[str, Any]]):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def save_xml_report(xml_data: str):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    xml_path = os.path.join(REPORTS_DIR, XML_FILENAME)
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_data)


def save_csv_report(csv_data: str):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    csv_path = os.path.join(REPORTS_DIR, CSV_FILENAME)
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(csv_data)
