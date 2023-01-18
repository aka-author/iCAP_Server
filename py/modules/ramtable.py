# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  ramtable.py                              (\(\
# Func:    Simulating database tables in memory     (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
import utils


class Row:

    def __init__(self, table):

        self.id = str(uuid.uuid4())
        self.table = table
        self.field_values = {}

    
    def get_id(self):

        return self.id


    def get_table(self):

        return self.table


    def set_field_value(self, field_name, native_value):

        self.field_values[field_name] = native_value

        return self


    def get_field_value(self, field_value):

        return self.field_values[field_value]


class Table:

    def __init__(self, table_name):

        self.table_name = table_name

        self.fields = {}
        self.field_names = []
        self.arg_field_names = []
        self.mandatory_field_names = []
        self.autoins_field_names = []
        self.rows = []
        self.rows_by_ids = {}


    def get_table_name(self):

        return self.table_name


    def count_fields(self):

        return len(self.fields)


    def has_field(self, field_name):

        return field_name in self.fields


    def get_field_names(self):

        return self.field_names 


    def get_field(self, field_name):

        return self.fields[field_name]


    def define_argument(self, field_name):

        self.arg_field_names.append(field_name)

        return self


    def is_argument(self, field_name):

        return field_name in self.arg_field_names


    def define_mandatory(self, field_name):

        self.mandatory_field_names.append(field_name)

        return self


    def is_mandatory(self, field_name):

        return field_name in self.mandatory_field_names


    def define_autoins(self, field_name):

        self.autoins_field_names.append(field_name)


    def is_insertable(self, field_name):

        return not (field_name in self.autoins_field_names)


    def add_field(self, field, options="optional"):

        varname = field.get_varname()

        self.fields[varname] = field

        if "arg" in options:
            self.define_argument(varname)

        if "mandatory" in options or "arg" in options:
            self.define_mandatory(varname)

        if "autoins" in options:
            self.define_autoins(varname)

        self.field_names.append(varname)

        return self


    def count_rows(self):

        return len(self.rows) 


    def create_blank_row(self):

        blank_row = Row(self)

        for field_name in self.fields:

            field = self.get_field(field_name)
            
            blank_row.set_field_value(field_name, \
                field.get_zero_value() \
                if self.is_mandatory(field_name) and not field.has_explicit_default_value() \
                else field.get_default_value())

        return blank_row
    

    def insert(self, src_dic):

        row = self.create_blank_row()

        for field_name in src_dic:
            if self.has_field(field_name):
                row.set_field_value(field_name, self.get_field(field_name).import_from_dic(src_dic[field_name]))

        self.rows.append(row)
        self.rows_by_ids[row.get_id()] = row

        return self
        

    def select_by_index(self, idx):

        return self.rows[idx]


    def select_by_id(self, id):

        return utils.safedic(self.rows_by_ids, id)


    def select_by_field_value(self, field_name, target_value):

        field = self.get_field(field_name)

        return [row for row in self.rows \
                if field.eq(row.get_field_value(field_name), target_value)]


    def union(self, table):

        self.rows = self.rows + table.rows
        self.rows_by_ids = {**self.rows_by_ids, **table.rows_by_ids}

        return self


    def delete_all(self):

        self.rows = []