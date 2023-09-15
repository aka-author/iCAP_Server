# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Performer (System)
# Module:  system_admin.py                        (\(\
# Func:    Dispatching administrative tasks       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 
from kernel import status, fields, dtos, performer_shortcuts, performers, perftask, \
                     sql_select, perfoutput, grq_report_query, performer_desks


class SystemAdmin(performers.Reporter):

   def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


   def preprocess(self, report_query_dict: Dict) -> Dict:

      preprocess_report_dict = {"result": "done"}

      performer_desk = performer_desks.PerformerDesk(self)

      for perf_name in performer_desk.get_performer_names():
         perf_blade = performer_desk.involve_processor(perf_name)
         if perf_blade is not None:
            perf_blade.process()

      return preprocess_report_dict


   # Performer's main

   def perform_task(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

      task_body = task.get_task_body()

      status_code = status.OK
      status_message = status.MSG_SUCCESS
      out_prolog = out_body = None
      
      if task.get_task_name() == "preprocess":
         out_body = self.preprocess(task_body)        
      else:
         status_code = status.ERR_UNKNOWN_TASK 
         status_message = status.MSG_UNKNOWN_TASK

      perf_out = perfoutput.PerformerOutput(self)\
                     .set_performer_name(task.get_performer_name())\
                     .set_task_name(task.get_task_name())\
                     .set_status_code(status_code)\
                     .set_status_message(status_message)\
                     .set_prolog(out_prolog)\
                     .set_body(out_body)
      
      return perf_out 


def new_admin(shortcut: performer_shortcuts.PerformerShortcut) -> performers.Reporter:
   
   return SystemAdmin(shortcut.get_chief()).set_shortcut(shortcut)