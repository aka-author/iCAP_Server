
import sys, datetime
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import fields


def get_pet_Tuzik():

    return {"pet_name": "Tuzik", "species": "dog", "weight": 12}


def get_pet_Barsik():

    return {"pet_name": "Barsik", "species": "cat", "weight": 5}


def check_fm(fm):

    recordset_name = fm.get_recordset_name()
    print(recordset_name)
    assert recordset_name == "pets"

    count_fields = fm.count_fields()    
    print(count_fields)
    assert count_fields == 5
    

def check_pet(fm, pet):

    str_pet_name_value = fm.get_serialized_field_value("pet_name")
    print(str_pet_name_value)
    assert str_pet_name_value == pet["pet_name"]

    str_pet_species = fm.get_serialized_field_value("species")
    print(str_pet_species)
    assert str_pet_species == pet["species"]

    str_pet_weight = fm.get_serialized_field_value("weight")
    print(str_pet_weight)
    assert str_pet_weight == str(pet['weight'])

    str_pet_name_value = fm.get_serialized_field_value("date_of_birth")
    print(str_pet_name_value)

def check_module():

    fm = fields.FieldManager()\
        .add_field(fields.UuidField("uuid"))\
        .add_field(fields.StringField("pet_name"))\
        .add_field(fields.StringField("species"))\
        .add_field(fields.BigintField("weight"))\
        .add_field(fields.DateField("date_of_birth"), "mandatory")\
        .reset_field_values().set_recordset_name("pets")

    check_fm(fm)


    # Test Tuzik

    fm.set_field_values(get_pet_Tuzik())
    check_pet(fm, get_pet_Tuzik())


    # Test Barsik

    barsik = get_pet_Barsik()

    fm.set_field_value("pet_name", barsik["pet_name"])
    fm.set_field_value("species", barsik["species"])
    fm.set_field_value("weight", barsik["weight"])
    fm.set_field_value("date_of_birth", datetime.datetime.strptime("2020-11-08", "%Y-%m-%d"))

    check_pet(fm, barsik)


check_module()



