# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  assayreq.py                              (\(\
# Func:    Managing analytical requests             (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, workers, models


class AssayRequest(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("assay_request")

        self.shop_name = None
        self.report_name = None
        self.payload = None


    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
                .add_field(fields.StringField("shop_name"))\
                .add_field(fields.StringField("report_name"))\
                .add_field(fields.DictField("payload"))

        return self


    def get_shop_name(self) -> str:

        return self.get_field_value("shop_name")


    def get_report_name(self) -> str:

        return self.get_field_value("report_name")


    def get_payload(self) -> Dict:

        return self.get_field_value("payload")