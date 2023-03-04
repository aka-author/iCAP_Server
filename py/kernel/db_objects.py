# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dbobjects.py                            (\(\
# Func:    Working with database objects           (^.^)
# # ## ### ##### ######## ############# #####################

import workers, db_instances, db_recordsets


class Table(db_recordsets.Recordset):

    def __init__(self, chief: 'Scheme', table_name: str):

        super().__init__(chief, table_name)

        self.table_name = table_name


    def get_table_name(self) -> str:

        return self.table_name
    

class Scheme(workers.Worker):

    def __init__(self, dbi, scheme_name: str):

        super().__init__(self, dbi)

        self.scheme_name = scheme_name

        self.tables = []
        self.tables_by_names = {}


    def get_scheme_name(self) -> str:

        return self.scheme_name
    

    def add_table(self, table: Table):

        self.tables.append(table)
        self.tables_by_names[table.get_table_name] = table

    
    def get_table(self, table_name: str) -> Table:

        return self.tables_by_names[table_name]