#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Application
# Module:  login.py                                  (\(\
# Func:    Authorizing iCAP users                    (^.^)                                                                                                                                                                  
# # ## ### ##### ######## ############# #####################

import os, sys, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import httpresp, auth, restserver
from debug import deb_login


class Login(restserver.RestServer):

    def __init__(self, rel_cfg_file_path):

        super().__init__("Login", rel_cfg_file_path)


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_login.mock_cgi_input()

        return self


    def do_the_job(self, request):

        username, password = request.get_credentials()

        session_info = auth.Auth(self).open_session(username, password)
        
        return httpresp.HttpResponse().set_body(session_info)


Login("../cfg/fserv.ini").process_request()

