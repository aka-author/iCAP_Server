# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  dbl.py                                   (\(\
# Func:    Running SQL queries                      (^.^)
# # ## ### ##### ######## ############# ##################### 

import psycopg2
import status, bureaucrat, buildsql


class DbConnector(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)
    
        self.db_connection = None
        self.connected_flag = False


    def get_connection_params(self):

        return cp


    def set_connected_flag(self, state=True):

        self.connected_flag = state

        return self


    def is_connected(self):

        return self.connected_flag


    def get_db_connection(self):

        return self.db_connection


    def connect_db(self):

        cp = self.get_connection_params()

        try:
            self.db_connection = \
                psycopg2.connect(dbname=cp["database"], host=cp["host"], \
                                 user=cp["user"], password=cp["password"])
            self.set_connected_flag()
        except:
            self.set_status_code(status.ERR_DB_CONNECTION_FAILED)

        return self 


    def execute_sql(self, sql_code):

        if not self.is_connected():
            self.connect_db()

        if self.isOK():

            db_cursor = self.get_db_connection().cursor()
            
            try:
                db_cursor.execute(sql_code)
            except:
                self.set_status_code(status.ERR_DB_QUERY_FAILED)

        return db_cursor


class Dbl(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.dbc = DbConnector(self)


    def new_select(self, query_name=None, scheme_name=None):

        return buildsql.Select(self, query_name, scheme_name)


    def new_union(self, query_name=None, scheme_name=None):

        return buildsql.Union(self, query_name, scheme_name)


    def new_insert(self, query_name, scheme_name=None):

        return buildsql.Insert(self, query_name, scheme_name)


    def run_script(self, script):

        db_cursor = self.dbc.execute_sql(script.get_snippet())

        if script.is_selective() and self.dbc.isOK():
            script.fill_output_ramtable(db_cursor.fetchall())

        return self


    def run_query(self, query):

        return self.run_script(buildsql.QueryScript(self).add_query(query))