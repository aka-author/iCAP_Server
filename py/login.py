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
from kernel import restresp, auth, restserver
from debug import deb_login


class Login(restserver.RestServer):

    def __init__(self, rel_cfg_file_path):

        super().__init__("Login", rel_cfg_file_path)

        self.auth_agent = auth.Auth(self)
        self.user = None


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_login.mock_cgi_input()

        return self


    def auth_client(self, req):

        is_authorized = False
        
        username, password = req.get_credentials()
        self.user = self.get_userdesk().get_user_by_username(username)

        if self.user is not None:
            is_authorized = self.auth_agent.check_user_credentials(self.user, password) 

        return is_authorized


    def get_session_duration(self):

        return self.get_cfg().get_default_cms_session_duration()


    def do_the_job(self, req):

        host = req.get_host()
        duration = self.get_session_duration()

        session = self.auth_agent.open_session(self.user, host, duration)
        
        return restresp.RestResponse().set_body(session.export_dto())


Login("../cfg/fserv.ini").process_request()

