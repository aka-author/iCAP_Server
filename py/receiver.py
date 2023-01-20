#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  receiver.py                               (\(\
# Func:    Saving measurements to a database         (^.^)
# # ## ### ##### ######## ############# ##################### 

import os, sys, pathlib 

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/modules"))

from modules import restserver, measurement, fields, ramtable
from debug import deb_receiver


class Receiver(restserver.RestServer):

    def __init__(self, rel_cfg_file_path):

        super().__init__(rel_cfg_file_path)

        self.debug_mode_flag = True


    def create_measurements_ramtable(self):

        rt = ramtable.Table("icap.measurements")\
        .add_field(fields.TimestampField("accepted_at"))\
        .add_field(fields.UuidField("sensor_uuid"))\
        .add_field(fields.StringField("sensor_id_deb"))\

        return rt


    def create_varvalues_ramtable(self):

        rt = ramtable.Table("icap.varvalues")\
        .add_field(fields.UuidField("measurement_uuid"))\
        .add_field(fields.UuidField("variable_uuid"))\
        .add_field(fields.StringField("varname_deb"))\
        .add_field(fields.StringField("serialized_value"))

        return rt


    def do_the_job(self, request):

        measurements_dtos = request.get_payload()["measurements"]

        rt_measurements = self.create_measurements_ramtable()
        rt_varvalues = self.create_varvalues_ramtable()

        for dto in measurements_dtos: 
            m = measurement.Measurement(self).import_dto(dto)
            rt_measurements.union(m.get_measurement_ramtable())
            rt_varvalues.union(m.get_varvalues_ramtable())

        mydbl = self.get_dbl() 
        scr = mydbl.new_script("insmeas", "icap")
        scr.import_source_ramtable(rt_measurements).import_source_ramtable(rt_varvalues)
        print(scr.get_snippet())
        # mydbl.execute(scr).commit()

        # log_file = open("log.txt", "a")
        # log_file.write(str(self.get_req().get_payload()));
        # log_file.write("\n");


    def get_debug_request_body(self):

        return deb_receiver.get_body()
    

Receiver("../cfg/fserv.ini").process_request()





