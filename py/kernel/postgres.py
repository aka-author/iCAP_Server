# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  postgres.py                           (\(\
# Func:    Working with Postgres databases       (^.^)
# # ## ### ##### ######## ############# #####################

import psycopg2
import status, datatypes, bureaucrat, dbms, sqlbuilder
    

class PostgreSql(sqlbuilder.Sql):

    pass


class Postgres(dbms.Dbms):

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


    def new_sql(self, owner: bureaucrat.Bureaucrat) -> sqlbuilder.Sql:

        return PostgreSql(owner)


    def connect(self, connection_params) -> object:

        status_code = status.OK

        try:
            self.connection = psycopg2.connect(\
                dbname=connection_params["database"], 
                host=connection_params["host"], 
                user=connection_params["user"], 
                password=connection_params["password"])
        except:
            status_code = status.ERR_DB_CONNECTION_FAILED

        return status_code 