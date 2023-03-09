# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  user_session.py                         (\(\
# Func:    Managing a user session                 (^.^)                                                                                                                                            
# # ## ### ##### ######## ############# #####################

from datetime import datetime, timedelta
import uuid
import fields, models, dtos


class UserSession(models.Model): 

    def __init__(self, chief: object, uuid: uuid.UUID=None):

        super().__init__(chief)

        self.set_model_name("user_session")

        self.set_field_value("closed_at", None)
        
        if uuid is not None:
            self.set_id(uuid)


    def define_fields(self):
        
        self.get_field_manager()\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.UuidField("user_uuid"))\
            .add_field(fields.StringField("username_deb"))\
            .add_field(fields.StringField("host"))\
            .add_field(fields.TimestampField("opened_at"))\
            .add_field(fields.TimestampField("expire_at"))\
            .add_field(fields.BigintField("duration"))\
            .add_field(fields.TimestampField("closed_at"))

        return self


    def set_export_dto_filter(self, dto: dtos.Dto) -> 'models.Model':
        
        dto.add_to_black_list("user_uuid", "username_deb", "closed_at")

        return self


    def set_uuid(self):

        self.get_field_manager().set_field_value("uuid", uuid.uuid4())

        return self


    def set_expire_at(self, duration):

        fm = self.get_field_manager()

        expire_at = self.fm.get_field_value("opened_at") + timedelta(seconds=duration)
        fm.set_field_value("expire_at", expire_at)

        return self


    def is_valid(self):
        
        return self.get_field_manager().get_field_value("uuid") is not None
    

    def close(self) -> 'UserSession':

        self.get_field_manager().set_field_value("closed_at", datetime.now())

        self.update()

        return self