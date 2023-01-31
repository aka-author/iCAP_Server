# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  restserver.py                             (\(\
# Func:    Providing a prototype for a REST server   (^.^)
# # ## ### ##### ######## ############# #####################

import cgi, os, sys
import utils, status, logs, restreq, restresp, userdesk, app


class RestServer (app.Application):

    def __init__(self, app_name, rel_cfg_file_path):

        super().__init__(app_name, rel_cfg_file_path)

        self.userdesk = userdesk.UserDesk(self)


    def get_userdesk(self): 

        return self.userdesk


    def mock_cgi_input(self):

       return self


    def parse_cgi_data(self):
        
        if self.is_console_mode():
            self.mock_cgi_input()

        cgi_body = ""
        cgi_form_fields = {}

        c_type = utils.safedic(os.environ, "CONTENT_TYPE", "Not provided")

        if c_type == "application/json":
            cgi_body = sys.stdin.read(int(os.environ.get("CONTENT_LENGTH", "0")))
        elif c_type == "application/x-www-form-urlencoded":
            cgi_form_fields = utils.extract_fields_from_url_encoded_form(input())
        elif c_type == "multipart/form-data":
            cgi_form_fields = utils.extract_fields_from_storage(cgi.FieldStorage())            
        
        req = restreq.RestRequest(os.environ, cgi_form_fields, cgi_body)
        
        self.set_req(req)
        
        return req


    def auth_client(self, req):
  
        return True


    def validate_request(self, req):

        return True


    def type_response(self, resp):

        print(resp.serialize()) 


    def do_the_job(self, req):

        return restresp.RestResponse()


    def process_request(self):

        req = self.parse_cgi_data()
        self.log(logs.LOG_INFO, status.MSG_REQUEST, req.serialize())

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

        return  self.quit()