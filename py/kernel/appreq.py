# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  appreq.py                                 (\(\
# Func:    Managing an application request           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class AppRequest(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("app_request")


    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
                .add_field(fields.StringField("app_request_type_name"))\
                .add_field(fields.BigintField("ver"))\
                .add_field(fields.DictField("app_request_body"))

        return self


    def get_type_name(self) -> str:

        return self.get_field_value("app_request_type_name")


    def get_ver(self) -> int:

        return self.get_field_value("ver")


    def get_body(self) -> Dict:

        return self.get_field_value("app_request_body")