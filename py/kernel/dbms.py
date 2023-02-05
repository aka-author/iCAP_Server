# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dbms.py                                      (\(\
# Func:    Achieving compatibility with a certain DBMS  (^.^)
# # ## ### ##### ######## ############# #####################

import utils, datatypes, bureaucrat


class Dbms(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def sql_datatype_name(self, icap_datatype_name):

        dt_map = {
            datatypes.DTN_UUID:         "uuid", 
            datatypes.DTN_BOOLEAN:      "boolean",
            datatypes.DTN_NUMERIC:      "numeric",
            datatypes.DTN_BIGINT:       "bigint",
            datatypes.DTN_DOUBLE:       "double",
            datatypes.DTN_STRING:       "varchar",
            datatypes.DTN_STRLIST:      "varchar",
            datatypes.DTN_TIMESTAMP:    "timestamp",
            datatypes.DTN_TIMESTAMP_TZ: "timestamptz",
            datatypes.DTN_DATE:         "timestamp",
            datatypes.DTN_JSON:         "json"
        }

        return utils.safeval(utils.safedic(dt_map, icap_datatype_name), "varchar")


    def get_format_for_datatype(self, datatype_name):

        fmt_map = {
            datatypes.DTN_TIMESTAMP:    datatypes.get_default_timestamp_format(),
            datatypes.DTN_TIMESTAMP_TZ: datatypes.get_default_timestamp_tz_format(),
            datatypes.DTN_DATE:         datatypes.get_default_date_format()
        }

        return utils.safedic(fmt_map, datatype_name)



    def sql_typed_phrase(self, phrse, icap_datatype_name):

        return phrse + "::" + self.sql_datatype_name(icap_datatype_name)


    def sql_varname(self, icap_varname):

        return icap_varname.replace(".", "__").replace(" ", "_")


    def sql_typed_varname(self, icap_varname, icap_datatype_name):

        return self.sql_typed_phrase(self.sql_varname(icap_varname), icap_datatype_name)


    def sql_value(self, raw_value_for_sql, icap_datatype_name):

        s_v = "null"

        if raw_value_for_sql is not None:
            sql_datatype_name = self.sql_datatype_name(icap_datatype_name)
            need_apos = ["uuid", "varchar", "timestamp", "timestamptz", "json"]
            s_v = utils.apos(raw_value_for_sql) if sql_datatype_name in need_apos else raw_value_for_sql

        return s_v
            

    def sql_typed_value(self, serialized_value, icap_datatype_name):

        return self.sql_typed_phrase(self.sql_value(serialized_value), icap_datatype_name)