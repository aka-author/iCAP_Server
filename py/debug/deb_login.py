import os, sys
from io import StringIO 


def get_content_type():

    return "application/x-www-form-urlencoded"


def get_body():

    return "username=ditatoo111&password=haveYouReadUlysses?"


def mock_cgi_input():

    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body()))
    sys.stdin = StringIO(get_body())