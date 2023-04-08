import os, sys
from io import StringIO 


def get_content_type():

    # return "application/json"

    return "multipart/form-data; boundary=---------------------------17449241711428180522542022093"


def get_body():
              
    return """---------------------------17449241711428180522542022093
Content-Disposition: form-data; name="unloadMeasurement"

{"measurements":[{"id":"6918ddcc-0256-4161-8dc7-f3cf2a94d931","accepted_at":"2023-04-08 12:02:20.451 UTC+03","sensor_id":"default-webhelp-sensor","args":[{"varname":"icap.pagereadId","parsable_value":"b95ed0ed-6d8e-49ac-9064-26e537eb488a"},{"varname":"icap.action.code","parsable_value":"UNLOAD"},{"varname":"icap.action.timeOffset","parsable_value":2092}],"outs":[]}]}
---------------------------17449241711428180522542022093--"""

    # return \
    #    """{"measurements": [
    #            {
    #                "id": "bff2b5eb-9601-43a2-b3cb-1068c8deaeba", 
    #                "acceptedAt": "2023-01-17 11:39:24.434 +0200", 
    #                "sensorId": "default-webhelp-sensor", 
    #                "args": [
    #                    {"varname": "icap.pagereadId", "parsableValue": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}
    #                ], 
    #                "outs": [
    #                    {"varname": "icap.prevPagereadId", "parsableValue": "3938546c-131c-4a63-969e-85a4a1241e14"}, 
    #                    {"varname": "icap.cms.doc.uid", "parsableValue": "193"}, 
    #                    {"varname": "icap.cms.doc.verno", "parsableValue": "22"}, 
    #                    {"varname": "icap.cms.topic.uid", "parsableValue": "195"}, 
    #                    {"varname": "icap.cms.topic.verno", "parsableValue": "20"}, 
    #                    {"varname": "icap.page.title", "parsableValue": "Get Started"}, 
    #                    {"varname": "icap.page.url", "parsableValue": "http://localhost/webhelp/GetStarted.html"}, 
    #                    {"varname": "userAgentInfo", "parsableValue": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}, 
    #                    {"varname": "userLangCode", "parsableValue": "en-US"}
    #                ]
    #            }, 
    #            {
    #                "id": "dd4d626c-a209-43a7-a346-63632734bed4", 
    #                "acceptedAt": "2023-01-17 11:39:24.436 +0200", 
    #                "sensorId": "default-webhelp-sensor", 
    #                "args": [
    #                    {"varname": "icap.cms.doc.uid", "parsableValue": "193"}, 
    #                    {"varname": "icap.cms.doc.verno", "parsableValue": "22"}, 
    #                    {"varname": "icap.cms.topic.uid", "parsableValue": "195"}, 
    #                    {"varname": "icap.cms.topic.verno", "parsableValue": "20"}], 
    #                "outs": [
    #                    {"varname": "icap.cms.taxonomy.Customer types", "parsableValue": "Individuals Government"}, 
    #                    {"varname": "icap.cms.taxonomy.Product scales", "parsableValue": "Enterprise Personal Workgroup"}
    #                ]
    #            }, 
    #            {
    #                "id": "577bfbde-7987-4a59-8782-f5dcef05d9e2", 
    #                "accepted_at": "2023-01-17 11:39:24.437 +0200", 
    #                "sensor_id": "default-webhelp-sensor", 
    #                "args": [
    #                    {"varname": "icap.pagereadId", "parsable_value": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}, 
    #                    {"varname": "icap.action.code", "parsable_value": "LOAD"}, 
    #                    {"varname": "icap.action.timeOffset", "parsable_value": 3}], 
    #                "outs": []
    #            }
    #        ]
    #    }"""

    # return \
    #    """{"measurements": [
    #            {
    #                "id": "bff2b5eb-9601-43a2-b3cb-1068c8deaeba", 
    #                "accepted_at": "2023-01-17 11:39:24.434 +0200", 
    #               "sensor_id": "default-webhelp-sensor", 
    #                "args": [
    #                   {"varname": "icap.pagereadId", "parsable_value": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}
    #                ], 
    #                "outs": [
    #                    {"varname": "icap.prevPagereadId", "parsable_value": "3938546c-131c-4a63-969e-85a4a1241e14"}, 
    #                    {"varname": "icap.cms.doc.uid", "parsable_value": "193"}, 
    #                    {"varname": "icap.cms.doc.verno", "parsable_value": "22"}, 
    #                    {"varname": "icap.cms.topic.uid", "parsable_value": "195"}, 
    #                    {"varname": "icap.cms.topic.verno", "parsable_value": "20"}, 
    #                    {"varname": "icap.page.title", "parsable_value": "Get Started"}, 
    #                    {"varname": "icap.page.url", "parsable_value": "http://localhost/webhelp/GetStarted.html"}, 
    #                    {"varname": "userAgentInfo", "parsable_value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}, 
    #                    {"varname": "userLangCode", "parsable_value": "en-US"}
    #                ]
    #            }, 
    #            {
    #                "id": "dd4d626c-a209-43a7-a346-63632734bed4", 
    #                "accepted_at": "2023-01-17 11:39:24.436 +0200", 
    #                "sensor_id": "default-webhelp-sensor", 
    #                "args": [
    #                    {"varname": "icap.cms.doc.uid", "parsable_value": "193"}, 
    #                    {"varname": "icap.cms.doc.verno", "parsable_value": "22"}, 
    #                    {"varname": "icap.cms.topic.uid", "parsable_value": "195"}, 
    #                    {"varname": "icap.cms.topic.verno", "parsable_value": "20"}], 
    #                "outs": [
    #                    {"varname": "icap.cms.taxonomy.Customer types", "parsable_value": "Individuals Government"}, 
    #                    {"varname": "icap.cms.taxonomy.Product scales", "parsable_value": "Enterprise Personal Workgroup"}
    #                ]
    #            }, 
    #            {
    #                "id": "577bfbde-7987-4a59-8782-f5dcef05d9e2", 
    #                "accepted_at": "2023-01-17 11:39:24.437 +0200", 
    #                "sensor_id": "default-webhelp-sensor", 
    #                "args": [
    #                    {"varname": "icap.pagereadId", "parsable_value": "2ce2a741-919a-47a1-9a3a-c05719bde44b"}, 
    #                    {"varname": "icap.action.code", "parsable_value": "LOAD"}, 
    #                    {"varname": "icap.action.timeOffset", "parsable_value": 3}], 
    #                "outs": []
    #            }
    #        ]
    #    }"""


def mock_cgi_input():

    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body()))
    sys.stdin = StringIO(get_body())