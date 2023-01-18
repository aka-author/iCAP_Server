# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  dirdesk.py                                (\(\
# Func:    Managing system directories               (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat, fields, ramtable, variable, sensor


class DirectoryDesk(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.rt_sensors = self.fetch_sensors()
        self.rt_variables = self.fetch_variables()


    def fetch_sensors(self):

        rt_sensors = ramtable.Table("icap.sensors")\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.StringField("sensor_id"))

        dbl = self.get_dbl()
        q = dbl.new_select().set_output_ramtable(rt_sensors)
        print(q.get_snippet())
        print(self.get_cfg().get_db_connection_params())
        dbl.execute(dbl.new_select().set_output_ramtable(rt_sensors))
        
        print(rt_sensors.select_by_index(0).field_values)
        return rt_sensors


    def get_sensor_by_id(self, sensor_id):

        return sensor 


    def fetch_variables(self):

        rt_variables = ramtable.Table("icap.variables")\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.StringField("varname"))\
            .add_field(fields.StringField("datatype_name"))

        dbl = self.get_dbl()
        dbl.execute(dbl.new_select().set_output_ramtable(rt_variables)) 

        return rt_variables

    
    def get_variable_by_name(self, varname):

        var = None

        rows = self.rt_variables.select_by_field_value("varname", varname)
        
        if len(rows) > 0:
            var = variable.Variable(self).load_from_ramtable_row(rows[0])

        return var 

