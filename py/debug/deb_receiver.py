import os, sys
from io import StringIO 


def get_content_type():

    return "application/json"


def get_body():

    return '{"measurements": [{"id": "bff2b5eb-9601-43a2-b3cb-1068c8deaeba", "acceptedAt": "2023-01-17 11:39:24.434 UTC+02", "sensorId": "default-webhelp-sensor", "args": [{"varName": "icap.pagereadId", "parsableValue": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}], "outs": [{"varName": "icap.prevPagereadId", "parsableValue": "3938546c-131c-4a63-969e-85a4a1241e14"}, {"varName": "icap.cms.doc.uid", "parsableValue": "193"}, {"varName": "icap.cms.doc.verno", "parsableValue": "22"}, {"varName": "icap.cms.topic.uid", "parsableValue": "195"}, {"varName": "icap.cms.topic.verno", "parsableValue": "20"}, {"varName": "icap.page.title", "parsableValue": "Get Started"}, {"varName": "icap.page.url", "parsableValue": "http://localhost/webhelp/GetStarted.html"}, {"varName": "userAgentInfo", "parsableValue": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}, {"varName": "userLangCode", "parsableValue": "en-US"}]}, {"id": "dd4d626c-a209-43a7-a346-63632734bed4", "acceptedAt": "2023-01-17 11:39:24.436 UTC+02", "sensorId": "default-webhelp-sensor", "args": [{"varName": "icap.cms.doc.uid", "parsableValue": "193"}, {"varName": "icap.cms.doc.verno", "parsableValue": "22"}, {"varName": "icap.cms.topic.uid", "parsableValue": "195"}, {"varName": "icap.cms.topic.verno", "parsableValue": "20"}], "outs": [{"varName": "icap.cms.taxonomy.Customer types", "parsableValue": "Individuals Government"}, {"varName": "icap.cms.taxonomy.Product scales", "parsableValue": "Enterprise Personal Workgroup"}]}, {"id": "577bfbde-7987-4a59-8782-f5dcef05d9e2", "acceptedAt": "2023-01-17 11:39:24.437 UTC+02", "sensorId": "default-webhelp-sensor", "args": [{"varName": "icap.pagereadId", "parsableValue": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}, {"varName": "icap.action.code", "parsableValue": "LOAD"}, {"varName": "icap.action.timeOffset", "parsableValue": 3}], "outs": []}]}'


def mock_cgi_input():

    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body()))
    sys.stdin = StringIO(get_body())