# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  performers.py                               (\(\
# Func:    Providing a prototype for each performer    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import workers, controllers, performer_shortcuts, perftask, perfoutput


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
    

