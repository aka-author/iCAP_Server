# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_insert.py                     (\(\
# Func:     Building INSERT queries           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import utils
import fields, dbms_instances, sql_queries


class IntoClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "INTO"

        self.varnames = []


    def set_varnames(self, varnames: List) -> 'ClauseInto':

        self.varnames = varnames

        return self
    

    def get_varnames(self) -> List:

        return self.varnames


    def get_varname_list(self) -> str:

        self.sql.list([self.sql.sql_varname(varname) for varname in self.get_varnames()])


    def assemble_snippet(self) -> str:

        return " ".join([self.get_clause_name(), 
                         self.get_qualified_table_name(), 
                         utils.pars(self.get_varname_list())])
                    

class ValuesClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "VALUES"


    def set_values(self, values: List) -> 'ClauseValues':

        self.values = values


    def get_values(self) -> List:

        return self.values


    def get_value_list(self) -> str:

        return self.sql.list([self.sql.typed_value(value) for value in self.get_values()])


    def assemble_snippet(self) -> str: 

        return " ".join([self.get_clause_name(), utils.pars(self.get_value_list())])


class Insert(sql_queries.Query):

    def __init__(self, chief: dbms_instances.Dbms, query_name: str=None):

        super().__init__(chief, "INSERT", query_name)


    def create_clauses(self) -> 'sql_queries.Query':

        self.add_clause(IntoClause(self))\
            .add_clause(ValuesClause(self))
        
        return self


    def INTO(self, db_scheme_name, table_name, *varnames) -> 'Insert':

        self.clauses["INTO"]\
            .set_table_name(table_name)\
            .set_db_scheme_name(db_scheme_name)\
            .set_varnames(varnames).turn_on()

        return self


    def VALUES(self, *values) -> 'Insert':

        self.clauses["VALUES"].set_values(values).turn_on()

        return self


    def build_of_field_manager(self, fm: fields.FieldManager, db_scheme_name: str=None) -> 'Insert':

        varnames = []
        values = []

        for varname in fm.get_varnames():
            if fm.get_field(varname).is_insertable():
                varnames.append(varname)
                values.append(fm.get_field_value(varname))

        self.INTO(db_scheme_name, fm.get_recordset_name(), *varnames)\
            .VALUES(*values)

        return self