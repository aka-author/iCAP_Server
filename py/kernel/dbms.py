# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dbms.py                                      (\(\
# Func:    Accessing a database using a certain DBMS    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import status, fields, bureaucrat, sqlscripts, sqlqueries, sqlresults, sqlsnippets


class DbLayer(bureaucrat.Bureaucrat):

    def __init__(self, chief, connection_params: Dict):

        super().__init__(chief)
    
        self.connection_params = connection_params

        self.connection = None
        self.connected_flag = False

        self.results = []


    def get_connection_params(self) -> Dict:

        return self.connection_params


    def set_connected_flag(self, state: bool=True) -> 'DbLayer':

        self.connected_flag = state

        return self


    def is_connected(self) -> bool:

        return self.connected_flag


    def connect(self) -> object:

        self.set_connected_flag(self.get_chief().connect(self.get_connection_params()) == status.OK)

        return self 


    def get_connection(self) -> 'DbLayer':

        return self.connection


    def execute_sql(self, sql_snippet: str) -> 'DbLayer':

        cursor = None

        if not self.is_connected():
            self.connect()

        if self.isOK():

            cursor = self.get_connection().cursor()

            try:
                cursor.execute(sql_snippet)
            except:
                self.set_status_code(status.ERR_DB_QUERY_FAILED)

        return cursor


    def execute_script(self, script: sqlscripts.Script) -> 'DbLayer':

        cursor = self.execute_sql(script.sql.get_snippet())

        self.results.append(self.get_dbms().new_result(self, script.get_selective_query().fk, cursor))

        return self


    def execute_query(self, query: sqlqueries.Query) -> 'DbLayer':

        script = self.get_chief().new_script(self)

        return self.execute_script(script.add_query(query))
    

    def commit(self) -> 'DbLayer':

        if self.is_connected():
            self.get_connection().commit()

        return self


    def get_query_result(self) -> sqlresults.Result:

        return self.results[len(self.results) - 1]


class Dbms(bureaucrat.Bureaucrat):

    def __init__(self, chief: bureaucrat.Bureaucrat):

        super().__init__(chief)


    def get_dbms(self) -> 'Dbms':

        return self


    def connect(self, connection_params: dict) -> 'Dbms':

        return status.OK


    def new_dblayer(self) -> DbLayer:

        return DbLayer(self)


    def new_sql(self, owner: bureaucrat.Bureaucrat) -> sqlsnippets.Sql:

        return sqlsnippets.Sql(self, owner)


    def new_select(self, query_name: str=None) -> sqlqueries.Select:

        return sqlqueries.Select(self, query_name)


    def new_union(self, query_name: str=None) -> sqlqueries.Union:

        return sqlqueries.Union(self, query_name)


    def new_insert(self, query_name: str=None) -> sqlqueries.Insert:

        return sqlqueries.Insert(self, query_name)


    def new_update(self, query_name: str=None) -> sqlqueries.Update:

        return sqlqueries.Update(self, query_name)


    def new_script(self, script_name: str="noname") -> sqlscripts.Script:

        return sqlscripts.Script(self, script_name)


    def new_result(self, dbl: DbLayer, fk: fields.FieldKeeper, cursor) -> sqlresults.Result:

        return sqlresults.Result(dbl, fk, cursor)
