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


    def is_valid(self, user_session_uuid: uuid.UUID) -> bool:

        dbms = self.get_default_dbms()
        db = self.get_default_db()

        runner = dbms.new_query_runner(db)

        out_fm = fields.FieldManager()\
            .add_field(fields.BigintField("count_valid"))

        count_query = dbms.new_select(db)\
            .FROM((self.get_plural(), "icap"))\
            .WHERE("{0}={1} AND {2}>{3} AND {4} IS null", 
                   ("uuid", 0), user_session_uuid, 
                   ("expire_at", 0), datetime.now(),
                   ("closed_at", 0))\
            .SELECT_expression("count_valid", "count(*)")\
            .set_field_manager(out_fm)
        
        count_result = runner.execute_query(count_query).get_query_result().fetch_one()

        runner.close()
        print(count_result.fm.get_field_value("count_valid"))

        return count_result.fm.get_field_value("count_valid") == 1
        

    def close(self) -> 'UserSession':

        self.get_field_manager().set_field_value("closed_at", datetime.now())

        self.update()

        return self