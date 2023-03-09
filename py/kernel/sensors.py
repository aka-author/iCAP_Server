# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sensors.py                         (\(\
# Func:    Managing a sensor                  (^.^)
# # ## ### ##### ######## ############# #####################

import fields, models, dirdesk


class Sensor(models.Model):

    def __init__(self, chief: 'dirdesk.DirectoryDesk'):

        super().__init__(chief)

        self.set_model_name("sensor")

    
    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.StringField("sensor_id"))

        return self