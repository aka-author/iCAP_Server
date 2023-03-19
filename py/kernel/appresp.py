# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  appresp.py                                  (\(\
# Func:    Managing an application response            (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class AppResponse(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("app_response")


    def define_fields(self) -> models.Model:

        self.get_field_manager()\
            .add_field(fields.StringField("app_response_type_name"))\
            .add_field(fields.StringField("ver"))\
            .add_field(fields.TimestampField("started_at"))\
            .add_field(fields.TimestampField("finished_at"))\
            .add_field(fields.BigintField("duration"))\
            .add_field(fields.DictField("app_response_body"))

        return self


    def set_type_name(self, type_name: str) -> 'AppResponse':

        self.set_field_value("app_response_type_name", type_name)

        return self
    

    def set_ver(self, ver: str) -> 'AppResponse':

        self.set_field_value("ver", ver)

        return self
    

    def set_started_at(self, started_at ) -> 'AppResponse':

        self.set_field_value("started_at", started_at)

        return self
    

    def set_finished_at(self, finished_at) -> 'AppResponse':

        self.set_field_value("started_at", finished_at)

        return self
    

    def set_duration(self, duration: int) -> 'AppResponse':

        self.set_field_value("duration", duration)

        return self
    

    def set_body(self, app_response_body: Dict) -> 'AppResponse':

        self.set_field_value("app_response_body", app_response_body)

        return self
        
