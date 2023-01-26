# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  app.py                                     (\(\
# Func:    Providing a prototype for each iCAP script (^.^)
# # ## ### ##### ######## ############# #####################

import os, sys, pathlib, uuid
import status, dblayer, cfg, bureaucrat, logs, dirdesk, srcdesk


GLOBAL_APP = None

class Application (bureaucrat.Bureaucrat):

    def __init__(self, rel_cfg_file_path):

        super().__init__()

        self.app = self
        self.session_id = str(uuid.uuid4())
        
        self.set_cfg_file_path(rel_cfg_file_path)
        self.cfg = cfg.Cfg().load(self.get_cfg_file_path())

        GLOBAL_APP = self
        
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


    def log(self, record_type, wording="", details=""):

        self.get_logger().log(record_type, wording, details)

        return self


    def get_source_desk(self):

        return self.source_desk
        

    def get_directory_desk(self):

        return self.directory_desk