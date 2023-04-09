# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  query_results.py                          (\(\
# Func:    Fetching and iterating query results      (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import fields, ramtables, db_recordsets, sql_queries


class QueryResult(db_recordsets.Recordset):

    def __init__(self, chief: sql_queries.SelectiveQuery, fm: fields.FieldManager, cursor: object):

        super().__init__(chief)

        if fm is not None:
            self.set_field_manager(fm)

        self.cursor = cursor

        self.curr_row_index = 0
        self.eof_flag = False


    def get_query(self) -> sql_queries.SelectiveQuery:

        return self.get_chief()


    def get_cursor(self) -> object:

        return self.cursor


    def current_row_index(self):

        return self.curr_row_index
    

    def count_rows(self) -> int:

        return self.get_cursor().rowcount
    

    def is_useful(self) -> bool:

        return self.count_rows() > 0


    def set_eof_flag(self, state: bool=True) -> 'QueryResult':

        self.eof_flag = state

        return self


    def repair_value(self, raw_value, varname) -> any:

        datatype_name = self.get_field_manager().get_field(varname).get_datatype_name()
        
        return self.sql.repair_value(raw_value, datatype_name)


    def fetch_one(self) -> 'QueryResult':

        if self.curr_row_index < self.count_rows():

            row = self.get_cursor().fetchone()

            if self.has_field_manager():
                fm = self.get_field_manager()
            else:
                fm = fields.FieldManager(self.get_query().autocreate_field_keeper(row))
                self.set_field_manager(fm)

            for idx, varname in enumerate(fm.get_varnames()):   
                fm.set_field_value(varname, self.repair_value(row[idx], varname))

            self.curr_row_index += 1
        else:
            self.set_eof_flag()

        return self


    def eof(self) -> bool:

        return self.eof_flag


    def dump_ramtable(self) -> ramtables.Table:

        q = self.get_query()

        rt_dump = ramtables.Table(q.get_query_name(), q.get_field_manager().get_field_keeper())

        query_dump = self.get_cursor().fetchall() 

        buffer = {}

        for row in query_dump:

            for idx, varname in enumerate(rt_dump.fk.get_varnames()):
                buffer[varname] = self.repair_value(row[idx], varname)

            rt_dump.insert(buffer)

        return rt_dump
    

    def dump_list_of_dicts(self) -> List:

        return self.dump_ramtable().dump_list_of_dicts() 