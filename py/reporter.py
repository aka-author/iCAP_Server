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

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import assayreq, assayresp, restserver, restreq, restresp, dtos, users, \
    shop_shortcuts, shop_desks
from debug import deb_reporter


class Reporter(restserver.RestServer):

    def __init__(self, rel_cfg_file_path: str):

        super().__init__("Reporter", rel_cfg_file_path)


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_reporter.mock_cgi_input()

        return self


    def check_user_permissions(self, user: users.User) -> bool:

        return user.may_fetch_reports()


    def validate_request(self, req: restreq.RestRequest) -> bool:
        
        return True


    def new_assay_request_dto(self, req: restreq.RestRequest) -> dtos.Dto:

        return dtos.Dto(req.get_payload()).repair_datatypes()


    def produce_response(self, req: restreq.RestRequest) -> restresp.RestResponse:

        assay_req = assayreq.AssayRequest(self).import_dto(self.new_assay_request_dto(req))
                            
        shop = self.get_shop_desk().involve_shop(assay_req.get_shop_name())

        if shop is not None:
            report = shop.build_report(assay_req.get_report_name(), assay_req.get_payload())
            assay_resp = assayresp.AssayResponse(self).set_payload(report)
        else:
            assay_resp = self.get_shop_desk().get_failure_assay_response()

        return restresp.RestResponse().set_body(assay_resp.export_dto().export_payload())
    

Reporter("../cfg/fserv.ini").process_request()