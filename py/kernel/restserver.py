# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   restserver.py                             
# Func:     Responding on REST requests                (\(\
# Usage:    Derive a REST CGI script from RestServer   (^.^)
# # ## ### ##### ######## ############# #####################

import cgi, os, sys, uuid
import utils, status, logs, restreq, restresp, users, auth, apps


class RestServer (apps.Application):

    def __init__(self, app_name: str, rel_cfg_file_path: str):

        super().__init__(app_name, rel_cfg_file_path)

        self.auth_agent = auth.Auth(self)
        self.user_session_uuid = None
        self.current_user = None


    def mock_cgi_input(self):

       return self


    def set_user_session_uuid(self, user_session_uuid: uuid.UUID) -> 'RestServer':

        self.user_session_uuid = user_session_uuid

        return self
    

    def get_user_session_uuid(self) -> uuid.UUID:

        return self.user_session_uuid


    def set_current_user(self, user: users.User) -> 'RestServer':

        self.current_user = user

        return self
    

    def get_current_user(self) -> users.User:

        return self.current_user
    

    def parse_cgi_data(self):
        
        if self.is_console_mode():
            self.mock_cgi_input()

        cgi_body = ""
        cgi_form_fields = {}

        c_type = os.environ.get("CONTENT_TYPE", "Not provided")

        if c_type == "application/json":
            cgi_body = sys.stdin.read(int(os.environ.get("CONTENT_LENGTH", "0")))
        elif c_type == "application/x-www-form-urlencoded":
            cgi_form_fields = utils.extract_fields_from_url_encoded_form(input())
        elif c_type == "multipart/form-data":
            cgi_form_fields = utils.extract_fields_from_storage(cgi.FieldStorage())            
        
        req = restreq.RestRequest(os.environ, cgi_form_fields, cgi_body)
        
        self.set_req(req)
        
        return req


    def get_auth_agent(self) -> auth.Auth:

        return self.auth_agent
    

    def get_guest_username(self) -> str:

        return self.get_cfg().get_guest_username(self.get_app_name())


    def check_user_permissions(self, user: users.User) -> bool:

        return False


    def authorize_user(self, req: restreq.RestRequest) -> bool:
        
        passed_user_session_uuid = utils.str2uuid(req.get_cookie())
        
        auth_agent = self.get_auth_agent()

        if auth_agent.check_user_session(passed_user_session_uuid):
            user_session_uuid = passed_user_session_uuid
            user_uuid = auth_agent.get_user_uuid_by_session_uuid(user_session_uuid)
            user = self.get_user_desk().get_user_by_uuid(user_uuid)
        else:
            user_session_uuid = uuid.uuid4()
            user = self.get_user_desk().get_user_by_name(self.get_guest_username())

        self.set_user_session_uuid(user_session_uuid)
        self.set_current_user(user)

        return self.check_user_permissions(user) if user is not None else False


    def validate_request(self, req: restreq.RestRequest) -> bool:

        return True


    def produce_response(self, req: restreq.RestRequest) -> restresp.RestResponse:

        return restresp.RestResponse()


    def type_response(self, resp: restresp.RestResponse) -> 'RestServer':

        print(resp.serialize())

        return self


    def cope(self, req: restreq.RestRequest) -> apps.Application:

        if self.authorize_user(req):

            if self.validate_request(req):
                resp = self.produce_response(req)
                self.type_response(resp)
                self.log(logs.LOG_INFO, status.MSG_RESPONSE, resp.serialize())
            else:
                self.set_status_code(status.ERR_INCORRECT_REQUEST)
                self.log(logs.LOG_ERROR, status.MSG_INCORRECT_REQUEST, self.req.get_serialized_payload())
                self.type_response(restresp.RestResponse().set_result_404())

        else:
            self.set_status_code(status.ERR_NOT_AUTHORIZED)
            self.log(logs.LOG_ERROR, status.MSG_NOT_AUTHORIZED, self.req.get_serialized_payload())
            self.type_response(restresp.RestResponse().set_result_401())

        return self
    

    def fail(self, errmsg):
        self.log(logs.LOG_ERROR, status.MSG_FATAL, errmsg)
        self.type_response(restresp.RestResponse().set_result_500())


    def process_request(self) -> apps.Application:

        if self.isOK():
    
            req = self.parse_cgi_data()
            self.log(logs.LOG_INFO, status.MSG_REQUEST, req.serialize())

            if self.is_debug_mode():
                self.cope(req)
            else:
                try:
                    self.cope(req)
                except Exception as internal_fail_reasons:
                    self.fail(internal_fail_reasons.args[0])
        else:
            self.fail(status.MSG_APP_INIT_FAILED)

        return  self.quit()