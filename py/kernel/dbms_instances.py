# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dbms_instances.py                            (\(\
# Func:    Creating and organizing DBMS-related objects (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, controllers
import db_instances, db_objects, query_runners, query_results 
import sql_workers, sql_scripts, sql_queries, sql_builders
import sql_insert, sql_update, sql_select


class Dbms(workers.Worker):

    def __init__(self, chief: controllers.Controller, access_params: Dict):

        self.access_params = access_params

        super().__init__(chief)


    def get_access_param(self, param_name: str) -> str:

        return self.access_params.get(param_name)


    def get_dbms(self) -> 'Dbms':

        return self


    def new_sql_builder(self, owner: sql_workers.SqlWorker) -> sql_builders.SqlBuilder:

        return sql_builders.SqlBuilder(owner)


    def new_table(self, scheme: db_objects.Scheme, table_name: str) -> db_objects.Table:

        return db_objects.Table(scheme, table_name)


    def new_scheme(self, db: db_instances.Db, scheme_name: str) -> db_objects.Scheme:

        return db_objects.Scheme(db, scheme_name)
    

    def new_db(self) -> db_instances.Db:

        return db_instances.Db(self)


    def new_subqueries(self, chief_query: sql_queries.Query) -> sql_queries.Subqueries:

        return sql_queries.Subqueries(chief_query)


    def new_select(self, query_name: str=None) -> sql_select.Select:

        return sql_queries.Select(self, query_name)


    # def new_union(self, query_name: str=None) -> sql_queries.Union:
    #
    #    return sql_queries.Union(self, query_name)


    def new_insert(self, query_name: str=None) -> sql_insert.Insert:

        return sql_insert.Insert(self, query_name)


    def new_update(self, query_name: str=None) -> sql_update.Update:

        return sql_update.Update(self, query_name)


    def new_script(self, script_name: str="noname") -> sql_scripts.Script:

        return sql_scripts.Script(self, script_name)


    def new_result(self, qres, fk: fields.FieldKeeper, cursor) -> query_results.QueryResult:

        return query_results.Result(qres, fk, cursor)
    

    def new_query_runner(self) -> 'query_runners.QueryRunner':

        return query_runners.QueryRunner(self)