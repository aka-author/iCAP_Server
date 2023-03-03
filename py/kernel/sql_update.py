# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_update.py                     (\(\
# Func:     Building UPDATE queries           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import dbms_instances, sql_queries


class UpdateClause(sql_queries.MototableClause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "UPDATE"
        self.set_headless_flag()


class SetClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "SET"


    def set_field_values(self, field_values: Dict) -> 'SetClause':

        self.field_values = field_values

        return self


    def setting(self, varname: str, value: any) -> str:

        return self.sql.eq(self.sql.sql_varname(varname), self.sql.typed_value(value))


    def assemble_snippet(self) -> str:

        settings = [self.setting(varname, value) for varname, value in field_values.items]

        return self.sql.list(settings)


class Update(sql_queries.Query):

    def __init__(self, chief: dbms_instances.Dbms, query_name: str=None):

        super().__init__(chief, "UPDATE", query_name)


    def create_clauses(self) -> 'sql_queries.Query':

        self.add_clause(UpdateClause(self))\
            .add_clause(SetClause(self))\
            .add_clause(sql_queries.WhereClause(self))
        
        return self


    def UPDATE(self, table_name, db_scheme_name=None) -> 'Update':

        self.clauses["UPDATE"]\
            .set_table_name(table_name)\
            .set_db_scheme_name(db_scheme_name).turn_on()

        return self


    def SET(self, field_values: Dict) -> 'Update':

        self.clauses["SET"].set_field_values(field_values).turn_on()

        return self
    

    def WHERE(self, expression: str, *operands) -> 'Update':

        self.clauses["WHERE"].set_expression(expression).set_operands(*operands).turn_on()

        return self


    def build_of_field_manager(self, fm, db_scheme_name: str=None) -> 'Update':

        field_values = []

        for varname in fm.get_field_names():
            if fm.get_field(varname).is_insertable():
                field_values[varname] = fm.get_field_value(varname)

        primary_key_name = self.sql.sql_varname(fm.get_primary_key_name())
        primary_key_value = self.sel.typed_value(fm.get_field_value(primary_key_name))

        self.UPDATE(db_scheme_name, fm.get_recordset_name())\
            .SET(*field_values)\
            .WHERE("{0}={1}", primary_key_name, primary_key_value)

        return self