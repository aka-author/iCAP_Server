# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  postgres.py                           (\(\
# Func:    Working with Postgres databases       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import psycopg2
from datetime import datetime
import utils, status, datatypes, controllers
import dbms_instances, db_instances, query_runners 
import sql_workers, sql_builders, sql_queries


class PostgresSqlBuilder(sql_builders.SqlBuilder):

    def __init__(self, owner: sql_workers.SqlWorker):
        
        super().__init__(owner)


    def native2sql_datatype_name(self, native_datatype_name: str) -> str:

        dt_map = {
            datatypes.DTN_UUID:         "uuid", 
            datatypes.DTN_BOOLEAN:      "boolean",
            datatypes.DTN_NUMERIC:      "numeric",
            datatypes.DTN_BIGINT:       "bigint",
            datatypes.DTN_DOUBLE:       "double",
            datatypes.DTN_STRING:       "varchar",
            datatypes.DTN_TIMESTAMP:    "timestamp",
            datatypes.DTN_TIMESTAMP_TZ: "timestamptz",
            datatypes.DTN_DATE:         "timestamp",
            datatypes.DTN_TIME:         "timestamp",
            datatypes.DTN_JSON:         "json"
        }

        return dt_map.get(native_datatype_name, "varchar")


    def looks_like_string(self, dbms_datatype_name: str) -> bool:

        dont_require_apos = ("boolean", "numeric", "bigint", "double")

        return dbms_datatype_name not in dont_require_apos
    

    def is_sql_duck_typed(self, native_value: any) -> bool:

        icap_datatype_name = datatypes.detect_native_value_datatype(native_value)
        
        sql_ducks = (datatypes.DTN_BOOLEAN, 
                     datatypes.DTN_BIGINT, 
                     datatypes.DTN_DOUBLE, 
                     datatypes.DTN_STRING)

        return icap_datatype_name in sql_ducks
    

    def repair_value(self, raw_value, native_datatype_name) -> any:

        if isinstance(raw_value, str):
            if native_datatype_name == datatypes.DTN_UUID:
                native_value = utils.str2uuid(raw_value)
            elif datatypes.is_datetime_datatype(native_datatype_name):
                format = self.get_format_for_datatype(native_datatype_name)
                native_value = utils.str2timestamp(raw_value, format)
            else:
                native_value = raw_value
        else:
            native_value = raw_value

        return native_value


class PostgresSubqueries(sql_queries.Subqueries):
     
    def get_subquery_def(self, query: sql_queries.Query) -> str:

        return self.sql.AS(query.get_query_name(), utils.pars(query.get_snippet()))
     

    def get_snippet(self) -> str:
        
        if len(self.subqueries) > 0:
            defs = [self.get_subquery_def(self.subqueries[sq_name]) for sq_name in self.subqueries]
            return "WITH\n" + self.sql.list_in_column(defs)  + "\n"
        else:
            return ""
        

class PostgresQueryRunner(query_runners.QueryRunner):

    def connect(self) -> query_runners.QueryRunner:

        db = self.get_db()

        status_code = status.OK
        
        try:
            self.connection = psycopg2.connect(\
                host=self.get_chief().get_access_param("host"),
                dbname=db.get_connection_param("database"),
                user=db.get_connection_param("user"),
                password=db.get_connection_param("password"))
            self.set_connected_flag()
        except:
            status_code = status.ERR_DB_CONNECTION_FAILED

        return status_code 


class Postgres(dbms_instances.Dbms):

    def __init__(self, chief: controllers.Controller, access_params: Dict):

        super().__init__(chief, access_params)


    def new_sql_builder(self, owner: sql_workers.SqlWorker) -> sql_builders.SqlBuilder:
        
        return PostgresSqlBuilder(owner)


    def new_subqueries(self, chief_query: sql_queries.Query) -> sql_queries.Subqueries:

        return PostgresSubqueries(chief_query)


    def new_query_runner(self, db: db_instances.Db=None) -> query_runners.QueryRunner:

        return PostgresQueryRunner(self, db)    