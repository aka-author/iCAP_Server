# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  user_session.py                         (\(\
# Func:    Managing a user session                 (^.^)                                                                                                                                            
# # ## ### ##### ######## ############# #####################

from datetime import datetime, timedelta
import uuid
import fields, workers, models, dtos


class UserSession(models.Model): 

    def __init__(self, chief: workers.Worker, user_session_uuid: uuid.UUID=None):

        super().__init__(chief)

        self.set_model_name("user_session")

        self.set_field_value("uuid", user_session_uuid if user_session_uuid is not None else uuid.uuid4())
        self.set_field_value("closed_at", None)


    def define_fields(self) -> 'UserSession':
        
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


    def is_valid(self) -> bool:

        is_expired = self.get_field_value("expire_at") <= datetime.now()
        is_closed = self.get_field_value("closed_at") is not None

        return not is_expired and not is_closed


    def set_export_dto_filter(self, dto: dtos.Dto) -> 'models.Model':
        
        dto.add_to_black_list("user_uuid", "username_deb", "closed_at")

        return self


    def set_expire_at(self, duration: int) -> 'UserSession':

        expire_at = self.get_field_value("opened_at") + timedelta(seconds=duration)
        
        self.set_field_value("expire_at", expire_at)

        return self


    def fast_check(self) -> bool:

        dbms, db = self.get_default_dbms(), self.get_default_db()        

        db_table_name = self.get_plural()
        db_scheme_name = self.get_default_db_scheme_name()

        runner = dbms.new_query_runner(db)

        count_query = dbms.new_select()\
            .FROM((db_table_name, db_scheme_name))\
            .WHERE("{0}={1} AND {2}>{3} AND {4} IS null", 
                   ("uuid", 0), self.get_field_value("uuid") , 
                   ("expire_at", 0), datetime.now(),
                   ("closed_at", 0))\
            .SELECT_expression("count_valid", "count(*)")
        
        runner.execute_query(count_query)

        if runner.isOK():
            count_result = runner.get_query_result().fetch_one()
            runner.close()
        else:
            raise Exception("Database error")
        
        return count_result.fm.get_field_value("count_valid") == 1
        

    def load_by_uuid(self, user_session_uuid: uuid.UUID) -> 'UserSession':

        return self.load("uuid", user_session_uuid)


    def close(self) -> 'UserSession':

        self.get_field_manager().set_field_value("closed_at", datetime.now())

        self.update()

        return self