# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  restserver.py                             (\(\
# Func:    Providing a prototype for a REST server   (^.^)
# # ## ### ##### ######## ############# #####################

import cgi, os, sys, pathlib
import  dbl, cfg, bureaucrat, clientreq, dirdesk


class RestServer (bureaucrat.Bureaucrat):

    def __init__(self, rel_cfg_file_path):

        super().__init__()

        self.app = self
        self.set_cfg_file_path(rel_cfg_file_path)
        self.cfg = cfg.Cfg().load(self.get_cfg_file_path())
        self.dbl = dbl.Dbl(self)
        self.directory_desk = dirdesk.DirectoryDesk(self)

        self.debug_mode_flag = False


    def set_cfg_file_path(self, rel_cfg_file_path):

        script_path = str(pathlib.Path(__file__).parent.absolute())

        self.cfg_file_path = os.path.abspath(script_path + "/../" + rel_cfg_file_path)

        return self


    def get_cfg_file_path(self): 
        
        return self.cfg_file_path


    def get_directory_desk(self):

        return self.directory_desk


    def parse_cgi_data(self):

        content_len = os.environ.get("CONTENT_LENGTH", "0")
        body = self.get_debug_request_body() if self.is_debug_mode() else sys.stdin.read(int(content_len))
        
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