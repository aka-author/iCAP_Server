# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  user.py                                  (\(\
# Func:    Modeling a system user                   (^.^)
# # ## ### ##### ######## ############# #####################

import utils, fields, model


class User(model.Model):

    def __init__(self, chief):

        super().__init__(chief, "user")


    def define_fields(self):
        
        self.add_field(fields.UuidField("uuid"), "key")\
            .add_field(fields.StringField("username"))\
            .add_field(fields.StringField("password_hash"))\
            .add_field(fields.BooleanField("auth_required"))\
            .add_field(fields.BooleanField("configuring_system"))\
            .add_field(fields.BooleanField("saving_measurements"))\
            .add_field(fields.BooleanField("fetching_reports"))

        return self


    def check_password(self, password):

        return self.get_field_value("password_hash") == utils.md5(password)


    def may_configure_system(self):

        return self.get_field_value("configuring_system")


    def may_save_measurements(self):

        return self.get_field_value("saving_measurements")

    
    def may_fetch_reports(self):

        return self.get_field_value("fetching_reports")
        
