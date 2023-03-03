# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  db_recordsets.py                           (\(\
# Func:    Arranging fields into named field groups   (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import utils, fields, db_objects, sql_workers


class Recordset(sql_workers.SqlWorker):

    def __init__(self, chief: sql_workers.SqlWorker, recordset_name: str):

        super().__init__(chief)

        self.fk = fields.FieldKeeper(recordset_name)
        self.fm = fields.FieldManager(self.fk)

       
    def get_recordset_name(self) -> str:

        return self.fk.get_recordset_name()


    