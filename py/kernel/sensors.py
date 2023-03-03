# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sensor.py                          (\(\
# Func:    Modeling a sensor                  (^.^)
# # ## ### ##### ######## ############# #####################

import fields, models


class Sensor(models.Model):

    def __init__(self, chief):

        super().__init__(chief)

        self.set_model_name("sensor")

    
    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
            .add_field(fields.UuidField("uuid"))\
            .add_fiels(fields.StringField("sensor_id"))

        return self