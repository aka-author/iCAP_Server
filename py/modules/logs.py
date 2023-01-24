# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  logs.py                                (\(\
# Func:    Writing to logs                        (^.^)
# # ## ### ##### ######## ############# #####################

import utils, bureaucrat, ramtable, fields


LOG_INFO    = "INFO   "
LOG_WARNING = "WARNING"
LOG_ERROR   = "ERROR  "
LOG_DEBUG   = "DEBUG  "

class Logger(bureaucrat.Bureaucrat):

    def __init__(self, chief=None):
        
        super().__init__(chief)

        self.log_file_path = self.get_app().get_log_file_path()
        self.log_file = open(self.log_file_path, "a") if self.get_cfg().is_log_to_file_mode() else None
        self.log(LOG_INFO, "Start")


    def get_logfile_path(self):

        return self.get_log_file_name()


    def assemble_log_record(self, logrec_type, wording, details=""):

        return " ".join([self.get_app().get_session_id(), 
                         utils.strnow(), 
                         self.get_app().get_app_name(), 
                         logrec_type, wording, details])


    def assemble_log_ramtable(self, record_type, wording, details=""):

        return ramtable.Table("log_records")\
                .add_field(fields.StringField("session_id"))\
                .add_field(fields.StringField("writer_name"))\
                .add_field(fields.StringField("record_type"))\
                .add_field(fields.StringField("wording"))\
                .add_field(fields.StringField("details"))\
                    .insert({"session_id": self.get_app().get_session_id(),
                             "writer_name": self.get_app().get_app_name(), 
                             "record_type": record_type, 
                             "wording": wording,
                             "details": details})


    def log(self, record_type, wording, details=""):

        if record_type != LOG_DEBUG or self.get_cfg().is_debug_mode():
            
            if self.get_cfg().is_log_to_file_mode():
                self.log_file.write(self.assemble_log_record(record_type, wording, details) + "\n")

            if self.get_cfg().is_log_to_db_mode():
                rt_rec = self.assemble_log_ramtable(record_type, wording, details)
                dbl = self.get_dbl()
                dbl.execute(dbl.new_script("logs", "icap").import_source_ramtable(rt_rec)).commit()

        return self


    def console(self, message):

        if self.get_cfg().is_console_mode():
            print(message)


    def __del__(self):

        self.log(LOG_INFO, "Finish")

        if self.get_cfg().is_log_to_file_mode():
            self.log_file.close()