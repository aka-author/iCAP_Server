# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  apps.py                                     
# Func:    Providing a prototype for each iCAP script   (\(\
# Usage:   The class is abstract                        (^.^)
# # ## ### ##### ######## ############# #####################

import os, pathlib, uuid
import controllers, cfg, dbms_instances, logs, dirdesk, srcdesk


GLOBAL_APP = None

class Application (controllers.Controller):

    def __init__(self, app_name, rel_cfg_file_path):

        super().__init__()

        self.app = self
        self.app_name = app_name
        self.session_id = str(uuid.uuid4())
        
        self.set_cfg_file_path(rel_cfg_file_path)
        self.cfg = cfg.Cfg(self.get_app_name()).load(self.get_cfg_file_path())

        GLOBAL_APP = self
        
        self.default_dbms = self.new_default_dbms(self)
                
        self.logger = logs.Logger(self)

        self.source_desk = srcdesk.SourceDesk(self)
        self.directory_desk = dirdesk.DirectoryDesk(self)


    def get_app_name(self) -> str:

        return self.app_name


    def get_session_id(self) -> uuid.UUID:

        return self.session_id


    def assemble_component_path(self, rel_path: str) -> str:

        script_path = str(pathlib.Path(__file__).parent.absolute())

        return os.path.abspath(script_path + "/../" + rel_path)


    def set_cfg_file_path(self, rel_cfg_file_path: str) -> 'Application':

        self.cfg_file_path = self.assemble_component_path(rel_cfg_file_path)

        return self


    def get_cfg_file_path(self) -> str: 
        
        return self.cfg_file_path


    def is_debug_mode(self) -> bool:

        return self.get_cfg().is_debug_mode()


    def is_console_mode(self) -> bool:
        
        return self.get_cfg().is_console_mode()


    def is_cgi_mode(self) -> bool:
        
        return self.get_cfg().is_cgi_mode()


    def is_batch_mode(self) -> bool:
        
        return self.get_cfg().is_batch_mode()


    def new_default_dbms(self) -> dbms_instances.Dbms:

        # This method is almost useless. Redefine it in a subclass.

        return dbms_instances.Dbms(self)


    def get_log_file_name(self) -> str:
        
        return self.get_app_name().lower() + ".log"


    def get_log_file_path(self) -> str:

        log_file_rel_path = self.get_cfg().get_log_folder_path() + "/" + self.get_log_file_name()

        return self.assemble_component_path(log_file_rel_path)


    def get_logger(self) -> logs.Logger:

        return self.logger


    def log(self, record_type: str, wording: str="", details: str="") -> 'Application':

        self.get_logger().log(record_type, wording, details)

        return self


    def is_log_to_file_mode(self) -> bool:

        return self.get_cfg().is_log_to_file_mode()


    def is_log_to_db_mode(self) -> bool:

        return self.get_cfg().is_log_to_db_mode()


    def get_source_desk(self) -> srcdesk.SourceDesk:

        return self.source_desk
        

    def get_directory_desk(self) -> dirdesk.DirectoryDesk:

        return self.directory_desk


    def quit(self) -> 'Application':

        self.get_logger().close_all()

        return self