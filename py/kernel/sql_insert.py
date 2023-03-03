
from typing import List
import utils
import fields, dbms_instances, sql_queries


class ClauseInto(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "INTO"

        self.db_scheme_name = None
        self.table_name = None
        self.varnames = []


    def set_db_scheme_name(self, db_scheme_name: str) -> 'ClauseInto':

        self.db_scheme_name = db_scheme_name

        return self
    
    def get_db_scheme_name(self) -> str: 

        return self.db_scheme_name
    

    def set_table_name(self, table_name: str) -> 'ClauseInto':

        self.table_name = table_name

        return self
    

    def get_table_name(self) -> str: 

        return self.table_name 
    

    def set_varnames(self, varnames: List) -> 'ClauseInto':

        self.varnames = varnames

        return self
    

    def get_varnames(self) -> List:

        return self.varnames


    def get_qualified_table_name(self) -> str:

        return self.sql.qualified_table_name(self.get_table_name(), self.get_db_scheme_name())


    def get_varname_list(self) -> str:

        self.sql.list([self.sql.sql_varname(varname) for varname in self.get_varnames()])


    def get_snippet(self) -> str:

        return " ".join([self.get_clause_name(), 
                         self.sql.get_qualified_table_name(), 
                         utils.pars(self.get_varname_list())])
                    

class ClauseValues(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "VALUES"


    def set_values(self, values: List) -> 'ClauseValues':

        self.values = values


    def get_values(self) -> List:

        return self.values


    def get_value_list(self) -> str:

        return self.sql.list([self.sql.typed_value(value) for value in self.get_values()])


    def get_snippet(self) -> str: 

        return " ".join([self.get_clause_name(), utils.pars(self.get_value_list())])


class Insert(sql_queries.Query):

    def __init__(self, chief: dbms_instances.Dbms, query_name: str=None):

        super().__init__(chief, "INSERT", query_name)

    def create_clauses(self) -> 'sql_queries.Query':

        self.add_clause(ClauseInto(self))\
            .add_clause(ClauseValues(self))
        
        return self


    def INTO(self, db_scheme_name, table_name, *varnames) -> 'Insert':

        self.clauses["INTO"]\
            .set_table_name(table_name)\
            .set_db_scheme_name(db_scheme_name)\
            .set_varnames(varnames)

        return self


    def VALUES(self, *values) -> 'Insert':

        self.clauses["VALUES"].set_values(values)

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