#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Level:    Application
# Module:   admin.py                              
# Func:     Configuring and maintaining a system       (\(\
# Usage     REST server, CGI script                    (^.^)
# # ## ### ##### ######## ############# ##################### 

import os, sys, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import performer_desks, restserver, users
from debug import deb_admin


class Admin(restserver.RestServer):

    def __init__(self, rel_cfg_file_path: str):

        super().__init__("Admin", rel_cfg_file_path)

        self.performer_desk = performer_desks.PerformerDesk(self)


    def mock_cgi_input(self):

        super().mock_cgi_input()
     
        deb_admin.mock_cgi_input()

        return self


    def get_performer_desk(self) -> performer_desks.PerformerDesk:

        return self.performer_desk


    def check_user_permissions(self, user: users.User) -> bool:

        return user.may_configure_system()


    def involve_performer_blade(self, perf_name: str) -> object:
        
        return self.get_performer_desk().involve_admin(perf_name) 


Admin("../cfg/fserv.ini").process_request()