# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  cfg.py                                  (\(\
# Func:    Retrieving configuration parameters     (^.^)                                                                                                                                                                        
# # ## ### ##### ######## ############# #####################

import configparser


class Cfg:

    def __init__(self, cfg_file_path):

        self.cfg_file_path = cfg_file_path

        self.parser = configparser.ConfigParser()
        self.parser.read(self.get_cfg_file_path())


    def get_cfg_file_path(self):

        return self.cfg_file_path

    
    def get_param_value(self, sect_name, param_name):

        param_value = None

        if sect_name in self.parser:
            if param_name in self.parser[sect_name]:
                param_value = self.parser[sect_name][param_name]

        return param_value


    def get_default_cms_session_duration(self):

        duration = self.get_param_value("CMS_SESSION", "duration")

        return int(duration) if duration is not None else 60     


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