# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   cfg.py                                  (\(\
# Func:     Reading configuration parameters        (^.^)                                                                                                                                                                        
# # ## ### ##### ######## ############# #####################

from typing import Dict, Tuple
import configparser
import utils


class Cfg:

    def __init__(self, default_app_name: str="Default"):

        self.parser = configparser.ConfigParser()

        self.cfg_file_path = None
        self.default_app_name = default_app_name
        

    def load(self, cfg_file_path: str) -> 'Cfg':
        
        self.cfg_file_path = cfg_file_path

        self.parser.read(cfg_file_path)

        return self

    
    def get_cfg_file_path(self) -> str:
        
        return self.cfg_file_path


    def get_default_app_name(self) -> str:

        return self.default_app_name.upper()


    def is_useful(self, value: any) -> bool:

        return not (value == "" or value is None)


    def get_param_value(self, sect_name: str, param_name: str) -> str:

        try:
            optvalue = self.parser.get(sect_name.upper(), param_name)
        except:
            optvalue = None

        return optvalue 


    def get_app_param_value(self, app_name: str, param_name: str) -> str:

        actual_app_name = utils.safeval(app_name, self.get_default_app_name())

        candidate = self.get_param_value(actual_app_name.upper(), param_name)

        winner = candidate if self.is_useful(candidate) \
                         else self.get_param_value("DEFAULT", param_name)
        
        return winner.upper()


    def get_default_cms_session_duration(self) -> int:

        duration = self.get_param_value("CMS_SESSION", "default_duration")

        return int(utils.safeval(duration, 60))     


    def get_dbms_connection_params(self) -> Dict:

        dbms_connection_params = {
            "software": self.get_param_value("DBMS", "software"),
            "host": self.get_param_value("DBMS", "host"),
            "port": self.get_param_value("DBMS", "port")
        }

        return dbms_connection_params
    

    def get_db_connection_params(self) -> Dict:

        db_connection_params = { 
            "database": self.get_param_value("DATABASE", "database"),
            "user":     self.get_param_value("DATABASE", "user"),
            "password": self.get_param_value("DATABASE", "password")
        }    

        return db_connection_params


    def get_default_admin_credentials(self) -> Tuple[str, str]:

        username = self.get_param_value("DEFAULT_ADMIN_USER", "username")
        passhash = self.get_param_value("DEFAULT_ADMIN_USER", "passhash")    

        return username, passhash
    

    def get_guest_username(self, app_name: str) -> str:

        return self.get_param_value(app_name, "guest_username")


    def get_default_db_scheme_name(self) -> str:

        return self.get_param_value("DATABASE", "default_scheme")    


    def is_debug_mode(self, app_name: str=None) -> str:
        
        return self.get_app_param_value(app_name, "debug_mode").lower() == "on"


    def get_run_mode(self, app_name: str=None) -> str:

        return self.get_app_param_value(app_name, "run_mode").lower()
        

    def is_console_mode(self, app_name: str=None) -> str:

        return "console" in self.get_run_mode(app_name)


    def is_cgi_mode(self, app_name: str=None) -> str:

        return "cgi" in self.get_run_mode(app_name)


    def is_batch_mode(self, app_name: str=None) -> str:

        return "batch" in self.get_run_mode(app_name)


    def get_log_folder_path(self) -> str:

        return self.get_param_value("LOGGING", "log_folder_path")


    def get_logs(self, app_name: str=None) -> str:

        return self.get_app_param_value(app_name, "logs").lower()


    def is_log_to_file_mode(self, app_name: str=None) -> str:

        return "file" in self.get_logs(app_name)


    def is_log_to_db_mode(self, app_name: str=None) -> str:

        return "db" in self.get_logs(app_name)