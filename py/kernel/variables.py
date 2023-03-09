# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  variables.py                              (\(\
# Func:    Managing an iCAP variable                 (^.^)
# # ## ### ##### ######## ############# #####################

import fields, models


class Variable(models.Model):

    def __init__(self, chief):

        super().__init__(chief)

        self.set_model_name("variable")

        
    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.StringField("varname"))\
            .add_field(fields.StringField("datatype_name"))\
            .add_field(fields.StringField("shortcut"))

        return self