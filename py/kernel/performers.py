# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  performers.py                               (\(\
# Func:    Providing a prototype for each performer    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import status, workers, controllers, performer_shortcuts, perftask, perfoutput


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
    

    def error_unknown_task(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

        err_perf_out = perfoutput.PerformerOutput(self)\
                        .set_performer_name(task.get_performer_name())\
                        .set_task_name(task.get_task_name())\
                        .set_status_code(status.ERR_UNKNOWN_TASK)\
                        .set_status_message(status.MSG_UNKNOWN_TASK)

        return err_perf_out
    

    def perform_task(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

        return perfoutput.PerformerOutput(self)


class Admin(Blade):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)
    

class Processor(Blade):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


class Reporter(Blade):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)
    

