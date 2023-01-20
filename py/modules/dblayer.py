# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  dbl.py                                     (\(\
# Func:    Connecting a database and running queries  (^.^)
# # ## ### ##### ######## ############# ##################### 

import psycopg2
import status, bureaucrat, buildsql


class DbConnector(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)
    
        self.connection = None
        self.connected_flag = False


    def get_connection_params(self):

        return self.get_cfg().get_db_connection_params()


    def set_connected_flag(self, state=True):

        self.connected_flag = state

        return self


    def is_connected(self):

        return self.connected_flag


    def get_connection(self):

        return self.connection


    def connect(self):

        cp = self.get_connection_params()

        try:
            self.connection = \
                psycopg2.connect(dbname=cp["database"], host=cp["host"], \
                                 user=cp["user"], password=cp["password"])
            self.set_connected_flag()
        except:
            self.set_status_code(status.ERR_DB_CONNECTION_FAILED)

        return self 


    def execute_sql(self, sql_code):

        cursor = None

        if not self.is_connected():
            self.connect()

        if self.isOK():

            cursor = self.get_connection().cursor()

            try:
                cursor.execute(sql_code)
            except:
                self.set_status_code(status.ERR_DB_QUERY_FAILED)

        return cursor

    
    def commit(self):

        self.connection.commit()

        return self


class Dbl(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.dbc = DbConnector(self)


    def new_select(self, query_name=None, scheme_name=None):

        return buildsql.Select(self, query_name, scheme_name)


    def new_union(self, query_name=None, scheme_name=None):

        return buildsql.Union(self, query_name, scheme_name)


    def new_insert(self, query_name=None, scheme_name=None):

        return buildsql.Insert(self, query_name, scheme_name)


    def new_script(self, script_name="noname", scheme_name=None):

        return buildsql.Script(self, script_name, scheme_name)


    def is_query(self, query_or_script):

        return query_or_script.is_query()


    def execute(self, exec_me):
        
        script = buildsql.Script(self).add_query(exec_me) if exec_me.is_query() else exec_me
        
        db_cursor = self.dbc.execute_sql(script.get_snippet())
        
        if script.is_selective() and self.dbc.isOK():
            script.get_selective_query().fill_output_ramtable(db_cursor.fetchall())

        return self


    def commit(self):

        self.dbc.commit()

        return self