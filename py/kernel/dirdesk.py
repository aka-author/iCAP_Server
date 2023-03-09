# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dirdesk.py                                (\(\
# Func:    Managing system directories               (^.^)
# # ## ### ##### ######## ############# #####################

import desks, sensors, variables


class DirectoryDesk(desks.Desk):

    def __init__(self, chief):

        super().__init__(chief)

        self.sensors, self.sensors_by_ids = self.fetch_sensors()
        self.variables, self.variables_by_names = self.fetch_variables()
        

    # Sensors

    def fetch_sensors(self) -> 'DirectoryDesk':
        print("default db", self.get_default_db())
        loaded_sensors = sensors.Sensor(self).load_all(self.get_default_db()) 

        sensors_by_ids = {}

        for sensor in loaded_sensors:
            sensors_by_ids[sensor.get_field_value("sensor_id")] = sensor

        return loaded_sensors, sensors_by_ids


    def get_sensor_by_id(self, sensor_id: str) -> sensors.Sensor:

        return self.sensors_by_ids.get(sensor_id)


    # Variables

    def fetch_variables(self) -> 'DirectoryDesk':

        loaded_variables = variables.Variable(self).load_all(self.get_default_db())

        variables_by_names = {}

        for variable in loaded_variables:
            print(variable.get_field_value("varname"))
            variables_by_names[variable.get_field_value("varname")] = variable

        return loaded_variables, variables_by_names

    
    def get_variable_by_name(self, varname: str) -> variables.Variable:

        return self.variables_by_names.get(varname)