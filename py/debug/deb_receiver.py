import os, sys
from io import StringIO 


def get_content_type():

    return "application/json"


def get_body():

    return \
        """{"measurements": [
                {
                    "id": "bff2b5eb-9601-43a2-b3cb-1068c8deaeba", 
                    "accepted_at": "2023-01-17 11:39:24.434 +2200", 
                    "sensor_id": "default-webhelp-sensor", 
                    "args": [
                        {"varname": "icap.pagereadId", "parsable_value": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}
                    ], 
                    "outs": [
                        {"varname": "icap.prevPagereadId", "parsable_value": "3938546c-131c-4a63-969e-85a4a1241e14"}, 
                        {"varname": "icap.cms.doc.uid", "parsable_value": "193"}, 
                        {"varname": "icap.cms.doc.verno", "parsable_value": "22"}, 
                        {"varname": "icap.cms.topic.uid", "parsable_value": "195"}, 
                        {"varname": "icap.cms.topic.verno", "parsable_value": "20"}, 
                        {"varname": "icap.page.title", "parsable_value": "Get Started"}, 
                        {"varname": "icap.page.url", "parsable_value": "http://localhost/webhelp/GetStarted.html"}, 
                        {"varname": "userAgentInfo", "parsable_value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}, 
                        {"varname": "userLangCode", "parsable_value": "en-US"}
                    ]
                }, 
                {
                    "id": "dd4d626c-a209-43a7-a346-63632734bed4", 
                    "accepted_at": "2023-01-17 11:39:24.436 +0200", 
                    "sensor_id": "default-webhelp-sensor", 
                    "args": [
                        {"varname": "icap.cms.doc.uid", "parsable_value": "193"}, 
                        {"varname": "icap.cms.doc.verno", "parsable_value": "22"}, 
                        {"varname": "icap.cms.topic.uid", "parsable_value": "195"}, 
                        {"varname": "icap.cms.topic.verno", "parsable_value": "20"}], 
                    "outs": [
                        {"varname": "icap.cms.taxonomy.Customer types", "parsable_value": "Individuals Government"}, 
                        {"varname": "icap.cms.taxonomy.Product scales", "parsable_value": "Enterprise Personal Workgroup"}
                    ]
                }, 
                {
                    "id": "577bfbde-7987-4a59-8782-f5dcef05d9e2", 
                    "accepted_at": "2023-01-17 11:39:24.437 +0200", 
                    "sensor_id": "default-webhelp-sensor", 
                    "args": [
                        {"varname": "icap.pagereadId", "parsable_value": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}, 
                        {"varname": "icap.action.code", "parsable_value": "LOAD"}, 
                        {"varname": "icap.action.timeOffset", "parsable_value": 3}], 
                    "outs": []
                }
            ]
        }"""


def mock_cgi_input():

    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body()))
    sys.stdin = StringIO(get_body())