#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Application
# Module:  logout.py                                (\(\
# Func:    Terminating a user session               (^.^)
# # ## ### ##### ######## ############# #####################

import os, sys, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import utils, restresp, auth, restserver
from debug import deb_logout


class Logout(restserver.RestServer):

    def __init__(self, rel_cfg_file_path):

        super().__init__("Logout", rel_cfg_file_path)

        self.auth_agent = auth.Auth(self)


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_logout.mock_cgi_input()

        return self


    def auth_client(self, req):
        print(req.get_cookie())
        self.session_uuid = utils.str2uuid(req.get_cookie())
        
        return self.auth_agent.check_session(self.session_uuid)


    def do_the_job(self, req):

        self.auth_agent.close_session(self.session_uuid)
        
        return restresp.RestResponse()


Logout("../cfg/fserv.ini").process_request()
