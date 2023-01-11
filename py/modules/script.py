# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  script.py                                  (\(\
# Func:    Providing a prototype for each script      (^.^)
# # ## ### ##### ######## ############# #####################

import cgi, os, sys
from . import cfg, bureaucrat, clientreq


class Script (bureaucrat.Bureaucrat):

    def __init__(self):

        super().__init__()

        self.app = self
        self.cfg = self.load_cfg(self.get_cfg_file_path())
        self.db = self.connect_db()


    def get_cfg_file_path(self): 

        return "../cfg/fserv.ini"


    def load_cfg(self, cfg_file_path):

        return cfg.Cfg(cfg_file_path)


    def connect_db(self): 

        return ""


    def parse_cgi_data(self):

        content_len = os.environ.get("CONTENT_LENGTH", "0")
        body = sys.stdin.read(int(content_len))

        return clientreq.ClientRequest(os.environ, cgi.FieldStorage(), body)


    def auth_client(self, request):

        return True


    def type_positive_response(self, response):

        pass 


    def type_negative_response(self):

        pass


    def do_the_job(self, request):

        pass


    def process_request(self):

        self.set_req(self.parse_cgi_data())
        
        if self.auth_client(self.get_req()):
            self.type_positive_response(self.do_the_job(self.get_req()))
        else:
            self.type_negative_response()