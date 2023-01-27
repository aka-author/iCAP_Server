# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Level:   Kernel
# Module:  dirdesk.py                                (\(\
# Func:    Managing system directories               (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat, fields, ramtable, variable, sensor


class DirectoryDesk(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.rt_sensors = self.fetch_sensors()
        self.rt_variables = self.fetch_variables()


    # Sensors

    def fetch_sensors(self):

        rt_sensors = ramtable.Table("icap.sensors")\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.StringField("sensor_id"))

        dbl = self.get_dbl()

        dbl.execute(dbl.new_select().set_output_ramtable(rt_sensors))
        
        return rt_sensors


    def get_sensor_by_id(self, sensor_id):

        sn = None

        rows = self.rt_sensors.select_by_field_value("sensor_id", sensor_id)
        
        if len(rows) > 0:
            sn = sensor.Sensor(self).load_from_ramtable_row(rows[0])

        return sn 


    # Variables

    def fetch_variables(self):

        rt_variables = ramtable.Table("icap.variables")\
            .add_field(fields.UuidField("uuid"))\
            .add_field(variable.VarnameField("varname"))\
            .add_field(fields.StringField("datatype_name"))\
            .add_field(fields.StringField("shortcut"))

        dbl = self.get_dbl()
        q = dbl.new_select().set_output_ramtable(rt_variables)
        dbl.execute(q) 

        return rt_variables

    
    def get_variable_by_name(self, varname):

        var = None

        rows = self.rt_variables.select_by_field_value("varname", varname)
        
        if len(rows) > 0:
            var = variable.Variable(self).load_from_ramtable_row(rows[0])

        return var 