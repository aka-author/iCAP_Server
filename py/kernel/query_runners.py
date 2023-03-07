# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  query_runners.py                           
# Func:    Connecting databases and running queries    (\(\
# Usage:   Create objects based on this class          (^.^)
# # ## ### ##### ######## ############# ##################### 

import status, workers
import dbms_instances, db_instances, sql_queries, sql_scripts, query_results


class QueryRunner(workers.Worker):

    def __init__(self, chief, db: db_instances.Db):

        super().__init__(chief)
    
        self.db = db

        self.connection = None
        self.connected_flag = False

        self.query_result = None


    def get_dbms(self) -> 'dbms_instances.Dbms':

        return self.get_chief()


    def set_connected_flag(self, state: bool=True) -> 'QueryRunner':

        self.connected_flag = state

        return self


    def is_connected(self) -> bool:

        return self.connected_flag


    def connect(self, db: db_instances.Db) -> 'QueryRunner':

        return self 


    def get_connection(self) -> object:

        return self.connection


    def execute_sql(self, sql_snippet: str) -> object:

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


    def execute_script(self, script: sql_scripts.Script) -> 'QueryRunner':

        cursor = self.execute_sql(script.get_snippet())

        sel_query = script.get_selective_query()

        fm = sel_query.get_field_manager()

        self.query_result = self.get_chief().new_result(sel_query, fm, cursor)

        return self


    def execute_query(self, query: sql_queries.Query) -> 'QueryRunner':

        script = self.get_chief().new_script(self)

        return self.execute_script(script.add_query(query))
    

    def commit(self) -> 'QueryRunner':

        if self.is_connected():
            self.get_connection().commit()

        return self


    def get_query_result(self) -> query_results.QueryResult:

        return self.query_result
    

    def close(self) -> 'QueryRunner':

        self.connection.close()

        return self