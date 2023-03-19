# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  perftask.py                                 (\(\
# Func:    Managing an output a performer returns      (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class PerformerOutput(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("performer_output")


    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
                .add_field(fields.StringField("performer_name"))\
                .add_field(fields.StringField("task_name"))\
                .add_field(fields.BigintField("status_code"))\
                .add_field(fields.StringField("status_message"))\
                .add_field(fields.DictField("prolog"))\
                .add_field(fields.DictField("output_body"))
        
        return self
    

    def set_performer_name(self, performer_name: str) -> 'PerformerOutput':

        self.set_field_value("performer_name", performer_name)

        return self
    

    def set_task_name(self, task_name: str) -> 'PerformerOutput':

        self.set_field_value("task_name", task_name)

        return self


    def set_status_code(self, status_code: int) -> 'PerformerOutput':

        self.set_field_value("status_code", status_code)

        return self
    

    def set_status_message(self, status_message: str) -> 'PerformerOutput':

        self.set_field_value("status_message", status_message)

        return self
    

    def set_prolog(self, prolog: Dict) -> 'PerformerOutput':

        self.set_field_value("prolog", prolog)

        return self
    

    def set_body(self, output_body: Dict) -> 'PerformerOutput':

        self.set_field_value("output_body", output_body)

        return self