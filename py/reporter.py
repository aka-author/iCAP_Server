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
from kernel import restserver, restreq, restresp, users
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


    def do_the_job(self, req: restreq.RestRequest) -> restresp.RestResponse:

        # shop = self.get_shop_desk(report_name)

        # report = shop.build_report(request)
        
        # response =  httpresp.HttpResponse().set_body(report)

        return restresp.HttpResponse().set_body({})
    

Reporter("../cfg/fserv.ini").process_request()