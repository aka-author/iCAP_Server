# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  basestat_reporter.py                     (\(\
# Func:    Building basic statistical reports       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 
from kernel import status, fields, dtos, performer_shortcuts, performers, perftask, \
                     sql_select, perfoutput, grq_report_query
from debug import deb_reporter


class BasestatProcessor(performers.Processor):

    def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


    def process(self) -> None:

        print("processing...")


def new_processor(shortcut: performer_shortcuts.PerformerShortcut) -> performers.Processor:

   return BasestatProcessor(shortcut.get_chief()).set_shortcut(shortcut)