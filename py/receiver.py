#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  receiver.py                               (\(\
# Func:    Saving measurements to a database         (^.^)
# # ## ### ##### ######## ############# ##################### 

import cgi, os, sys, math, json 
from distutils.command.config import config
from modules import script, measurement


class Receiver(script.Script):

    def do_the_job(self, request):

        measurements_dtos = request.get_payload()

        m_rt = self.create_measurements_ramtable()
        v_rt = self.create_varvalues_ramtable()

        for dto in measurements_dtos: 
            m = measurement.Measurement().import_dto(dto)
            m_rt.union(m.get_measurement_ramtable())
            v_rt.union(m.get_varvalues_ramtable())

        m_query = dbl.Query()
        m_query.    



        log_file = open("log.txt", "a")

        log_file.write(str(self.get_req().get_payload()));

        log_file.write("\n");

Receiver().process_request()





