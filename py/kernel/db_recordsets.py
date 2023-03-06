# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  db_recordsets.py                           (\(\
# Func:    Managing something that has field manager  (^.^)
# # ## ### ##### ######## ############# #####################

import fields, sql_workers


class Recordset(sql_workers.SqlWorker):

    def __init__(self, chief: sql_workers.SqlWorker):

        super().__init__(chief)

        self.fm = None
        self.fk = None
        
       
    def get_recordset_name(self) -> str:

        return self.fk.get_recordset_name()
    

    def set_field_manager(self, fm: fields.FieldManager) -> 'Recordset':

        self.fm = fm
        self.fk = fm.get_field_keeper()

        return self


    def has_field_manager(self) -> bool:

        return self.fm is not None


    def get_field_manager(self) -> fields.FieldManager:

        return self.fm
    

    def get_field_keeper(self) -> fields.FieldKeeper:

        return self.fk