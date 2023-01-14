# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  ramtable.py                              (\(\
# Func:    Simulating database tables in memory     (^.^)
# # ## ### ##### ######## ############# #####################


class Row:

    def __init__(self, table):

        self.table = table
        self.field_values = {}

    
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
        self.arg_field_names = []
        self.mandatory_field_names = []
        self.rows = []


    def get_table_name(self):

        return self.table_name


    def count_fields(self):

        return len(self.fields)


    def has_field(self, field_name):

        return field_name in self.fields


    def get_field_names(self):

        return self.fields.keys() 


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


    def add_field(self, field, field_subset="out", mandatority="optional"):

        self.fields[field.get_varname()] = field

        if field_subset == "arg":
            self.define_argument(field.get_varname())

        if mandatority == "mandatory" or field_subset == "arg":
            self.define_mandatory(field.get_varname())

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
    

    def insert_from_dic(self, src_dic):

        row = self.create_blank_row()

        for field_name in src_dic:
            if self.has_field(field_name):
                row.set_field_value(field_name, self.get_field(field_name).import_from_dic(src_dic[field_name]))

        self.rows.append(row)

        return self
        

    def select_by_index(self, idx):

        return self.rows[idx]


    def union(self, table):

        self.rows + table.rows

        return self