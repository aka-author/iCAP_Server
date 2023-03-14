import os, sys
from io import StringIO 


def get_content_type():

    return "application/json"


def get_body():

    return \
        """{
                "shop_name":    "basestat",
                "report_name":  "Messages",
                "conditions":   []
        }"""


def mock_cgi_input():

    os.environ["HTTP_COOKIE"] = "71a08bf6-b0fb-4954-95b9-998af2bfa745"
    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body()))

    sys.stdin = StringIO(get_body())