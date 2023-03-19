#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Application
# Module:   login.py                                  
# Func:     Authorizing users who send REST requests   (\(\  
# Usage     REST server, CGI script                    (^.^)                                                                                                                                 
# # ## ### ##### ######## ############# #####################

import os, sys, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import restreq, restresp, restserver
from debug import deb_login


class Login(restserver.RestServer):

    def __init__(self, rel_cfg_file_path: str):

        super().__init__("Login", rel_cfg_file_path)


    def mock_cgi_input(self) -> restserver.RestServer:

        super().mock_cgi_input()
     
        deb_login.mock_cgi_input()

        return self


    def authorize_user(self, req: restreq.RestRequest) -> bool:

        is_authorized = False
        
        username, password = req.get_credentials()
        user = self.get_user_desk().get_user_by_name(username)

        if user is not None:
            is_authorized = self.get_auth_agent().check_user_credentials(user, password) 
            self.set_current_user(user)

        return is_authorized


    def get_session_duration(self):

        return self.get_cfg().get_default_cms_session_duration()


    def produce_response(self, req: restreq.RestRequest) -> restresp.RestResponse:

        host = req.get_host()
        duration = self.get_session_duration()

        user_session = self.get_auth_agent().open_user_session(self.get_current_user(), host, duration)
        
        return restresp.RestResponse().set_body(user_session.export_dto().export_payload())


Login("../cfg/fserv.ini").process_request()

