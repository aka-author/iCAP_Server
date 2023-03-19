# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   restserver.py                             
# Func:     Responding on REST requests                (\(\
# Usage:    Derive a REST CGI script from RestServer   (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import cgi, os, sys, uuid
from datetime import datetime
import utils, status, logs, dtos, restreq, restresp, performers, users, auth, apps
import status, restreq, appreq, appresp, perftask, perfoutput


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
            try:
                cgi_form_fields = utils.extract_fields_from_url_encoded_form(input())
            except:
                cgi_form_fields = {}
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


    def validate_rest_request(self, rest_req: restreq.RestRequest) -> bool:

        return True
    

    def check_performer_blade(self, performer_blade: performers.Blade) -> bool:

        return performer_blade is not None


    def involve_performer_blade(self, perf_name: str) -> object:

        return None 


    def error_unknown_performer(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

        failure = perfoutput.PerformerOutput(self)\
                        .set_performer_name(task.get_performer_name())\
                        .set_task_name(task.get_task_name())\
                        .set_status_code(status.ERR_UNKNOWN_PERFORMER)\
                        .set_status_message(status.MSG_UNKNOWN_PERFORMER)
        
        return failure
    

    def perform_task(self, task_data: Dict) -> Dict:

        perf_task = perftask.PerformerTask(self).import_dto(dtos.Dto(task_data))
        
        perf_name = perf_task.get_performer_name()
        
        pref_blade = self.involve_performer_blade(perf_name)
        
        perf_output = pref_blade.perform_task(perf_task)\
                        if self.check_performer_blade(pref_blade)\
                        else self.error_unknown_performer(perf_task)
        
        return perf_output.export_dto().get_payload()


    def error_unknown_request_type(self):

        error_info = {"status_code": status.ERR_UNKNOWN_REQUEST_TYPE, 
                      "status_message": status.MSG_UNKNOWN_REQUEST_TYPE}

        return error_info


    def new_app_request_dto(self, req: restreq.RestRequest) -> dtos.Dto:

        return dtos.Dto(req.get_payload()).repair_datatypes()


    def produce_response(self, req: restreq.RestRequest) -> restresp.RestResponse:

        app_req = appreq.AppRequest(self).import_dto(self.new_app_request_dto(req))
        app_req_type_name = app_req.get_type_name()

        started_at = datetime.now()

        if app_req_type_name == "performer_task":
            app_resp_body = self.perform_task(app_req.get_body())
            app_resp_type_name = "performer_output"
        else:
            app_resp_body = self.error_unknown_request_type()
            app_resp_type_name = "request_error"
        
        finished_at = datetime.now()

        app_resp = appresp.AppResponse(self)\
                        .set_type_name(app_resp_type_name)\
                        .set_ver(2)\
                        .set_started_at(started_at)\
                        .set_finished_at(finished_at)\
                        .set_duration((finished_at - started_at).microseconds)\
                        .set_body(app_resp_body)

        return restresp.RestResponse().set_body(app_resp.export_dto().export_payload())


    def type_response(self, resp: restresp.RestResponse) -> 'RestServer':

        print(resp.serialize())

        return self


    def cope(self, req: restreq.RestRequest) -> apps.Application:

        if self.authorize_user(req):

            if self.validate_rest_request(req):
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