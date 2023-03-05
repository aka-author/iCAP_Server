import sys, datetime
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import fields, postgres, sql_insert, sql_update, sql_select

def get_pet_Tuzik():

    return {"pet_name": "Tuzik", "species": "dog", "weight": 12}


fm = fields.FieldManager()\
        .add_field(fields.UuidField("uuid"), "autoins")\
        .add_field(fields.StringField("pet_name"))\
        .add_field(fields.StringField("species"))\
        .add_field(fields.BigintField("weight"))\
        .add_field(fields.DateField("date_of_birth"), "mandatory")\
        .reset_field_values().set_recordset_name("pets")


fm.set_field_values(get_pet_Tuzik())

dbms = postgres.Postgres(None, {})

q_insert = dbms.new_insert()
q_insert.build_of_field_manager(fm, "icap")
print(q_insert.get_snippet())

q_update = dbms.new_update()
q_update.build_of_field_manager(fm, "icap")
print(q_update.get_snippet())

q_select = dbms.new_select()\
    .FROM(("pets", "icap"),)\
    .INNER_JOIN(("cities", "icap"),)\
    .ON("{0}={1}", ("city_uuid", 0), ("uuid", 1))\
    .LEFT_JOIN(("countries", "icap"),)\
    .ON("{0}={1}", ("country_uuid", 1), ("uuid", 2))\
    .WHERE("{0}={1}", ("pet_name", 0), "Tuzik")\
    .SELECT_field(("pet_name", 0))\
    .SELECT_expression("k_losev", "1/{0}", ("weight", 0))\
    .SELECT_expression("today", "{0}", datetime.datetime.now())\
    .SELECT_field(("city_name", 1))\
    .SELECT_field(("country_name", 2))

print(q_select.get_snippet())

q_select_fm = dbms.new_select().build_of_field_manager(fm, \
            '{0}={1} AND {2} is null', ("pet_name", 0), "Murzik", ("is_deleted", 0))

print(q_select_fm.get_snippet())
