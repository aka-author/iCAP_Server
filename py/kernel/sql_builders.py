# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sql_builders.py                           (\(\
# Func:    Assembling primitive SQL code snippets    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List, Tuple
from datetime import datetime
import utils, datatypes, workers, sql_workers, sql_queries


class SqlBuilder(workers.Worker):

    def __init__(self, chief: sql_workers.SqlWorker):

        super().__init__(chief)


    def get_query(self) -> sql_queries.Query:

        return self.get_chief().get_query()


    # Escaping and concating strings

    def esc(self, s):

        return s.replace("'", "''")
    

    def typed(self, expr: str, sql_datatype_name: str) -> str:

        return expr + "::" + sql_datatype_name
    

    def biop(self, operand_left: str, operator: str, operand_right: str) -> str:

        return " ".join([operand_left, operator, operand_right])
    

    def eq(self, operand_left: str, operand_right: str) -> str:

        return self.biop(operand_left, "=", operand_right)
    

    def AS(self, substitutee: str, substitutor: str) -> str:

        return utils.infix(substitutee, utils.wspad("AS"), substitutor)
    

    def list(self, list_items: List, separ: str=", ") -> str:

        return separ.join(list_items)
    

    def column_list(self, list_items: List, separ: str=",\n") -> str:

        return self.list(list_items, separ)


    # Detecting and mapping data types of values

    def native2sql_datatype_name(self, native_datatype_name: str) -> str:

        # Code depends on a DBMS

        return ""
    

    def sql_datatype_name(self, native_value: any) -> str:

        native_datatype_name = datatypes.detect_native_value_datatype(native_value)

        return self.native2sql_datatype_name(native_datatype_name)


    # Formatting field names

    def sql_varname(self, native_varname: str) -> str:

        return native_varname.replace(".", "__").replace(" ", "_")
    

    def qualified_varname(self, varname, table_alias=None) -> str:

        return utils.prefix(table_alias, ".", self.sql_varname(varname))


    # Formatting values

    def get_format_for_datatype(self, native_datatype_name: str) -> str:

        return datatypes.get_format(native_datatype_name)


    def serialized_value(self, native_value: any) -> str:

        if native_value is None:
            s_v = "null"
        else:
            native_datatype_name = datatypes.detect_native_value_datatype(native_value)
            format = self.get_format_for_datatype(native_datatype_name)
            if native_datatype_name == datatypes.DTN_UUID:
                s_v = str(native_value)
            elif native_datatype_name == datatypes.DTN_BOOLEAN:
                s_v = str(native_value)
            elif datatypes.is_numeric_datatype(native_datatype_name):
                s_v = str(native_value) 
            elif native_datatype_name == datatypes.DTN_STRING:
                s_v = native_value
            elif datatypes.is_datetime_datatype(native_datatype_name):
                s_v = datetime.strftime(native_value, format)
            else:
                s_v = str(native_value)

        return s_v
    

    def looks_like_string(self, dbms_datatype_name: str) -> bool:

        # Should we put a value into apostrophes in SQL queries?
        # It depends on a particular DBMS.

        return True
    

    def is_sql_duck_typed(self, native_value: any) -> bool:

        # Should we provide an explicit data type specification
        # for a value in SQL queries?
        # It depends on a particular DBMS.

        return False
    

    def repair_value(self, raw_value, native_datatype_name) -> any:

        return raw_value
    

    def sqlized_value(self, native_value: any) -> str:

        if native_value is not None:
            sql_datatype_name = self.sql_datatype_name(native_value)
            ser_val = self.serialized_value(native_value)
            return utils.apos(self.esc(ser_val)) if self.looks_like_string(sql_datatype_name) else ser_val
        else:
            return "null"
    

    def typed_value(self, native_value: any, options: str="duck_type") -> str:

        sqlized_value = self.sqlized_value(native_value) 
        db_datatype_name = self.sql_datatype_name(native_value)

        typed_value = sqlized_value

        if ((not self.is_sql_duck_typed(native_value)) or ("explicit_type" in options)) and (native_value is not None):
            typed_value += "::" + db_datatype_name 

        return typed_value


    # Formatting more complex expressions and operands

    def op_name(self, op: Tuple) -> str:

        return op[0]
    

    def op_alias(self, op: Tuple) -> str:

        return op[1] if len(op) > 1 else None
    

    def op_datatype_name(self, op: Tuple) -> str:

        return op[2] if len(op) > 2 else None
    

    def op_is_field(self, op: any) -> bool:

        return isinstance(op, tuple)


    def recordset_alias(self, op: Tuple) -> str:

        op_alias = self.op_alias(op)
        is_idx = isinstance(op_alias, int)

        return self.get_query().get_src_recordset_alias_by_index(op_alias) if is_idx else op_alias
        

    def typed_expression(self, expr: str, native_datatype_name: str) -> str:
    
        if native_datatype_name is not None:
            dbms_datatype_name = self.native2sql_datatype_name(native_datatype_name)
            return self.typed(expr, dbms_datatype_name)
        else:
            return expr


    def field_operand(self, op: Tuple) -> str:
                            
        qualified = self.qualified_varname(self.op_name(op), self.recordset_alias(op))
        
        return self.typed_expression(qualified, self.op_datatype_name(op))


    def value_operand(self, op: any) -> str:

        return self.typed_value(op)


    def operand(self, op: any) -> str:

        return self.field_operand(op) if self.op_is_field(op) else self.value_operand(op)


    # Tables

    def qualified_table_name(self, table_name: str, db_scheme_name: str=None) -> str:

        return utils.prefix(db_scheme_name, ".", table_name)
    

    # CASE

    def case(self, *cases) -> str:

        with_clauses = []
        for case in cases:
            with_clauses.append("WHEN " + case[0] + " THEN " + case[1])

        return "CASE " + " ".join(with_clauses)  + " END"


