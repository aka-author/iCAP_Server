# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Prototype
# Module:  session.py                                  (\(\
# Func:    Impersonating user sessions                 (^.^)                                                                                                                                            
# # ## ### ##### ######## ############# #####################

from datetime import timedelta
import uuid
import fields, model


class Session(model.Model): 

    def __init__(self, chief, uuid=None):

        super().__init__(chief, "user_session")
        
        if uuid is not None:
            self.set_id(uuid)


    def define_fields(self):
        
        self.add_field(fields.UuidField("uuid"))\
            .add_field(fields.UuidField("user_uuid"))\
            .add_field(fields.StringField("username_deb"))\
            .add_field(fields.StringField("host"))\
            .add_field(fields.TimestampField("opened_at"))\
            .add_field(fields.TimestampField("expire_at"))\
            .add_field(fields.BigintField("duration"))\
            .add_field(fields.TimestampField("closed_at"))

        return self


    def set_uuid(self):

        self.set_field_value("uuid", uuid.uuid4())


    def set_expire_at(self, duration):

        expire_at = self.get_field_value("openedAt") + timedelta(seconds=duration)

        self.set_field_value("expireAt", expire_at)


    def is_valid(self):
        
        return self.get_field_value("uuid") is not None