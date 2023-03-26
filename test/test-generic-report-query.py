
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import postgres, dtos 
import grq_scopes, grq_granularity, grq_report_query


class AppMoke():

    def __init__(self):

        pass

    
    def get_app(self):

        return self
    

def get_test_report_query():

    return  {
                "scope": {
                    "conditions": [
                        {
                            "condition_name": "langScope",
                            "varname": "icap.cms.doc.localCode",
                            "range": {
                                "datatype_name": "string",
                                "range_type_name": "set",
                                "constraints": {
                                    "members": ["en", "es"]
                                }
                            }
                        },
                        {
                            "condition_name": "timeScope",
                            "varname": "accepted_at", 
                            "range": {
                                "datatype_name": "timestamp",
                                "range_type_name": "segment",
                                "constraints": { 
                                    "min": "2022-01-01", 
                                    "max": "2022-12-31"
                                }
                            }
                        }
                    ],
                    "expression": "langScope and timeScope"
                },
                "granularity": {
                    "dimensions": [
                        {
                            "varname": "test_var"
                        },
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
                                    "group_value": "Q3",
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
                                    "group_value": "Q4",
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
                    ]
                }
            }


app = AppMoke()


postgres_instance = postgres.Postgres(app, {})
sql_builder = postgres_instance.new_sql_builder(None)

report_query = grq_report_query.ReportQuery(app)\
    .import_dto(dtos.Dto(get_test_report_query()).repair_datatypes())

print("Scope :", report_query.scope)
print("Granularity: ", report_query.granularity.dimensions[1].groups)