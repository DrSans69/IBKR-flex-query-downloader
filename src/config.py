REPORTS_DIR = "reports"
CSV_FILENAME = "trade_history.csv"
XML_FILENAME = "trade_history.xml"
CREDS_FILENAME = "credentials.csv"
FIELDS = ["name", "token", "query_id"]
FAIL_STATUS = "Fail"
SUCCESS_STATUS = "Success"
SEND_REQUEST_URL_TEMPLATE = "https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={query_id}&v=3"
FETCH_REPORT_URL_TEMPLATE = "https://www.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement?t={token}&q={ref_code}&v=3"
