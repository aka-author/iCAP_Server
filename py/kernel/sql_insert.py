# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_insert.py                     (\(\
# Func:     Building INSERT queries           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import utils
import fields, dbms_instances, sql_queries, sql_select


class IntoClause(sql_queries.MonotableClause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "INTO"

        self.varnames = []


    def set_varnames(self, varnames: List) -> 'IntoClause':

        self.varnames = varnames

        return self
    

    def get_varnames(self) -> List:

        return self.varnames


    def assemble_varname_list(self) -> str:

        return self.sql.list([self.sql.sql_varname(varname) for varname in self.get_varnames()])


    def assemble_snippet(self) -> str:

        return " ".join([self.get_qualified_table_name(), 
                         utils.pars(self.assemble_varname_list())])
                    

class ValuesClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "VALUES"


    def set_values(self, values: List) -> 'ValuesClause':

        self.values = values

        return self


    def get_values(self) -> List:

        return self.values


    def get_value_list(self) -> str:

        return self.sql.list([self.sql.typed_value(value) for value in self.get_values()])


    def assemble_snippet(self) -> str: 

        return utils.pars(self.get_value_list())


class Insert(sql_queries.Query):

    def __init__(self, chief: 'dbms_instances.Dbms', query_name: str=None):

        super().__init__(chief, "INSERT", query_name)


    def create_clauses(self) -> 'sql_queries.Query':

        self.add_clause(IntoClause(self))\
            .add_clause(ValuesClause(self))\
            .add_clause(sql_select.SelectClause(self).set_headless_flag(False))\
            .add_clause(sql_select.FromClause(self))
        
        return self


    def INTO(self, table_name, db_scheme_name, *varnames) -> 'Insert':

        self.clauses_by_names["INTO"]\
            .set_table_name(table_name)\
            .set_db_scheme_name(db_scheme_name)\
            .set_varnames(varnames).turn_on()

        return self


    def VALUES(self, *values) -> 'Insert':

        self.clauses_by_names["VALUES"].set_values(values).turn_on()

        return self
    

    def get_FROM(self) -> sql_select.FromClause:

        return self.clauses_by_names["FROM"]
    

    def count_src_recordsets(self) -> int:

        return len(self.get_FROM().src_recordsets)
    

    def get_next_alias(self, alias: str) -> str:

        return utils.safeval(alias, "t" + str(self.count_src_recordsets()))
    

    def FROM(self, recordset: tuple, alias: str=None) -> 'Insert':

        self.get_FROM().add_src_recordset(\
            None,
            recordset[0], recordset[1] if len(recordset) > 1 else None, 
            self.get_next_alias(alias)).turn_on()        
            
        return self
    

    def get_SELECT(self) -> sql_select.SelectClause:

        return self.clauses_by_names["SELECT"]


    def SELECT_field(self, field_def, alias: str=None) -> 'Select':
        
        self.get_SELECT().add_field(alias, "{0}", *[field_def]).turn_on()
        
        return self


    def SELECT_expression(self, alias: str, expr: str, *operands) -> 'Select':

        self.get_SELECT().add_field(alias, expr, *operands).turn_on()
        
        return self


    def build_of_field_manager(self, fm: fields.FieldManager, db_table_name: str, db_scheme_name: str=None) -> 'Insert':

        varnames = []
        values = []

        for varname, native_value in fm.get_insertable_field_values().items():
            varnames.append(varname)
            values.append(native_value)

        self.INTO(db_table_name, db_scheme_name, *varnames)\
            .VALUES(*values)

        return self