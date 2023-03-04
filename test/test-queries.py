import sys, datetime
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import fields, postgres, sql_insert, sql_update

def get_pet_Tuzik():

    return {"pet_name": "Tuzik", "species": "dog", "weight": 12}


fm = fields.FieldManager()\
        .add_field(fields.UuidField("uuid"))\
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

