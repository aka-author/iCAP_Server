from typing import Dict
import os, sys
from io import StringIO 


def get_content_type():

    return "application/json"


def get_body(sample_number: int) -> Dict:

    sample_requests = [
        """{
            "app_request_type_name": "performer_task",
            "ver": 2,
            "app_request_body": {
                "performer_name": "system",
                "task_name": "preprocess",
                "prolog": null,
                "task_body": null
            }       
        }"""
    ]
    
    return sample_requests[sample_number]


def mock_cgi_input():

    os.environ["HTTP_COOKIE"] = "6e3abbc1-a9c6-495e-b51c-42f812bdca3d"
    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body(0)))

    sys.stdin = StringIO(get_body(0))