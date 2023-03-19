# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  basestat_reporter.py                     (\(\
# Func:    Building basic statistical reports       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 
from kernel import performer_shortcuts, performers, perftask, perfoutput
from debug import deb_reporter


class BasestatReporter(performers.Reporter):

   def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


   def perform_task(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

      perf_out = perfoutput.PerformerOutput(self)\
                  .set_performer_name(task.get_performer_name())\
                  .set_task_name(task.get_task_name())\
                  .set_status_code(0)\
                  .set_status_message("Success")\
                  .set_prolog({})\
                  .set_body(task.get_output_template())

      return perf_out


def new_reporter(shortcut: performer_shortcuts.PerformerShortcut) -> performers.Reporter:

   return BasestatReporter(shortcut.get_chief()).set_shortcut(shortcut)




