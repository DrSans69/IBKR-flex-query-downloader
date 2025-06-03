from config import SEND_REQUEST_URL_TEMPLATE, SUCCESS_STATUS, GET_STATEMENT_URL_TEMPLATE

import requests
import logging

from xml_wrapper import get_tag_value


def send_request(token, query_id):
    link_url = SEND_REQUEST_URL_TEMPLATE.format(token=token, query_id=query_id)
    logging.info(link_url)
    try:
        r = requests.get(link_url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return None

    res = get_tag_value(r.text, "Status")

    if res == SUCCESS_STATUS:
        return get_tag_value(r.text, "ReferenceCode")

    logging.error("Request failed")
    logging.error(
        f"Error message: {get_tag_value(r.text, 'ErrorMessage') or 'Undefined, try again later, if problem repeats, please contact mainter of this tool'}")

    return None


def get_statement(token, ref_code):
    data_url = GET_STATEMENT_URL_TEMPLATE.format(
        token=token, ref_code=ref_code)
    r = requests.get(data_url)

    return r
