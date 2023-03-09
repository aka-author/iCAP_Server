# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  users.py                                  (\(\
# Func:    Managing a user of a system               (^.^)
# # ## ### ##### ######## ############# #####################

import fields, models, userdesk


class User(models.Model):

    def __init__(self, chief: 'userdesk.User'):

        super().__init__(chief)
                         
        self.set_model_name("user")


    def define_fields(self):
        
        self.get_field_manager()\
            .add_field(fields.UuidField("uuid"), "subkey,autoins")\
            .add_field(fields.StringField("username"))\
            .add_field(fields.StringField("password_hash"))\
            .add_field(fields.BooleanField("auth_required"))\
            .add_field(fields.BooleanField("configuring_system"))\
            .add_field(fields.BooleanField("saving_measurements"))\
            .add_field(fields.BooleanField("fetching_reports"))

        return self