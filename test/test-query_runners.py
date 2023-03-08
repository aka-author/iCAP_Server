import sys, datetime
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import fields, postgres, db_instances, sql_insert, sql_update, sql_select


fm = fields.FieldManager()\
        .add_field(fields.UuidField("uuid"), "autoins")\
        .add_field(fields.StringField("username"))\
        .add_field(fields.StringField("password_hash"))\
        .add_field(fields.BooleanField("auth_required"))\
        .add_field(fields.TimestampField("created_at"), "mandatory")\
        .reset_field_values()

dbms = postgres.Postgres(None, {"host": "89.108.102.59"})

db_connection_params = {
   "database": "Intuillion",
   "user": "postgres",
   "password": "My:s3Cr3t/"
}

db = dbms.new_db(db_connection_params)

query_runner = dbms.new_query_runner().set_db(db)

query_runner.connect()

load_query = dbms.new_select()\
    .build_of_field_manager(fm, "users", "icap", "{0}={1}", ("username",0), "ditatoo")

print(load_query.get_snippet())

query_runner.execute_query(load_query).get_query_result().fetch_one()
print(fm.field_values)

rt = query_runner.execute_query(load_query).get_query_result().dump()
print(rt)




