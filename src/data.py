import os
import csv
import logging
from dataclasses import dataclass
from typing import Any, List, Iterator, Dict, Iterable, Tuple
from io import StringIO

from config import REPORTS_DIR, CREDS_FILENAME, FIELDS


@dataclass
class Credential:
    token: str
    query_id: str


class Credentials:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._data: Dict[str, Credential] = {}
            self.read()
            self._initialized = True

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
        logging.info(f"Credential '{name}' added")

    def remove(self, name: str) -> None:
        if name not in self._data:
            logging.error(f"No credential found with name '{name}'.")
            return

        del self._data[name]
        logging.info(f"Credential '{name}' removed")

    def read(self):
        credentials = read_csv(CREDS_FILENAME)
        if not credentials:
            return

        logging.info(f"Loading credentials from file {CREDS_FILENAME}")

        for credential in credentials:
            name = credential.get("name")
            token = credential.get("token")
            query_id = credential.get("query_id")

            if not name or not token or not query_id:
                logging.error("Name or token or query_id is missing")
                continue

            self.add(name, token, query_id)

        logging.info(f"Done loading")

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

    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def save_report(data: str, filename: str):

    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
        logging.info(f"Report saved to {path}")


def merge_csv_texts(csv_texts: List[str]) -> List[str]:
    if not csv_texts:
        return []

    main_csv = csv_texts[0]
    main_reader = csv.reader(StringIO(main_csv))
    main_header = next(main_reader)
    all_rows = list(main_reader)

    merged = []

    for text in csv_texts[1:]:
        reader = csv.reader(StringIO(text))
        try:
            header = next(reader)
        except StopIteration:
            logging.error("Empty csv, skiping")
            continue

        if header == main_header:
            all_rows.extend(reader)
        else:
            merged.append(text)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(main_header)
    writer.writerows(all_rows)

    merged.insert(0, output.getvalue())

    return merged
