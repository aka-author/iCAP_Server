# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  performers.py                               (\(\
# Func:    Providing a prototype for each performer    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import workers, controllers, performer_shortcuts


class Blade(controllers.Controller):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.shortcut = None


    def get_report_ver(self) -> int:

        return self.report_ver
    

    def get_status_message(self) -> str:

        return "Success"

    
    def set_shortcut(self, shortcut: performer_shortcuts.PerformerShortcut) -> 'Blade':

        self.shortcut = shortcut

        return self


    def get_shortcut(self) -> performer_shortcuts.PerformerShortcut:

        return self.shortcut


class Admin(Blade):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def perform_admin_task(self, task_name: str, admin_task_data) -> Dict:

        return {}
    

class Processor(Blade):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def perform_processing_task(self, task_name: str, processing_task_data) -> Dict:

        return {}


class Reporter(Blade):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def build_report(self, report_name: str, assay_query_data: Dict) -> Dict:


        return {"version": 1, "wording": "test"}
    

