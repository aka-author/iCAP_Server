# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  restserver.py                             (\(\
# Func:    Providing a prototype for a REST server   (^.^)
# # ## ### ##### ######## ############# #####################

import cgi, os, sys, pathlib, uuid
import dblayer, cfg, bureaucrat, logs, clientreq, dirdesk, srcdesk


class RestServer (bureaucrat.Bureaucrat):

    def __init__(self, rel_cfg_file_path):

        super().__init__()

        self.app = self
        self.session_id = str(uuid.uuid4())
        
        self.set_cfg_file_path(rel_cfg_file_path)
        self.cfg = cfg.Cfg().load(self.get_cfg_file_path())
        
        self.dbl = dblayer.Dbl(self)
        
        self.logger = logs.Logger(self)

        self.source_desk = srcdesk.SourceDesk(self)
        self.directory_desk = dirdesk.DirectoryDesk(self)


    def get_app_name(self):

        return "icap"


    def get_session_id(self):

        return self.session_id


    def assemble_component_path(self, rel_path):

        script_path = str(pathlib.Path(__file__).parent.absolute())

        return os.path.abspath(script_path + "/../" + rel_path)


    def set_cfg_file_path(self, rel_cfg_file_path):

        self.cfg_file_path = self.assemble_component_path(rel_cfg_file_path)

        return self


    def get_cfg_file_path(self): 
        
        return self.cfg_file_path


    def get_log_file_name(self):
        
        return "icap.log"


    def get_log_file_path(self):

        log_file_rel_path = self.get_cfg().get_log_folder_path() + "/" + self.get_log_file_name()

        return self.assemble_component_path(log_file_rel_path)


    def get_logger(self):

        return self.logger


    def get_source_desk(self):

        return self.source_desk
        

    def get_directory_desk(self):

        return self.directory_desk


    def parse_cgi_data(self):

        content_len = os.environ.get("CONTENT_LENGTH", "0")
        body = self.get_debug_request_body() if self.is_debug_mode() \
               else sys.stdin.read(int(content_len))
        
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