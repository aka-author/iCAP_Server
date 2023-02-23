# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  postgres.py                           (\(\
# Func:    Working with Postgres databases       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import psycopg2
import status, datatypes, controllers
import dbms_instances, db_instances, query_runners


class PostgresQueryRunner(query_runners.QueryRunner):

    def connect(self, db: db_instances.Db) -> query_runners.QueryRunner:

        status_code = status.OK

        try:
            self.connection = psycopg2.connect(\
                dbname=self.get_chief().get_access_param("host"),
                dbname=db.get_connection_param("database"),
                dbname=db.get_connection_param("user"),
                dbname=db.get_connection_param("password"))
        except:
            status_code = status.ERR_DB_CONNECTION_FAILED

        return status_code 


class Postgres(dbms_instances.DbmsInstance):

    def __init__(self, chief: controllers.Controller, access_params: Dict):

        super().__init__(chief, access_params)


    def sql_datatype_name(self, icap_datatype_name: str) -> str:

        dt_map = {
            datatypes.DTN_UUID:         "uuid", 
            datatypes.DTN_BOOLEAN:      "boolean",
            datatypes.DTN_NUMERIC:      "numeric",
            datatypes.DTN_BIGINT:       "bigint",
            datatypes.DTN_DOUBLE:       "double",
            datatypes.DTN_STRING:       "varchar",
            datatypes.DTN_STRLIST:      "varchar",
            datatypes.DTN_TIMESTAMP:    "timestamp",
            datatypes.DTN_TIMESTAMP_TZ: "timestamptz",
            datatypes.DTN_DATE:         "timestamp",
            datatypes.DTN_TIME:         "timestamp",
            datatypes.DTN_JSON:         "json"
        }

        return dt_map.get(icap_datatype_name, "varchar")


    def new_query_runner(self) -> query_runners.QueryRunner:

        return PostgresQueryRunner(self)


    