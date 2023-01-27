# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  dbms.py                                 (\(\
# Func:    Providing support for certain CBMSs     (^.^)
# # ## ### ##### ######## ############# #####################

import utils, bureaucrat


class Dbms(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def varname2sql(self, varname):

        return varname.replace(".", "__").replace(" ", "_")        


    def get_sql_datatype_name(self, icap_datatype_name):

        dt_map = {
            "STRING":       "varchar",
            "BIGINT":       "bigint",
            "DOUBLE":       "numeric",
            "TIMESTAMP":    "timestamp",
            "TIMESTAMP_TZ": "timestamptz",
            "BOOLEAN":      "boolean",
            "JSON":         "json"
        }

        return utils.safeval(utils.safedic(dt_map, icap_datatype_name), "varchar")