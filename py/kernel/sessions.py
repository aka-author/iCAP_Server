# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  session.py                                  (\(\
# Func:    Modeling user sessions                 (^.^)                                                                                                                                            
# # ## ### ##### ######## ############# #####################

from datetime import datetime, timedelta
import uuid
import utils, fields, model


class UserSession(model.Model): 

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

        return self


    def set_expire_at(self, duration):

        expire_at = self.get_field_value("opened_at") + timedelta(seconds=duration)

        self.set_field_value("expire_at", expire_at)

        return self


    def is_valid(self):
        
        return self.get_field_value("uuid") is not None


    def get_direct_load_query(self, field_name, field_value):

        dlq = self.get_dbl().new_select("selusers", "icap").set_output_ramtable(self.get_empty_master_ramtable())
        
        conds = "({0} = '{1}') and (closed_at is null) and (expire_at > '{2}'::timestamp)"

        dlq.WHERE.sql.add(conds.format(field_name, str(field_value), utils.timestamp2str(datetime.now())))

        print(dlq.get_snippet())

        return dlq