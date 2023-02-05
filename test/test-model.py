
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import dbms, dtoms, fields, model


class AppMoke():

    def __init__(self):

        pass

    
    def get_app(self):

        return self


    def get_dtoms(self):

        return dtoms.DtoMs(self)


class Pet(model.Model):

    def __init__(self, chief):

        super().__init__(chief, "pet")


    def define_fields(self):

        self.fm.add_field(fields.UuidField("uuid"))\
               .add_field(fields.StringField("pet_name"))\
               .add_field(fields.StringField("species"))\
               .add_field(fields.BigintField("weight"))\
               .add_field(fields.DateField("date_of_birth"), "mandatory")


app_moke = AppMoke()

pet = Pet(app_moke)

dto_tuzik = {
    "pet_name": "Tuzik",
    "species": "dog",
    "weight": 10,
    "date_of_birth": "2020-02-03"
}

pet.import_dto(dto_tuzik)
print(pet)

dto_tuzik_out = pet.export_dto()
print(dto_tuzik_out)