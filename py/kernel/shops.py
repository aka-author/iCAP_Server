# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shops.py                                    (\(\
# Func:    Providing a prototype for each assay shop   (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import workers, controllers


class ShopAdmin(controllers.Controller):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def perform_admin_task(self, task_name: str, admin_task_data) -> Dict:

        return {}
    

class ShopProcessor(controllers.Controller):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def perform_processing_task(self, task_name: str, processing_task_data) -> Dict:

        return {}


class ShopReporter(controllers.Controller):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def build_report(self, report_name: str, assay_query_data: Dict) -> Dict:


        return {"version": 1, "wording": "test"}
    

