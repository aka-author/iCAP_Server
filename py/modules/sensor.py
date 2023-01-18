# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  sensor.py                          (\(\
# Func:    Modeling a sensor                  (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat


class Sensor(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.uuid = None
        self.varname = None
        self.datatype_name = None


    def load_from_ramtable_row(self, row):

        self.uuid = row.get_field_value("uuid")
        self.varname = row.get_field_value("varname")
        self.datatype_name = row.get_field_value("datatype_name")

        return self


    def get_uuid(self):

        return self.uuid


    def get_varname(self):

        return self.varname


    def get_datatype_name(self):

        return self.datatype_name