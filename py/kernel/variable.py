# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  variable.py                               (\(\
# Func:    Modeling a variable                       (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat, fields


class VarnameField(fields.StringField):

    def eq(self, val1, val2):
        
        res = False

        if val1.endswith(".*") and not val2.endswith(".*"):
            res = val2.startswith(val1.split(".*")[0])
        elif not val1.endswith(".*") and val2.endswith(".*"):
            res = val1.startswith(val2.split(".*")[0])
        elif val1.endswith(".*") and val2.endswith(".*"):
            res = False
        else:
            res = super().eq(val1, val2)

        return res


class Variable(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.uuid = None
        self.varname = None
        self.datatype_name = None
        self.shortcut = None


    def load_from_ramtable_row(self, row):

        self.uuid = row.get_field_value("uuid")
        self.varname = row.get_field_value("varname")
        self.datatype_name = row.get_field_value("datatype_name")
        self.shortcut = row.get_field_value("shortcut")

        return self


    def get_uuid(self):

        return self.uuid


    def get_varname(self):

        return self.varname


    def get_datatype_name(self):

        return self.datatype_name


    def get_sql_datatype_name(self):

        return self.get_dbl().get_dbms().get_sql_datatype_name(self.get_datatype_name())


    def get_sql_varname(self):

        return self.get_dbl().get_dbms().varname2sql(self.get_varname())


    def get_shortcut(self):

        return self.shortcut