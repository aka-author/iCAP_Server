# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  assayresp.py                              (\(\
# Func:    Managing an analytical response           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class AssayResponse(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("assay_response")


    def define_fields(self) -> models.Model:

        self.get_field_manager()\
                .add_field(fields.DictField("payload"))

        return self


    def set_payload(self, payload: Dict) -> 'AssayResponse':

        self.set_field_value("payload", payload)

        return self


    def get_payload(self) -> Dict:

        return self.get_field_value("payload")
    

class FailureAssayResponse(AssayResponse):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        failure_info = {
            "status_code":      1,
            "status_wording":   "Failure"
        }

        self.set_payload(failure_info)
