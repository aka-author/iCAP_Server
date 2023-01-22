# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  cfg.py                                  (\(\
# Func:    Reading configuration parameters        (^.^)                                                                                                                                                                        
# # ## ### ##### ######## ############# #####################

import configparser
import utils


class Cfg:

    def __init__(self):

        self.parser = configparser.ConfigParser()

        self.cfg_file_path = None
        

    def load(self, cfg_file_path):
        
        self.parser.read(cfg_file_path)

        return self

    
    def get_cfg_file_path(self):
        
        return self.cfg_file_path


    def get_param_value(self, sect_name, param_name):
        
        return utils.safedic(utils.safedic(self.parser, sect_name), param_name)


    def is_debug_mode(self):

        return self.get_param_value("MODE", "debug") == "yes"

    
    def is_write_logs_mode(self):

        return self.get_param_value("MODE", "write_logs") == "yes"


    def is_log_to_file_mode(self):

        return self.get_param_value("LOGGING", "log_to_files") == "yes"


    def get_log_folder_path(self):

        return self.get_param_value("LOGGING", "log_folder_path")


    def is_log_to_db_mode(self):

        return self.get_param_value("LOGGING", "log_to_db") == "yes"


    def get_default_cms_session_duration(self):

        duration = self.get_param_value("CMS_SESSION", "default_duration")

        return int(utils.safeval(duration, 60))     


    def get_db_connection_params(self):

        db_connection_params = { 
            "host":     self.get_param_value("DATABASE", "host"),
            "port":     self.get_param_value("DATABASE", "port"),
            "database": self.get_param_value("DATABASE", "database"),
            "user":     self.get_param_value("DATABASE", "user"),
            "password": self.get_param_value("DATABASE", "password")
        }    

        return db_connection_params


    def get_default_admin_credentials(self):

        username = self.get_param_value("DEFAULT_ADMIN_USER", "username")
        passhash = self.get_param_value("DEFAULT_ADMIN_USER", "passhash")    

        return username, passhash