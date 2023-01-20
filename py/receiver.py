#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  receiver.py                               (\(\
# Func:    Saving measurements to a database         (^.^)
# # ## ### ##### ######## ############# ##################### 

import os, sys, pathlib 

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/modules"))

from modules import restserver, measurement
from debug import deb_receiver


class Receiver(restserver.RestServer):

    def __init__(self, rel_cfg_file_path):

        super().__init__(rel_cfg_file_path)

        self.log_file_name = "receiver.log"


    def do_the_job(self, request):

        payload = request.get_payload()

        if "measurements" in payload:
        
            measurements_dtos = payload["measurements"]

            rt_measurements = rt_varvalues = None 

            for dto in measurements_dtos: 

                m = measurement.Measurement(self).import_dto(dto)

                rt_m = m.get_measurement_ramtable()
                rt_measurements = rt_m if rt_measurements is None else rt_measurements.union(rt_m) 

                rt_v = m.get_varvalues_ramtable()
                rt_varvalues = rt_v if rt_varvalues is None else rt_varvalues.union(rt_v)

            mydbl = self.get_dbl() 

            scr = mydbl.new_script("insert_measurements", "icap")
            scr.import_source_ramtable(rt_measurements).import_source_ramtable(rt_varvalues)
            
            if self.is_debug_mode():
                print(rt_measurements)
                print(scr.get_snippet())
            
            mydbl.execute(scr).commit()

            if self.is_write_logs_mode():
                log_file = open(self.get_log_file_path(), "a")
                log_file.write(str(self.get_req().get_payload()));
                log_file.write("\n");


    def get_debug_request_body(self):

        return deb_receiver.get_body()
    

Receiver("../cfg/fserv.ini").process_request()





