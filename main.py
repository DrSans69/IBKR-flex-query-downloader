import requests
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET

load_dotenv()

REPORTS_DIR = "reports"
CSV_FILENAME = "trade_history.csv"
XML_FILENAME = "trade_history.xml"
FAIL_STATUS = "Fail"
SUCCESS_STATUS = "Success"
SEND_REQUEST_URL_TEMPLATE = "https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={query_id}&v=3"
GET_STATEMENT_URL_TEMPLATE = "https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?t={token}&q={ref_code}&v=3"

TOKEN = os.getenv("IBKR_TOKEN")
QUERY_ID = os.getenv("FLEX_QUERY_ID")


def get_tag_value(xml_string, tag):
    try:
        root = ET.fromstring(xml_string)
        element = root.find('.//' + tag)
        if element is not None:
            return element.text
    except ET.ParseError:
        pass
    return None


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


def check_env_vars() -> bool:
    if TOKEN is not None and QUERY_ID is not None:
        return True

    if TOKEN is None and QUERY_ID is None:
        print("Token and query id are missing")
    elif TOKEN is None:
        print("Token is missing")
    elif QUERY_ID is None:
        print("Query id is missing")

    print("Please set them as your environment variables or in .env file in form:\nIBKR_TOKEN=your_ibkr_token\nFLEX_QUERY_ID=your_flex_query_id")

    return False


def send_request():
    link_url = SEND_REQUEST_URL_TEMPLATE.format(token=TOKEN, query_id=QUERY_ID)
    r = requests.get(link_url)
    res = get_tag_value(r.text, "Status")

    if res == SUCCESS_STATUS:
        return get_tag_value(r.text, "ReferenceCode")

    print(
        f"Request failed\nError message: {get_tag_value(r.text, 'ErrorMessage') or 'Undefined, try again later, if problem repeats, please contact mainter of this tool'}")

    return None


def get_statement(ref_code):
    data_url = GET_STATEMENT_URL_TEMPLATE.format(
        token=TOKEN, ref_code=ref_code)
    r = requests.get(data_url)

    # todo: implement error checking
    return r


def main():

    if not check_env_vars():
        return

    print("Request to IBKR send")

    ref_code = send_request()

    if not ref_code:
        return

    print(f"Request success, downloading report, reference code - {ref_code}")

    r = get_statement(ref_code)
    content = r.text.strip()
    content_type = r.headers.get("Content-Type", "")

    if not content:
        return

    if "xml" in content_type.lower():
        save_xml(content)
        print("XML data saved to trade_history.xml")

    else:
        save_csv(content)
        print("CSV data saved to trade_history.csv")

    print("Report saved")


if __name__ == "__main__":
    main()
    input()
