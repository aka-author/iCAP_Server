# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  query_results.py                          (\(\
# Func:    Fetching and iterating query results      (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import fields, ramtables, db_recordsets


class QueryResult(db_recordsets.Recordset):

    def __init__(self, chief, fk: fields.FieldKeeper, cursor: object):

        super().__init__(chief)

        self.fk = fk
        self.fm = fields.FieldManager(fk)
        self.cursor = cursor

        self.eof_flag = False


    def get_cursor(self) -> object:

        return self.cursor


    def set_eof_flag(self, state: bool=True) -> 'QueryResult':

        self.eof_flag = state

        return self


    def repair_value(self, raw_value, varname) -> any:

        datatype_name = self.get_field_manager().get_field(varname).get_datatype_name()
        
        return self.sql.repair_value(raw_value, datatype_name)


    def fetch_one(self) -> 'QueryResult':

        row = self.get_cursor().fetchone()

        fm = self.get_field_manager()

        if row is not None:
            for idx, varname in enumerate(fm.get_varnames()):   
                fm.set_field_value(varname, self.repair_value(row[idx]), varname) 
        else:
            self.set_eof_flag()

        return self


    def get_current_row(self) -> Dict:

        return self.fm.get_field_values()


    def eof(self) -> bool:

        return self.eof_flag


    def dump(self) -> ramtables.Table:

        rt_dump = ramtables.Table()

        query_dump = self.get_cursor().fetchall() 

        buffer = {}

        for row in query_dump:

            for field_idx, varname in enumerate(rt_dump.fk.get_varnames()):
                buffer[varname] = row[field_idx]

            rt_dump.insert(buffer)

        return rt_dump