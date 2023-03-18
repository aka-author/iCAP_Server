# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  perfresp.py                              (\(\
# Func:    Managing a performer response            (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class PerformerResponse(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("performer_response")


    def define_fields(self) -> models.Model:

        self.get_field_manager()\
            .add_field(fields.StringField("ver"))\
            .add_field(fields.BigintField("status_code"))\
            .add_field(fields.StringField("status_message"))\
            .add_field(fields.StringField("performer_name"))\
            .add_field(fields.StringField("task_name"))\
            .add_field(fields.TimestampField("started_at"))\
            .add_field(fields.TimestampField("finished_at"))\
            .add_field(fields.BigintField("duration"))\
            .add_field(fields.DictField("payload"))

        return self


    def set_ver(self, ver: str) -> 'PerformerResponse':

        self.set_field_value("ver", ver)

        return self
    

    def set_status_code(self, status_code: int) -> 'PerformerResponse':

        super().set_status_code(status_code)
        self.set_field_value("status_code", status_code)

        return self
    

    def set_status_message(self, status_message: str) -> 'PerformerResponse':

        self.set_field_value("status_message", status_message)

        return self


    def set_performer_name(self, performer_name: str) -> 'PerformerResponse':

        self.set_field_value("performer_name", performer_name)

        return self
    

    def set_task_name(self, task_name: str) -> 'PerformerResponse':

        self.set_field_value("task_name", task_name)

        return self
    

    def set_started_at(self, started_at ) -> 'PerformerResponse':

        self.set_field_value("started_at", started_at)

        return self
    

    def set_finished_at(self, finished_at) -> 'PerformerResponse':

        self.set_field_value("started_at", finished_at)

        return self
    

    def set_duration(self, duration: int) -> 'PerformerResponse':

        self.set_field_value("duration", duration)

        return self
    

    def set_payload(self, payload: Dict) -> 'PerformerResponse':

        self.set_field_value("payload", payload)

        return self


    def get_payload(self) -> Dict:

        return self.get_field_value("payload")
    

class FailurePerformerResponse(PerformerResponse):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        failure_info = {
            "status_code":      1,
            "status_wording":   "Failure"
        }

        self.set_payload(failure_info)
