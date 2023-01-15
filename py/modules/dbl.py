# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  dbl.py                                   (\(\
# Func:    Running SQL queries                      (^.^)
# # ## ### ##### ######## ############# ##################### 

import psycopg2
import status, bureaucrat, buildsql


class Dbl(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def new_select(self, query_name=None, scheme_name=None):

        return buildsql.Select(self, query_name, scheme_name)


    def new_union(self, query_name=None, scheme_name=None):

        return buildsql.Union(self, query_name, scheme_name)


    def new_insert(self, query_name, scheme_name=None):

        return buildsql.Insert(self, query_name, scheme_name)


    def run_script(self, script):

        try:
            db_cursor.execute(script.get_snippet())
        except:
            status_code = status.ERR_DB_QUERY_FAILED

        return status_code


    def run_query(self, query):

        self.run_script(buildsql.QueryScript(self).add_query(query))



    