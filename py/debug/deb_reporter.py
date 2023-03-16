import os, sys
from io import StringIO 


def get_content_type():

    return "application/json"


def get_body():

    return """{
                "ver":          "2",
                "shop_name":    "basestat",
                "report_name":  "summaries",
                "payload": {
                    "scope": {
                        "conditions": [
                            {
                                "cond_name":    "langScope",
                                "varname":      "icap.cms.doc.localCode",
                                "range": {
                                    "datatype_name":    "string",
                                    "range_type_name":  "list",
                                    "values":           ["en", "es"]
                                }
                            },
                            {
                                "cond_name":    "timeScope",
                                "varname":      "accepted_at", 
                                "range": {
                                    "datatype_name":    "timestamp",
                                    "range_type_name":  "segment",
                                    "values": { 
                                        "min": "2023-01-01", 
                                        "max": "2023-12-31"
                                    }
                                }
                            }
                        ],
                        "expression": "langScope and timeScope"
                    },
                    "granularity": {
                        "dimensions": [
                            {
                                "varname": "accepted_at",
                                "groups": [
                                    {
                                        "group_name": "Q1",
                                        "range": {
                                            "datatype_name":    "timestamp",
                                            "range_type_Name":  "segment",
                                            "values": { 
                                                "min": "2023-01-01", 
                                                "max": "2022-03-31"
                                            }
                                        }
                                    },
                                    {
                                        "group_name": "Q2",
                                        "range": {
                                            "datatype_name":    "timestamp",
                                            "range_type_name":  "segment",
                                            "values": { 
                                                "min": "2023-04-01", 
                                                "max": "2022-06-30"
                                            }
                                        }
                                    },
                                    {
                                        "level_name": "Q3",
                                        "range": {
                                            "datatype_name":    "timestamp",
                                            "range_type_name":  "segment",
                                            "values": { 
                                                "min": "2023-07-01", 
                                                "max": "2022-09-30"
                                            }
                                        }
                                    },
                                    {
                                        "level_name": "Q4",
                                        "range": {
                                            "datatype_name":    "timestamp",
                                            "range_type_name":  "segment",
                                            "values": { 
                                                "min": "2023-10-01", 
                                                "max": "2022-12-31"
                                            }
                                        }
                                    }
                                ]
                            }    
                        ]
                    } 
                }
            }"""


def mock_cgi_input():

    os.environ["HTTP_COOKIE"] = "7c87a2ff-f8e9-4cdf-afaa-8c33ae7e6e5f"
    os.environ["CONTENT_TYPE"] = get_content_type()
    os.environ["CONTENT_LENGTH"] = str(len(get_body()))

    sys.stdin = StringIO(get_body())