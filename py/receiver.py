#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Level:   Application
# Module:  receiver.py                               (\(\
# Func:    Saving measurements to a database         (^.^)
# # ## ### ##### ######## ############# ##################### 

from typing import Dict
import os, sys, pathlib

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import dtos, restserver, restreq, restresp, measurements
from debug import deb_receiver


class Receiver(restserver.RestServer):

    def __init__(self, rel_cfg_file_path: str):

        super().__init__("Receiver", rel_cfg_file_path)


    def mock_cgi_input(self) -> restserver.RestServer:

        super().mock_cgi_input()
     
        deb_receiver.mock_cgi_input()

        return self


    def auth_client(self, req: restreq.RestRequest) -> bool:

        return True
    

    def validate_request(self, req: restreq.RestRequest) -> bool:
        
        return "measurements" in req.get_payload()


    def new_measurement_dto(self, measurement_dict: Dict) -> dtos.Dto:

        return dtos.Dto(measurement_dict).repair_datatypes()
    

    def do_the_job(self, req: restreq.RestRequest) -> restresp.RestResponse:
                        
        for measurement_dict in req.get_payload().get("measurements"): 

            measurement_dto = self.new_measurement_dto(measurement_dict)
            
            measurement = measurements.Measurement(self)\
                            .import_dto(measurement_dto)\
                            .rebuild()

            if measurement.is_valid() and measurement.is_unique():
                measurement.insert()

        return restresp.RestResponse()


Receiver("../cfg/fserv.ini").process_request()