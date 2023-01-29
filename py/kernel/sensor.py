# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sensor.py                          (\(\
# Func:    Modeling a sensor                  (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat


class Sensor(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.uuid = None
        self.sensor_id = None


    def load_from_ramtable_row(self, row):

        self.uuid = row.get_field_value("uuid")
        self.sensor_id = row.get_field_value("sensor_id")

        return self


    def get_uuid(self):

        return self.uuid


    def get_sensor_id(self):

        return self.sensor_id