# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  measurement.py                             (\(\
# Func:    Mamaging data fields                       (^.^)
# # ## ### ##### ######## ############# #####################

import uuid, datetime
import fields, model, ramtable, dirdesk


class VarValue(model.Model):

    def __init__(self, measurement):

        super().__init__(measurement, "varvalue")

        self.varname = None
        self.parsable_value = None


    def import_dto(self, dto):
        
        self.varname = dto["varName"]
        self.parsable_value = dto["parsableValue"]

        return self


    def get_variable_uuid(self):

        dd = self.get_app().get_directory_desk()

        v = dd.get_variable_by_name(self.get_varname())

        return v.get_uuid() if v is not None else None


    def get_varname(self):

        return self.varname


    def get_parsable_value(self):

        return self.parsable_value
 

class Measurement(model.Model):

    def __init__(self, script):

        super().__init__(script, "measurement")
        self.uuid = uuid.uuid4() 
        self.accepted_at = datetime.datetime.now()
        self.sensor_id = ""    
        self.args = []
        self.outs = [] 


    def get_uuid(self):

        return self.uuid


    def get_accepted_at(self):

        return self.accepted_at


    def get_sensor_id(self):

        return self.sensor_id


    def get_sensor_uuid(self):

        dd = self.get_app().get_directory_desk()

        s = dd.get_sensor_by_id(self.get_sensor_id())

        return s.get_uuid() if s is not None else None


    def import_dto(self, dto):

        self.uuis = dto["id"]
        self.accepted_at = datetime.datetime.strptime(dto["acceptedAt"].split(" UTC")[0], "%Y-%m-%d %H:%M:%S.%f")
        self.sensor_id = dto["sensorId"]

        self.args = [VarValue(self).import_dto(vv_dto) for vv_dto in dto["args"]]
        self.outs = [VarValue(self).import_dto(vv_dto) for vv_dto in dto["outs"]]

        return self


    def get_measurement_ramtable(self):

        m_rt = ramtable.Table("measurements")\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.TimestampField("accepted_at"))\
            .add_field(fields.UuidField("sensor_uuid"))\
            .add_field(fields.StringField("sensor_id_deb"))

        m_src = { 
                "uuid":          self.get_uuid(),
                "accepted_at":   self.get_accepted_at(), 
                "sensor_uuid":   self.get_sensor_uuid(),
                "sensor_id_deb": self.get_sensor_id() 
                }

        m_rt.insert(m_src)

        return m_rt


    def get_varvalues_ramtable(self):

        vv_rt = ramtable.Table("varvalues")\
            .add_field(fields.UuidField("measurement_uuid"))\
            .add_field(fields.UuidField("variable_uuid"))\
            .add_field(fields.StringField("varname_deb"))\
            .add_field(fields.StringField("serialized_value"))\
            .add_field(fields.StringField("value_subset"))

        for vv in self.args:

            print(vv)

            if vv is not None:
                vv_src = {  
                            "measurement_uuid": self.get_uuid(),
                            "variable_uuid": vv.get_variable_uuid(),
                            "varname_deb": vv.get_varname(),
                            "serialized_value": str(vv.get_parsable_value()),
                            "value_subset": "ARG"
                        }

                vv_rt.insert(vv_src)

        for vv in self.outs:

            vv_src = {  
                        "measurement_uuid": self.get_uuid(),
                        "variable_uuid": vv.get_variable_uuid(),
                        "varname_deb": vv.get_varname(),
                        "serialized_value": str(vv.get_parsable_value()),
                        "value_subset": "OUT"
                     }

            vv_rt.insert(vv_src)

        return vv_rt