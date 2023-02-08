# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  auth.py                                  (\(\
# Func:    Managing user sessions                   (^.^)                                                                                                                                            
# # ## ### ##### ######## ############# #####################

from datetime import datetime
import status, utils, controller, sessions


class Auth(controller.Controller):

    def __init__(self, chief):

        super().__init__(chief)


    def check_user_credentials(self, user, password):

        return user.get_password_hash() == utils.md5(password)


    def open_session(self, user, host, duration):

        session = sessions.UserSession(self)\
            .set_uuid()\
            .set_field_value("user_uuid", user.get_uuid())\
            .set_field_value("username_deb", user.get_username())\
            .set_field_value("host", host)\
            .set_field_value("opened_at", datetime.now())\
            .set_field_value("duration", duration)\
            .set_expire_at(duration)
    
        session.direct_save()
            
        return session


    def check_session(self, session_uuid):

        return sessions.UserSession(self).direct_load("uuid", session_uuid).is_valid()


    def close_session(self, session):

        dbl = self.get_dbl()

        # upd_q = dbl.new_update()\
        #    .TABLE.sql.set("icap.user_sessions").q\
        #    .SET.sql.set("closed_at = '{0}'".format(utils.timestamp2str(datetime.now()))).q\
        #    .WHERE.sql.set("uuid = '{0}'".format(str(session_uuid))).q


        upd_q = dbl.new_update()\
            .TABLE.sql.set("{scheme}.user_session").q\
            .SET.sql.set(session.fm.sql_equal("closed_at", datetime.now())).q\
            .WHERE.sql.set(session.fm.sql_equal("uuid")).q


        dbl.execute(upd_q).commit()

        return self