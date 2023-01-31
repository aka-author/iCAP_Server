#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Level:   Application
# Module:  reporter.py                              (\(\
# Func:    Requesting and delivering reports        (^.^)
# # ## ### ##### ######## ############# ##################### 

import os, sys, pathlib

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import restserver, logs, measurement, httpresp
from debug import deb_reporter


class Reporter(restserver.RestServer):

    def __init__(self, rel_cfg_file_path):

        super().__init__("Reporter", rel_cfg_file_path)


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_reporter.mock_cgi_input()

        return self


    def validate_request(self, request):
        
        return True


    def do_the_job(self, request):

        # shop = self.get_shop_desk(report_name)

        # report = shop.build_report(request)
        
        # response =  httpresp.HttpResponse().set_body(report)

        return httpresp.HttpResponse().set_body({})
    

Reporter("../cfg/fserv.ini").process_request()