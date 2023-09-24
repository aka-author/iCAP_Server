import os 
import sys
from io import StringIO 


def get_content_type():

    return "application/json"


def get_body(sample_number: int) -> dict:

    sample_requests = {
        "get_directories": """{
            "app_request_type_name": "performer_task",
            "ver": 2,
            "app_request_body": {
                "performer_name": "webstat",
                "task_name": "get_directories",
                "task_body": {
                }
            }
        }""",
        "get_quality_summaries": """{
            "app_request_type_name": "performer_task",
            "ver": 2,
            "app_request_body": {
                "performer_name": "webstat",
                "task_name": "get_quality_summaries",
                "task_body": {
                    "scope": {
                        "conditions": [
                            {
                                "condition_name": "browser",
                                "varname": "userBrowser",
                                "range": {
                                    "datatype_name": "string",
                                    "range_type_name": "set",
                                    "constraints": {
                                        "members": ["chrome"]
                                    }
                                }
                            },
                            {
                                "condition_name": "time",
                                "varname": "accepted_at", 
                                "range": {
                                    "datatype_name": "timestamp",
                                    "range_type_name": "segment",
                                    "constraints": { 
                                        "min": "2023-04-01", 
                                        "max": "2023-09-10"
                                    }
                                }
                            }
                        ],
                        "expression": "*"
                    },
                    "granularity": {
                        "dimensions": [
                            {
                                "varname": "icap.cms.topic.uid"
                            }    
                        ]
                    } 
                }
            }
        }""",
        "get_audience_breakdown": """{
            "app_request_type_name": "performer_task",
            "ver": 2,
            "app_request_body": {
                "performer_name": "webstat",
                "task_name": "get_audience_breakdown",
                "task_body": {
                    "scope": {
                        "conditions": [
                            {
                                "condition_name": "time",
                                "varname": "accepted_at", 
                                "range": {
                                    "datatype_name": "timestamp",
                                    "range_type_name": "segment",
                                    "constraints": { 
                                        "min": "2023-04-01", 
                                        "max": "2023-09-20"
                                    }
                                }
                            }
                        ],
                        "expression": "*"
                    }
                }
            }
        }"""
        
    }
    
    return sample_requests[sample_number]


def mock_cgi_input():

    body = get_body("get_audience_breakdown")

    os.environ["HTTP_COOKIE"] = "12345678-1234-1234-1234-123456789abc"
    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(body))

    sys.stdin = StringIO(body)


"""
"output_template": {
                        "groups": [
                            {
                                "group_name": "Q1",
                                "countries": [
                                    {"country_code": "de", "share": 0.10},
                                    {"country_code": "es", "share": 0.10},
                                    {"country_code": "il", "share": 0.10},
                                    {"country_code": "us", "share": 0.70}
                                ],
                                "user_langs": [
                                    {"lang_code": "de", "share": 0.05},
                                    {"lang_code": "es", "share": 0.05},
                                    {"lang_code": "he", "share": 0.10},
                                    {"lang_code": "en", "share": 0.80}
                                ],
                                "oss": [
                                    {"os_code": "android", "share": 0.15},
                                    {"os_code": "ios",     "share": 0.15},
                                    {"os_code": "linux",   "share": 0.10},
                                    {"os_code": "osx",     "share": 0.20},
                                    {"os_code": "windows", "share": 0.40}
                                ],
                                "browsers": [
                                    {"browser_code": "chrome",  "share": 0.20},
                                    {"browser_code": "edge",    "share": 0.20},
                                    {"browser_code": "firefox", "share": 0.20},
                                    {"browser_code": "opera",   "share": 0.20},
                                    {"browser_code": "safari",  "share": 0.20}
                                ],
                                "goodness": 0.4,
                                "badness": 0.86,
                                "pain_factor": 0.12
                            },
                            {
                                "group_name": "Q2",
                                "countries": [
                                    {"country_code": "de", "share": 0.10},
                                    {"country_code": "es", "share": 0.10},
                                    {"country_code": "il", "share": 0.15},
                                    {"country_code": "us", "share": 0.65}
                                ],
                                "user_langs": [
                                    {"lang_code": "de", "share": 0.05},
                                    {"lang_code": "es", "share": 0.05},
                                    {"lang_code": "he", "share": 0.11},
                                    {"lang_code": "en", "share": 0.79}
                                ],
                                "oss": [
                                    {"os_code": "android", "share": 0.14},
                                    {"os_code": "ios",     "share": 0.16},
                                    {"os_code": "linux",   "share": 0.12},
                                    {"os_code": "osx",     "share": 0.20},
                                    {"os_code": "windows", "share": 0.38}
                                ],
                                "browsers": [
                                    {"browser_code": "chrome",  "share": 0.20},
                                    {"browser_code": "edge",    "share": 0.18},
                                    {"browser_code": "firefox", "share": 0.22},
                                    {"browser_code": "opera",   "share": 0.19},
                                    {"browser_code": "safari",  "share": 0.21}
                                ],
                                "goodness": 0.45,
                                "badness": 0.70,
                                "pain_factor": 0.11
                            },
                            {
                                "group_name": "Q3",
                                "countries": [
                                    {"country_code": "de", "share": 0.10},
                                    {"country_code": "es", "share": 0.10},
                                    {"country_code": "il", "share": 0.20},
                                    {"country_code": "us", "share": 0.60}
                                ],
                                "user_langs": [
                                    {"lang_code": "de", "share": 0.05},
                                    {"lang_code": "es", "share": 0.05},
                                    {"lang_code": "he", "share": 0.24},
                                    {"lang_code": "en", "share": 0.66}
                                ],
                                "oss": [
                                    {"os_code": "android", "share": 0.15},
                                    {"os_code": "ios",     "share": 0.15},
                                    {"os_code": "linux",   "share": 0.10},
                                    {"os_code": "osx",     "share": 0.20},
                                    {"os_code": "windows", "share": 0.40}
                                ],
                                "browsers": [
                                    {"browser_code": "chrome",  "share": 0.30},
                                    {"browser_code": "edge",    "share": 0.10},
                                    {"browser_code": "firefox", "share": 0.30},
                                    {"browser_code": "opera",   "share": 0.10},
                                    {"browser_code": "safari",  "share": 0.20}
                                ],
                                "goodness": 0.51,
                                "badness": 0.66,
                                "pain_factor": 0.09
                            },
                            {
                                "group_name": "Q4",
                                "countries": [
                                    {"country_code": "de", "share": 0.10},
                                    {"country_code": "es", "share": 0.10},
                                    {"country_code": "il", "share": 0.25},
                                    {"country_code": "us", "share": 0.55}
                                ],
                                "user_langs": [
                                    {"lang_code": "de", "share": 0.05},
                                    {"lang_code": "es", "share": 0.05},
                                    {"lang_code": "he", "share": 0.30},
                                    {"lang_code": "en", "share": 0.60}
                                ],
                                "oss": [
                                    {"os_code": "android", "share": 0.15},
                                    {"os_code": "ios",     "share": 0.15},
                                    {"os_code": "linux",   "share": 0.10},
                                    {"os_code": "osx",     "share": 0.30},
                                    {"os_code": "windows", "share": 0.30}
                                ],
                                "browsers": [
                                    {"browser_code": "chrome",  "share": 0.10},
                                    {"browser_code": "edge",    "share": 0.30},
                                    {"browser_code": "firefox", "share": 0.10},
                                    {"browser_code": "opera",   "share": 0.30},
                                    {"browser_code": "safari",  "share": 0.20}
                                ],
                                "goodness": 0.59,
                                "badness": 0.59,
                                "pain_factor": 0.05
                            }
                        ]
                    }
                }
            }
"""

"""
    ,
                                {
                                    "varname": "accepted_at",
                                    "group_by_value_datatype_name": "string",
                                    "groups": [
                                        {
                                            "group_by_value": "Q1",
                                            "range": {
                                                "datatype_name": "timestamp",
                                                "range_type_name": "segment",
                                                "constraints": { 
                                                    "min": "2022-01-01", 
                                                    "max": "2022-03-31"
                                                }
                                            }
                                        },
                                        {
                                            "group_by_value": "Q2",
                                            "range": {
                                                "datatype_name": "timestamp",
                                                "range_type_name": "segment",
                                                "constraints": { 
                                                    "min": "2022-04-01", 
                                                    "max": "2022-06-30"
                                                }
                                            }
                                        },
                                        {
                                            "group_by_value": "Q3",
                                            "range": {
                                                "datatype_name": "timestamp",
                                                "range_type_name": "segment",
                                                "constraints": { 
                                                    "min": "2022-07-01", 
                                                    "max": "2022-09-30"
                                                }
                                            }
                                        },
                                        {
                                            "group_by_value": "Q4",
                                            "range": {
                                                "datatype_name": "timestamp",
                                                "range_type_name": "segment",
                                                "constraints": { 
                                                    "min": "2022-10-01", 
                                                    "max": "2022-12-31"
                                                }
                                            }
                                        }
                                    ]
                                }
    """