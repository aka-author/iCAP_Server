# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  perfreq.py                              (\(\
# Func:    Managing requests to performers         (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class PerformerRequest(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("performer_request")

        self.performer_name = None
        self.task_name = None
        self.payload = None


    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
                .add_field(fields.StringField("ver"))\
                .add_field(fields.StringField("performer_name"))\
                .add_field(fields.StringField("task_name"))\
                .add_field(fields.DictField("payload"))

        return self


    def get_performer_name(self) -> str:

        return self.get_field_value("performer_name")


    def get_task_name(self) -> str:

        return self.get_field_value("task_name")


    def get_payload(self) -> Dict:

        return self.get_field_value("payload")