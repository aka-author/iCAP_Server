# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_update.py                     (\(\
# Func:     Building UPDATE queries           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import dbms_instances, sql_queries


class UpdateClause(sql_queries.MonotableClause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "UPDATE"
        self.set_headless_flag()


    def assemble_snippet(self) -> str:
        
        return self.get_qualified_table_name() 


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

        settings = [self.setting(varname, value) for varname, value in self.field_values.items()]

        return self.sql.list(settings)


class Update(sql_queries.Query):

    def __init__(self, chief, query_name: str=None):

        super().__init__(chief, "UPDATE", query_name)


    def create_clauses(self) -> 'sql_queries.Query':

        self.add_clause(UpdateClause(self))\
            .add_clause(SetClause(self))\
            .add_clause(sql_queries.WhereClause(self))
        
        return self


    def UPDATE(self, table_name, db_scheme_name=None) -> 'Update':

        self.clauses_by_names["UPDATE"]\
            .set_table_name(table_name)\
            .set_db_scheme_name(db_scheme_name).turn_on()

        return self


    def SET(self, field_values: Dict) -> 'Update':

        self.clauses_by_names["SET"].set_field_values(field_values).turn_on()

        return self
    

    def WHERE(self, expression: str, *operands) -> 'Update':

        self.clauses_by_names["WHERE"].set_expression(expression).add_operands(*operands).turn_on()

        return self


    def build_of_field_manager(self, fm, db_scheme_name: str=None) -> 'Update':

        field_values = {}

        for varname in fm.get_varnames():
            if fm.is_insertable(varname):
                field_values[varname] = fm.get_field_value(varname)

        surrogate_key_name = fm.get_surrogate_key_name()

        if surrogate_key_name is not None:
            self.UPDATE(fm.get_recordset_name(), db_scheme_name)\
                .SET(field_values)\
                .WHERE("{0} = {1}", 
                       (surrogate_key_name, None), 
                       fm.get_field_value(surrogate_key_name))

        return self