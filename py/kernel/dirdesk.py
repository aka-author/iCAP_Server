# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dirdesk.py                                (\(\
# Func:    Managing system directories               (^.^)
# # ## ### ##### ######## ############# #####################

import workers, desks, sensors, variables


class DirectoryDesk(desks.Desk):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.sensors, self.sensors_by_ids = self.load_sensors()
        self.variables, self.variables_by_names = self.load_variables()
        

    # Sensors

    def load_sensors(self) -> 'DirectoryDesk':
        
        loaded_sensors = sensors.Sensor(self).load_all() 

        sensors_by_ids = {}

        for sensor in loaded_sensors:
            sensors_by_ids[sensor.get_field_value("sensor_id")] = sensor

        return loaded_sensors, sensors_by_ids


    def get_sensor_by_id(self, sensor_id: str) -> sensors.Sensor:

        return self.sensors_by_ids.get(sensor_id)


    # Variables

    def load_variables(self) -> 'DirectoryDesk':

        loaded_variables = variables.Variable(self).load_all()

        variables_by_names = {}

        for variable in loaded_variables:
            variables_by_names[variable.get_field_value("varname")] = variable

        return loaded_variables, variables_by_names

    
    def check_varname(self, varname: str) -> bool:

        return varname in self.variables_by_names
    

    def get_variable_by_name(self, varname: str) -> variables.Variable:

        return self.variables_by_names.get(varname)