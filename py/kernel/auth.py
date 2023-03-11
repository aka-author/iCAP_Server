# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   auth.py                                  
# Func:     Managing user sessions                   (\(\  
# Usage:    Use an Auth instance directly            (^.^)                                                                                                                  
# # ## ### ##### ######## ############# #####################

from datetime import datetime
import uuid
import utils, workers, controllers, users, user_sessions


class Auth(controllers.Controller):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def check_user_credentials(self, user: users.User, password: str) -> bool:

        return user.get_field_value("password_hash") == utils.md5(password)


    def open_user_session(self, user: users.User, host: str, duration: int) -> user_sessions.UserSession:

        user_session = user_sessions.UserSession(self)\
            .set_field_value("uuid", uuid.uuid4())\
            .set_field_value("user_uuid", user.get_field_value("uuid"))\
            .set_field_value("username_deb", user.get_field_value("username"))\
            .set_field_value("host", host)\
            .set_field_value("opened_at", datetime.now())\
            .set_field_value("duration", duration)\
            .set_expire_at(duration)
    
        user_session.insert()
            
        return user_session


    def check_user_session(self, user_session_uuid: uuid.UUID) -> bool:

        us = user_sessions.UserSession(self).set_field_value("uuid", user_session_uuid)

        return us.fast_check()


    def close_user_session(self, user_session_uuid: uuid.UUID) -> 'Auth':

        user_session = user_sessions.UserSession(self)
        
        user_session.load_by_uuid(user_session_uuid).close()

        return self