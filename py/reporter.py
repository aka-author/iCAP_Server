#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  reporter.py                              (\(\
# Func:    Requesting and delivering reports        (^.^)
# # ## ### ##### ######## ############# ##################### 

import os, sys, pathlib

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/modules"))
from modules import restserver, logs, measurement, httpresp
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

        

        return httpresp.HttpResponse()
    

Reporter("../cfg/fserv.ini").process_request()