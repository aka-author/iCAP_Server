# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  basestat_reporter.py                     (\(\
# Func:    Building basic statistical reports       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/kernel"))
import shops


class BasestatReporter(shops.ShopReporter):

   def __init__(self, chief):

      super().__init__(chief)


   def build_report(self, report_name, assay_query_data) -> Dict:

      return {"report_name": report_name}


def new_shop_reporter(chief):

   return BasestatReporter(chief)




