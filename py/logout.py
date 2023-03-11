#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Application 
# Module:   logout.py                                
# Func:     Terminating a user session             (\(\    
# Usage:    REST server                            (^.^)
# # ## ### ##### ######## ############# #####################

import os, sys, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import utils, restresp, auth, restserver
from debug import deb_logout


class Logout(restserver.RestServer):

    def __init__(self, rel_cfg_file_path: str):

        super().__init__("Logout", rel_cfg_file_path)


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_logout.mock_cgi_input()

        return self


    def do_the_job(self, req):

        user_session_uuid = utils.str2uuid(req.get_cookie())

        self.auth_agent.close_user_session(user_session_uuid)
        
        return restresp.RestResponse()


Logout("../cfg/fserv.ini").process_request()
