# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  auth.py                                  (\(\
# Func:    Managing user sessions                   (^.^)                                                                                                                                            
# # ## ### ##### ######## ############# #####################

from datetime import datetime
import status, utils, controller #, session


class Auth(controller.Controller):

    def __init__(self, chief):

        super().__init__(chief)


    def passw_hash(self, passw):

        return utils.safearg(utils.md5, passw)


    def get_cms_session_duration(self):

        return self.get_cfg().get_cms_session_duration() 


    def check_credentials(self, username, password):

        # cms_login, cms_passw_hash = self.get_cfg().get_default_admin_credentials()
        
        # req_passw_hash = self.passw_hash(req_passw)

        # return req_login == cms_login and req_passw_hash == cms_passw_hash

        u = self.get_app().get_userdesk().get_user_by_username(username)

        return False if u is None else u.check_password(password) 


    def open_session(self, username, password):

        status_code = status.ERR_LOGIN_FAILED
        user_session = {} #session.Session(self) 

        # http_req = self.get_req()
        # req_login, req_passw = http_req.get_credentials()
        
        if self.check_credentials(username, password):

            self.deb("Welcome!")

            # user_session.set_uuid()
            # user_session.set_field_value("login", req_login)
            # user_session.set_field_value("host", http_req.get_host())
            # user_session.set_field_value("openedAt", datetime.now())
            # duration = self.get_cms_session_duration()
            # user_session.set_field_value("duration", duration)
            # user_session.set_expire_at(duration)
        
            # status_code = self.get_db().open_session(user_session)

            # if status_code != status.OK:
            #    user_session.clear_field_values()

            pass
            

        return {"uuid": "e7dd26cb-e609-4f4a-93f0-e696b26b17a4"}  # self.export_result_dto(status_code, "session", user_session.export_dto())


    def check_session(self, session_uuid_str):

        status_code, is_session_active = \
            self.get_db().check_session(utils.str2uuid(session_uuid_str))

        return status_code == status.OK and is_session_active


    def close_session(self):

        session_uuid_str = self.get_req().get_cookie()

        status_code = self.get_db().close_session(utils.str2uuid(session_uuid_str))

        return self.export_result_dto(status_code)