import os, sys
from io import StringIO 


def get_content_type():

    return "application/json"


def get_body():

    return \
        """{
                "shop_name":    "basestat1",
                "report_name":  "Messages",
                "conditions":   []
        }"""


def mock_cgi_input():

    os.environ["HTTP_COOKIE"] = "1706e33e-a6d1-4cd3-bba7-b0cc6121d91d"
    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body()))

    sys.stdin = StringIO(get_body())