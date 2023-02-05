
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import dbms, dtoms, fields


def check_pet_sql(fm, d):

    sql_pet_name_value = fm.code_field_value_for_sql("pet_name", d)
    print(sql_pet_name_value)

    sql_pet_name_typed_value = fm.code_typed_field_value_for_sql("pet_name", d)
    print(sql_pet_name_typed_value)

    sql_weight_value = fm.code_field_value_for_sql("weight", d)
    print(sql_weight_value)

    sql_weight_typed_value = fm.code_typed_field_value_for_sql("weight", d)
    print(sql_weight_typed_value)

    sql_date_of_birth_value = fm.code_field_value_for_sql("date_of_birth", d)
    print(sql_date_of_birth_value)

    sql_date_of_birth_typed_value = fm.code_typed_field_value_for_sql("date_of_birth", d)
    print(sql_date_of_birth_typed_value)



fm = fields.FieldManager(None)\
    .add_field(fields.UuidField("uuid"))\
    .add_field(fields.StringField("pet_name"))\
    .add_field(fields.StringField("species"))\
    .add_field(fields.BigintField("weight"))\
    .add_field(fields.DateField("date_of_birth"), "mandatory")\
    .reset_field_values()


count_fields = fm.count_fields()
print(count_fields)

fm.set_field_values({"pet_name": "Tuzik", "species": "dog", "weight": 12})

pet_name = fm.get_field_value("pet_name")
print(pet_name)

date_of_birth = fm.get_field_value("date_of_birth")
print(date_of_birth)

assert count_fields == 5 
assert pet_name == "Tuzik"

d = dbms.Dbms(None)

check_pet_sql(fm, d)


# Testing import from DTO

fm.reset_field_values()

dto_impl = dtoms.DtoMs(None)

fm.import_field_value_from_dto("pet_name", "Barsik", dto_impl)\
  .import_field_value_from_dto("species", "cat", dto_impl)\
  .import_field_value_from_dto("weight", 6, dto_impl)\
  .import_field_value_from_dto("date_of_birth", "2020-02-03", dto_impl)     

check_pet_sql(fm, d)



