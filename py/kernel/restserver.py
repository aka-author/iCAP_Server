# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  restserver.py                             (\(\
# Func:    Providing a prototype for a REST server   (^.^)
# # ## ### ##### ######## ############# #####################

import cgi, os, sys
import utils, status, logs, clientreq, httpresp, userdesk, app


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

        if os.environ["CONTENT_TYPE"] == "application/json":
            cgi_body = sys.stdin.read(int(os.environ.get("CONTENT_LENGTH", "0")))
        elif os.environ["CONTENT_TYPE"] == "application/x-www-form-urlencoded":
            cgi_form_fields = utils.extract_fields_from_url_encoded_form(input())
        elif os.environ["CONTENT_TYPE"] == "multipart/form-data":
            cgi_form_fields = utils.extract_fields_from_storage(cgi.FieldStorage())            
        
        req = clientreq.ClientRequest(os.environ, cgi_form_fields, cgi_body)
        
        self.set_req(req)
        
        return req


    def auth_client(self, request):
  
        return True


    def validate_request(self, request):

        return True


    def type_response(self, response):

        print(response.serialize()) 


    def do_the_job(self, request):

        return httpresp.HttpResponse()


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
                self.type_response(httpresp.HttpResponse().set_result_404())

        else:
            self.set_status_code(status.ERR_NOT_AUTHORIZED)
            self.log(logs.LOG_ERROR, status.MSG_NOT_AUTHORIZED, self.req.get_serialized_payload())
            self.type_response(httpresp.HttpResponse().set_result_401())

        return  self.quit()