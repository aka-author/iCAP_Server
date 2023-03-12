# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   restserver.py                             
# Func:     Providing a prototype for a REST server    (\(\
# Usage:    Derive your application from RestServer    (^.^)
# # ## ### ##### ######## ############# #####################

import cgi, os, sys
import utils, status, logs, restreq, restresp, auth, apps


class RestServer (apps.Application):

    def __init__(self, app_name: str, rel_cfg_file_path: str):

        super().__init__(app_name, rel_cfg_file_path)

        self.auth_agent = auth.Auth(self)


    def mock_cgi_input(self):

       return self


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


    def auth_client(self, req: restreq.RestRequest) -> bool:
        
        user_session_uuid = utils.str2uuid(req.get_cookie())
        
        return self.auth_agent.check_user_session(user_session_uuid)


    def validate_request(self, req: restreq.RestRequest) -> bool:

        return True


    def type_response(self, resp: restresp.RestResponse) -> 'RestServer':

        print(resp.serialize())

        return self


    def do_the_job(self, req: restreq.RestRequest) -> restresp.RestResponse:

        return restresp.RestResponse()


    def fail(self, errmsg):
        self.log(logs.LOG_ERROR, status.MSG_FATAL, errmsg)
        self.type_response(restresp.RestResponse().set_result_500())


    def cope(self, req: restreq.RestRequest) -> apps.Application:

        if self.auth_client(req):

            if self.validate_request(req):
                resp = self.do_the_job(req)
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