# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  measurement.py                             (\(\
# Func:    Mamaging data fields                       (^.^)
# # ## ### ##### ######## ############# #####################

import uuid, datetime
import utils, fields, model, ramtable, dirdesk


class VarValue(model.Model):

    def __init__(self, measurement):

        super().__init__(measurement, "varvalue")

        self.varname = None
        self.parsable_value = None


    def import_dto(self, dto):
        
        self.varname = dto["varName"]
        self.parsable_value = dto["parsableValue"]

        return self


    def get_varname(self):

        return self.varname


    def get_parsable_value(self):

        return self.parsable_value
 

    def get_variable_uuid(self):

        dd = self.get_app().get_directory_desk()

        v = dd.get_variable_by_name(self.get_varname())

        return v.get_uuid() if v is not None else None


    def is_valid(self): 

        return self.get_variable_uuid() is not None


class Measurement(model.Model):

    def __init__(self, script):

        super().__init__(script, "measurement")
        self.uuid = uuid.uuid4() 
        self.accepted_at = datetime.datetime.now()
        self.sensor_id = ""    
        self.args = []
        self.outs = []
        self.varvals_by_names = {} 
        

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

    
    def get_parsable_value(self, varname):

        return self.varvals_by_names[varname].get_parsable_value()


    def count_args(self):

        return len(self.args)


    def count_outs(self):

        return len(self.outs)


    def import_dto(self, dto):

        self.uuis = dto["id"]
        self.accepted_at = utils.str2timestamp(dto["acceptedAt"])
        self.sensor_id = dto["sensorId"]

        self.args = [VarValue(self).import_dto(vv_dto) for vv_dto in dto["args"]]
        self.outs = [VarValue(self).import_dto(vv_dto) for vv_dto in dto["outs"]]
        
        for varval in self.args + self.outs: 
            self.varvals_by_names[varval.get_varname()] = varval

        return self


    def is_valid(self): 

        valid_flag = self.get_accepted_at() is not None \
                 and self.get_sensor_id() is not None \
                 and self.count_args() > 0 

        if valid_flag:

            for v in self.args + self.outs:
                valid_flag = v.is_valid()
                if not valid_flag: break

        return valid_flag           


    def get_hashkey(self):

        dd = self.get_app().get_directory_desk()

        arg_names = [arg.get_varname() for arg in self.args]
        arg_names.sort()

        out_names = [out.get_varname() for out in self.outs]
        out_names.sort()

        args_hashkey = "#".join([utils.safeval(dd.get_variable_by_name(arg_name).get_shortcut(), arg_name)\
                     + ":"\
                     + str(self.get_parsable_value(arg_name)) \
                                 for arg_name in arg_names])

        outs_hashkey = "#".join([utils.safeval(dd.get_variable_by_name(out_name).get_shortcut(), out_name) \
                                 for out_name in out_names])

        hashkey = args_hashkey + "$" + outs_hashkey

        return hashkey
 

    def get_measurement_ramtable(self):

        rt_m = ramtable.Table("measurements")\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.TimestampField("accepted_at"))\
            .add_field(fields.UuidField("sensor_uuid"))\
            .add_field(fields.StringField("sensor_id_deb"))\
            .add_field(fields.StringField("hashkey"))

        src_m = { 
                    "uuid":          self.get_uuid(),
                    "accepted_at":   self.get_accepted_at(), 
                    "sensor_uuid":   self.get_sensor_uuid(),
                    "sensor_id_deb": self.get_sensor_id(), 
                    "hashkey":       self.get_hashkey()
                }

        rt_m.insert(src_m)

        return rt_m


    def get_varvalues_ramtable(self):

        rt_vv = ramtable.Table("varvalues")\
            .add_field(fields.UuidField("measurement_uuid"))\
            .add_field(fields.UuidField("variable_uuid"))\
            .add_field(fields.StringField("varname_deb"))\
            .add_field(fields.StringField("serialized_value"))\
            .add_field(fields.StringField("value_subset"))

        for vv in self.args:

            src_vv = {  
                        "measurement_uuid": self.get_uuid(),
                        "variable_uuid": vv.get_variable_uuid(),
                        "varname_deb": vv.get_varname(),
                        "serialized_value": str(vv.get_parsable_value()),
                        "value_subset": "ARG"
                    }

            rt_vv.insert(src_vv)

        for vv in self.outs:

            src_vv = {  
                        "measurement_uuid": self.get_uuid(),
                        "variable_uuid": vv.get_variable_uuid(),
                        "varname_deb": vv.get_varname(),
                        "serialized_value": str(vv.get_parsable_value()),
                        "value_subset": "OUT"
                     }

            rt_vv.insert(src_vv)

        return rt_vv