import logging

import requests

from config import SEND_REQUEST_URL_TEMPLATE, FAIL_STATUS, SUCCESS_STATUS, GET_STATEMENT_URL_TEMPLATE
from xml_wrapper import get_tag_value


def send_request(token: str, query_id: str) -> str | None:
    link_url = SEND_REQUEST_URL_TEMPLATE.format(token=token, query_id=query_id)
    logging.info(link_url)

    try:
        r = requests.get(link_url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return None

    res = get_tag_value(r.text, "Status")

    if res != SUCCESS_STATUS:
        logging.error("Request failed")
        logging.error(
            f"Error message: {get_tag_value(r.text, 'ErrorMessage') or 'Undefined, try again later, if problem repeats, please contact mainter of this tool'}")
        return None

    return get_tag_value(r.text, "ReferenceCode")


def get_statement(token: str, ref_code: str) -> requests.Response | None:
    data_url = GET_STATEMENT_URL_TEMPLATE.format(
        token=token, ref_code=ref_code)
    try:
        r = requests.get(data_url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return None

    return r
