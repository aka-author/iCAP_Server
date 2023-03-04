# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sql_builders.py                      (\(\
# Func:    Assembling SQL queries               (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
from datetime import datetime
import utils, datatypes, fields, workers, sql_workers


class SqlBuilder(workers.Worker):

    def __init__(self, chief):

        super().__init__(chief)


    # Data types

    def icap2sql_datatype_name(self, icap_datatype_name: str) -> str:

        # Code depends on a DBMS

        return ""
    

    def sql_datatype_name(self, native_value: any) -> str:

        icap_datatype_name = datatypes.detect_native_value_datatype(native_value)

        return self.icap2sql_datatype_name(icap_datatype_name)


    # Field names

    def sql_varname(self, icap_varname: str) -> str:

        return icap_varname.replace(".", "__").replace(" ", "_")
    

    def qualified_varname(self, varname, table_alias=None) -> str:

        return (table_alias + "." if table_alias is not None else "") + varname
    

    def fieldref_as_name(self, field_info: Dict, as_name: str=None) -> str:

        # Field info:
        #    {"recordset": "rabbits", "varname": "pet_name"}

        alias = self.get_chief().get_group_alias_by_field_info(field_info)
        prefix = alias + "." if alias is not None else ""

        postfix = (" AS " + as_name) if as_name is not None else ""

        return prefix + field_info.get("varname") + postfix
    

    def expr_as_name(self, expr: str, field_infos: List, as_name: str=None) -> str:

        # Samples of an expression are:
        #    "count({0})"
        #    "({0} + {1})*{3}"

        return ""


    # Base expresions

    def typed_expr(self, expr: str, sql_datatype_name: str) -> str:

        return expr + "::" + sql_datatype_name
    

    def biop(self, op_l: str, op: str, op_r: str) -> str:

        return " ".join([op_l, op, op_r])
    

    def eq(self, op_l: str, op_r: str) -> str:

        return self.biop(op_l, "=", op_r)
    

    def as_subst(self, to_be_substituted: str, substitute: str) -> str:

        return self.biop(to_be_substituted, "AS", substitute)
    

    def list(self, list_items: List) -> str:

        return ", ".join(list_items)
    

    def list_in_column(self, list_items: List) -> str:

        return ",\n".join(list_items)
 

    # Field values

    def get_format_for_datatype(self, icap_datatype_name: str) -> str:

        return datatypes.get_format(icap_datatype_name)


    def serialized_value(self, native_value: any) -> str:

        if native_value is None:
            s_v = "null"
        else:
            icap_datatype_name = datatypes.detect_native_value_datatype(native_value)
            format = self.get_format_for_datatype(icap_datatype_name)
            if icap_datatype_name == datatypes.DTN_UUID:
                s_v = str(native_value)
            elif icap_datatype_name == datatypes.DTN_BOOLEAN:
                s_v = str(native_value)
            elif datatypes.is_numeric_datatype(icap_datatype_name):
                s_v = str(native_value) 
            elif icap_datatype_name == datatypes.DTN_STRING:
                s_v = native_value
            elif datatypes.is_datetime_datatype(icap_datatype_name):
                s_v = datetime.strftime(native_value, format)
            else:
                s_v = str(native_value)

        return s_v
    

    def looks_like_string(self, dbms_datatype_name: str) -> bool:

        return True
    

    def is_sql_duck_typed(self, native_value: any) -> bool:

        icap_datatype_name = datatypes.detect_native_value_datatype(native_value)
        
        sql_ducks = (datatypes.DTN_BOOLEAN, 
                     datatypes.DTN_BIGINT, 
                     datatypes.DTN_DOUBLE, 
                     datatypes.DTN_STRING)

        return icap_datatype_name in sql_ducks
    

    def sqlized_value(self, native_value: any) -> str:

        sql_datatype_name = self.sql_datatype_name(native_value)
        ser_val = self.serialized_value(native_value)

        return utils.apos(ser_val) if self.looks_like_string(sql_datatype_name) else ser_val
    

    def typed_value(self, native_value: any, options: str="duck_type") -> str:

        sqlized_value = self.sqlized_value(native_value) 
        db_datatype_name = self.sql_datatype_name(native_value)

        typed_value = sqlized_value

        if (not self.is_sql_duck_typed(native_value)) or ("explicit_type" in options):
            typed_value += "::" + db_datatype_name

        return typed_value
    

    def typed_value_as_name(self, value_info: Dict, options: str="duck_type") -> str:

        # value_info = {"value": 12345, "as": "number_of_arnocles"}

        typed_value = self.typed_value(value_info.get("value"), options)
        field_name =  value_info.get("as", utils.unique_name("f"))

        return typed_value + " AS " + field_name


    # Operands

    def operand(self, operand: any) -> str:

        if isinstance(operand, tuple):
            field_group_alias = None
            if len(operand) > 1:
                if isinstance(operand[1], int):
                    field_group_alias = self.get_field_group_alias_by_index(operand[1])
                elif isinstance(operand[1], str):
                    field_group_alias = operand[1]                    
            actual_operand = self.qualified_varname(operand[0], field_group_alias)
        else:
            actual_operand = self.typed_value(operand)

        return actual_operand


    # Tables

    def qualified_table_name(self, table_name: str, scheme_name: str=None) -> str:

        return (scheme_name + "." if scheme_name is not None else "") + table_name

