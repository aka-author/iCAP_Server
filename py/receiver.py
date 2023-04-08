#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Level:    Application
# Module:   receiver.py                                 
# Func:     Receiving and writing measurements to a DB  (\(\
# Usage:    REST server, CGI script                     (^.^)
# # ## ### ##### ######## ############# ##################### 

from typing import Dict
import os, sys, pathlib

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/kernel"))
from kernel import dtos, restreq, restserver, users, restresp, measurements
from debug import deb_receiver


class Receiver(restserver.RestServer):

    def __init__(self, rel_cfg_file_path: str):

        super().__init__("Receiver", rel_cfg_file_path)


    def mock_cgi_input(self) -> restserver.RestServer:

        super().mock_cgi_input()
     
        deb_receiver.mock_cgi_input()

        return self


    def check_user_permissions(self, user: users.User) -> bool:

        return user.may_save_measurements()
    

    def validate_request(self, req: restreq.RestRequest) -> bool:
        
        return "measurements" in req.get_payload()


    def new_measurement_dto(self, measurement_dict: Dict) -> dtos.Dto:

        return dtos.Dto(measurement_dict).repair_datatypes()
    

    def produce_response(self, req: restreq.RestRequest) -> restresp.RestResponse:
                        
        req_payload = req.get_payload()
        
        if isinstance(req_payload, dict):
            if req_payload.get("measurements") is not None:
                for measurement_dict in req_payload.get("measurements"): 

                    source_desk = self.get_source_desk()

                    source_desk.insert_measurement(source_desk.new_measurement()\
                                    .import_dto(self.new_measurement_dto(measurement_dict))\
                                    .rebuild())

        return restresp.RestResponse()


Receiver("../cfg/fserv.ini").process_request()