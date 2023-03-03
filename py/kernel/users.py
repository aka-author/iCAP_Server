# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  users.py                                  (\(\
# Func:    Modeling a user of a system              (^.^)
# # ## ### ##### ######## ############# #####################

import fields, models


class User(models.Model):

    def __init__(self, chief):

        super().__init__(chief)
                         
        self.set_model_name("user")


    def define_fields(self):
        
        self.get_field_manager()\
            .add_field(fields.UuidField("uuid"), "key")\
            .add_field(fields.StringField("username"))\
            .add_field(fields.StringField("password_hash"))\
            .add_field(fields.BooleanField("auth_required"))\
            .add_field(fields.BooleanField("configuring_system"))\
            .add_field(fields.BooleanField("saving_measurements"))\
            .add_field(fields.BooleanField("fetching_reports"))

        return self


    def get_uuid(self):

        return self.get_field_manager().get_field_value("uuid")


    def get_username(self):

        return self.get_field_manager().get_field_value("username")


    def get_password_hash(self):

        return self.get_field_manager().get_field_value("password_hash")


    def is_auth_required(self):

        return self.get_field_manager().get_field_value("auth_required")


    def may_configure_system(self):

        return self.get_field_manager().get_field_value("configuring_system")


    def may_save_measurements(self):

        return self.get_field_manager().get_field_value("saving_measurements")

    
    def may_fetch_reports(self):

        return self.get_field_manager().get_field_value("fetching_reports")
        
