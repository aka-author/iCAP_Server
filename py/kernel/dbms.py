# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dbms.py                                     (\(\
# Func:    Achieving compatibility with certain DBMSs  (^.^)
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


    def sql_list(self, items):

        return ", ".join(items)


    def sql_typed_phrase(self, phrse, icap_datatype_name):

        return phrse + "::" + self.sql_datatype_name(icap_datatype_name)


    def sql_table_alias(self, table_alias):

        return table_alias + "." if table_alias is not None else ""


    def sql_varname(self, icap_varname, table_alias=None):

        return self.sql_table_alias(table_alias) + icap_varname.replace(".", "__").replace(" ", "_")


    def sql_typed_varname(self, icap_varname, icap_datatype_name, table_alias=None):

        return self.sql_typed_phrase(self.sql_varname(icap_varname, table_alias), icap_datatype_name)


    def sql_substitute_varnames(self, expr, varnames, table_alias=None):

        # {price}*{numner} -> t.price*t.number 

        expr_sv = expr

        for varname in varnames:
            varname_pattern = "{" + varname + "}"
            expr_sv = expr_sv.replace(varname_pattern, self.sql_varname(varname, table_alias))

        return expr_sv 


    def sql_value(self, raw_value_for_sql, icap_datatype_name):

        s_v = "null"

        if raw_value_for_sql is not None:
            sql_datatype_name = self.sql_datatype_name(icap_datatype_name)
            need_apos = ["uuid", "varchar", "timestamp", "timestamptz", "json"]
            s_v = utils.apos(raw_value_for_sql) if sql_datatype_name in need_apos else raw_value_for_sql

        return s_v
            

    def sql_typed_value(self, serialized_value, icap_datatype_name):

        return self.sql_typed_phrase(self.sql_value(serialized_value), icap_datatype_name)


    def sql_table_name(self, table_local_name, scheme_name=None):

        sql_tn = table_local_name

        if scheme_name is not None:
            sql_tn = scheme_name + "." + table_local_name

        return sql_tn 

