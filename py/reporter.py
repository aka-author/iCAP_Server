#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Level:    Application
# Module:   reporter.py                              
# Func:     Requesting and delivering reports         (\(\
# Usage     REST server, CGI script                   (^.^)
# # ## ### ##### ######## ############# ##################### 

import os, sys, pathlib
from datetime import datetime
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import utils, performer_desks, perfreq, perfresp, restserver, restreq, restresp, dtos, users
from debug import deb_reporter


class Reporter(restserver.RestServer):

    def __init__(self, rel_cfg_file_path: str):

        super().__init__("Reporter", rel_cfg_file_path)

        self.performer_desk = performer_desks.PerformerDesk(self)


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_reporter.mock_cgi_input()

        return self


    def get_performer_desk(self) -> performer_desks.PerformerDesk:

        return self.performer_desk


    def check_user_permissions(self, user: users.User) -> bool:

        return user.may_fetch_reports()


    def validate_rest_request(self, rest_req: restreq.RestRequest) -> bool:
        
        return super().validate_rest_request(rest_req)


    def new_performer_request_dto(self, req: restreq.RestRequest) -> dtos.Dto:

        return dtos.Dto(req.get_payload()).repair_datatypes()


    def produce_response(self, req: restreq.RestRequest) -> restresp.RestResponse:

        perf_req = perfreq.PerformerRequest(self).import_dto(self.new_performer_request_dto(req))
        perf_name = perf_req.get_performer_name()                    
        perf_reporter = self.get_performer_desk().involve_reporter(perf_name)
        
        if self.check_performer_blade(perf_reporter):

            report_name = perf_req.get_task_name()
            perf_query_data = perf_req.get_payload()
            
            started_at = datetime.now()
            report = perf_reporter.build_report(report_name, perf_query_data)
            finished_at = datetime.now()
            duration = (finished_at - started_at).microseconds 
            
            perf_resp = perfresp.PerformerResponse(self)\
                .set_ver(perf_reporter.get_report_ver())\
                .set_status_code(perf_reporter.get_status_code())\
                .set_status_message(perf_reporter.get_status_message())\
                .set_performer_name(perf_name)\
                .set_task_name(report_name)\
                .set_started_at(started_at)\
                .set_finished_at(finished_at)\
                .set_duration(duration)\
                .set_payload(report)
            
        else:
            perf_resp = self.get_performer_desk().get_failure_performer_response()

        return restresp.RestResponse().set_body(perf_resp.export_dto().export_payload())
    

Reporter("../cfg/fserv.ini").process_request()