# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  assay_responses.py                        (\(\
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
                .add_field(fields.DictField("assay_response_content"))

        return self


    def set_assay_response_content(self, assay_response_content: Dict) -> 'AssayResponse':

        self.set_field_value("assay_response_content", assay_response_content)

        return self


    def get_assay_response_content(self) -> Dict:

        return self.get_field_value("assay_response_content")
    

class FailureAssayResponse(AssayResponse):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        content = {
            "status_code": 1,
            "status_wording": "Failure"
        }

        self.set_assay_response_content(content)
