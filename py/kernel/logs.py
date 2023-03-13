# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  logs.py                                (\(\
# Func:    Writing to logs                        (^.^)
# # ## ### ##### ######## ############# #####################

import utils, workers, ramtables, fields


LOG_INFO    = "INFO"
LOG_WARNING = "WARNING"
LOG_ERROR   = "ERROR"
LOG_DEBUG   = "DEBUG"

class Logger(workers.Worker):

    def __init__(self, chief=None):
        
        super().__init__(chief)

        self.log_file_path = self.get_app().get_log_file_path()
        self.log_file = open(self.log_file_path, "a") if self.get_app().is_log_to_file_mode() else None
        self.log(LOG_INFO, "Start")


    def get_logfile_path(self):

        return self.get_log_file_name()


    def assemble_log_record(self, logrec_type, wording, details=""):

        return "\t".join([self.get_app().get_launch_id(), 
                         utils.strnow(), 
                         self.get_app().get_app_name(), 
                         logrec_type, wording, details])


    def assemble_log_ramtable(self, record_type, wording, details=""):

        fk = fields.FieldKeeper()\
                .add_field(fields.StringField("launch_id"))\
                .add_field(fields.StringField("writer_name"))\
                .add_field(fields.StringField("record_type"))\
                .add_field(fields.StringField("wording"))\
                .add_field(fields.StringField("details"))

        return ramtables.Table("log_records", fk)\
                    .insert({"session_id": self.get_app().get_launch_id(),
                             "writer_name": self.get_app().get_app_name(), 
                             "record_type": record_type, 
                             "wording": wording,
                             "details": details})


    def log(self, record_type, wording, details=""):
        
        if record_type != LOG_DEBUG or self.is_debug_mode():
            
            if self.get_app().is_log_to_file_mode():
                self.log_file.write(self.assemble_log_record(record_type, wording, details).replace("\n", '\\n') + "\n")

            if self.get_app().is_log_to_db_mode():
                rt_rec = self.assemble_log_ramtable(record_type, wording, details)
                dbms = self.get_default_dbms()
                qr = dbms.new_query_runner(self.get_default_db())
                qi = dbms.new_insert().build_of_field_manager(rt_rec.select_by_index(0).fm, "log_records", self.get_default_db_scheme_name())
                try:
                    qr.execute_query(qi).commit().close()
                except:
                    pass
            
        return self


    def console(self, message):

        if self.is_console_mode():
            print(message)


    def close_all(self):
        
        self.log(LOG_INFO, "Finish")
        
        if self.get_app().is_log_to_file_mode():
            self.log_file.close()