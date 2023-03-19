# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  perftask.py                                 (\(\
# Func:    Managing a task for a performer             (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class PerformerTask(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("performer_task")


    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
                .add_field(fields.StringField("performer_name"))\
                .add_field(fields.StringField("task_name"))\
                .add_field(fields.DictField("prolog"))\
                .add_field(fields.DictField("task_body"))

        return self
    

    def get_performer_name(self) -> str:

        return self.get_field_value("performer_name")
    

    def get_task_name(self) -> str:

        return self.get_field_value("task_name")
    

    def get_prolog(self) -> Dict:

        return self.get_field_value("prolog")
    

    def get_task_body(self) -> Dict:

        return self.get_field_value("task_body")
