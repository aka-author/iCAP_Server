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

        self.cfg_file_path = cfg_file_path

        self.parser.read(cfg_file_path)

        return self

    
    def get_cfg_filr_path(self):

        return self.cfg_file_path


    def get_param_value(self, sect_name, param_name):
        
        return utils.safedic(utils.safedic(self.parser, sect_name), param_name)


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