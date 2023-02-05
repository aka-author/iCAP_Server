# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  ramtable.py                              (\(\
# Func:    Simulating database tables in memory     (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
import utils, fields


class Row:

    def __init__(self, table):

        self.id = str(uuid.uuid4())
        
        self.table = table

        self.fm = fields.FieldManager(self, table.get_field_keeper()).reset_field_values()

        print(self.fm.count_fields())

    
    def get_id(self):

        return self.id


    def get_table(self):

        return self.table


    def move_to_table(self, table):

        self.table = table
        self.fm.set_field_keeper(table.get_field_keeper())


    def __str__(self):

        t = self.get_table()

        return " ".join([t.fm.get_field(vn).get_serialized_value(self.fm.get_field_value(vn)) \
                         for vn in t.fm.fields_by_varnames])


class Table:

    def __init__(self, table_name):

        self.table_name = table_name

        self.fm = fields.FieldManager(self)

        self.rows = []
        self.rows_by_ids = {}


    def get_table_name(self):

        return self.table_name


    def get_field_keeper(self):

        return self.fm.fk


    def count_rows(self):

        return len(self.rows) 


    def create_blank_row(self):

        return Row(self)
    

    def insert(self, field_values={}):

        row = self.create_blank_row()
        print(row.fm.get_field("weight"))
        self.rows.append(row)
        row.fm.set_field_values(field_values)
        print(field_values)
        #self.rows.append(row)
        self.rows_by_ids[row.get_id()] = row

        return self
        

    def select_by_index(self, idx):

        return self.rows[idx]


    def select_by_id(self, id):

        return utils.safedic(self.rows_by_ids, id)


    def select_by_field_value(self, field_name, target_value):
        
        return [row for row in self.rows if row.fm.eq_field_value(field_name, target_value)]


    def union(self, table):

        for idx in range(0, table.count_rows()):
            table.select_by_index(idx).move_to_table(self)

        self.rows = self.rows + table.rows
        self.rows_by_ids = {**self.rows_by_ids, **table.rows_by_ids}

        return self


    def get_field_values(self, field_name):

        return [self.select_by_index(r).get_field_value(field_name) for r in range(0, self.count_rows())]


    def delete_all(self):

        self.rows = []


    def __str__(self):

        return " ".join([fn for fn in self.fields]) + "\n" + "\n".join([row.__str__() for row in self.rows])