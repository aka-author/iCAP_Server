# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  measurement.py                                  (\(\
# Func:    Mamaging data fields                       (^.^)
# # ## ### ##### ######## ############# #####################

import uuid, datetime
import fields, model, ramtable


class VarValue(model.Model):

    def __init__(self, measurement):

        super().__init__(measurement, "varvalue")

        self.varname = None
        self.parsable_value = None
        self.is_argument = False


    def define_fields(self):

        self.define_field(fields.StrField("varvalue"))
        self.define_field(fields.StrField("parsable_value"))





class Measurement(model.Model):

    def __init__(self):

        self.uuid = uuid.uuid4()
        self.accepted_at = datetime.now()
        self.sensor_id = "";     
        self.args = [];
        self.outs = [];   


    def get_uuid(self):

        return self.get_uuid


    def get_accepted_at(self):

        return self.accepted_at


    def get_sensor_id(self):

        return self.sensor_id


    def import_dto(self, dto):

        self.set_


    def insert_vvs_to_rt(self, rt, vvs):

        for varvalue in vvs:

            src = { \
                   "measurement_uuid":                self.get_uuid(), \
                   "varname":                         varvalue.get_varname(), \
                   varvalue.get_useful_field_name():  varvalue.get_useful_value(), \
                   "value_subset":                    self.get_subset_code()}
            
            rt.insert_from_dic(src)

        return rt


    def assemble_ramtables(self):

        m_rt = ramtable.Ramtable("measurements")

        m_rt.add_field(fields.UuidField("uuid"))
        m_rt.add_field(fields.TimestampField("accepted_at"))
        m_rt.add_field(fields.StringField("sensor_id"))

        m_src = { \
                 "accepted_at": self.get_accepted_at(), \
                 "sensor_id":   self.get_sensor_id() \
                }

        m_rt.insert_from_dic(m_src)

        vv_rt = ramtable.Ramtable("varvals")

        vv_rt.add_field(fields.UuidField("measurement_uuid"))
        vv_rt.add_field(fields.StringField("subset"))
        vv_rt.add_field(fields.StringField("value_str"))
        vv_rt.add_field(fields.StringField("value_bgi"))
        vv_rt.add_field(fields.StringField("value_dbl"))
        vv_rt.add_field(fields.StringField("value_tms"))
        vv_rt.add_field(fields.StringField("value_boo"))
        vv_rt.add_field(fields.StringField("value_jsn"))

        
    
        self.insert_vvs_to_rt(vv_rt, self.args)
        self.insert_vvs_to_rt(vv_rt, self.outs)

        return m_rt, vv_rt
        
