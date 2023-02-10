# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  fields.py                                  (\(\
# Func:    Managing data fields                       (^.^)
# # ## ### ##### ######## ############# #####################

import math, uuid
from datetime import datetime
import utils, datatypes


class Field: 

    def __init__(self, varname, datatype_name, base_datatype_name=None):

        self.varname = varname
        self.datatype_name = datatype_name
        self.base_datatype_name = utils.safeval(base_datatype_name, datatype_name)

        self.null_value = None
        self.zero_value = None
        self.default_value_flag = False
        self.default_value = None

        self.serialize_format = None
        self.parse_format = None 

        self.expr = None


    def get_varname(self):

        return self.varname


    def get_datatype_name(self):

        return self.datatype_name


    def get_base_datatype_name(self):

        return self.base_datatype_name  


    def is_atomic(self):

        return datatypes.is_atomic(self.get_datatype_name())
            

    # Dealing with empty, zero, and default values 

    def set_null_value(self, null_value):

        self.null_value = null_value

        return self


    def get_null_value(self):

        return self.null_value


    def set_zero_value(self, zero_value):

        self.zero_value = zero_value

        return self


    def get_zero_value(self):

        return self.zero_value


    def set_default_value(self, default_value=None):

        self.default_value = utils.safeval(default_value,  self.get_zero_value()) 

        self.default_value_flag = True

        return self


    def has_default_value(self):

        return self.default_value_flag


    def get_default_value(self):

        return self.default_value if self.has_default_value() else self.get_null_value()

    
    # Parsing strings into native values 

    def set_parse_format(self, parse_format):

        self.parse_format = parse_format

        return self


    def get_parse_format(self):

        return self.parse_format


    def parse_to_value(self, serialized_value, format=None):

        return serialized_value


    # Serializing native values into strings

    def set_serialize_format(self, serialize_format):

        self.serialize_format = serialize_format

        return self


    def get_serialize_format(self):

        return self.serialize_format


    def get_serialized_value(self, native_value, format=None):

        serialized_value = "null"

        if native_value is not None:
            try:    
                serialized_value = str(native_value) 
            except: 
                serialized_value = "Serializaton failed"

        return serialized_value


    # Exchanging values with DTOs

    def import_value_from_dto(self, dtoms, dto_value):

        native_value = None

        if dto_value is not None:
            format = dtoms.get_format_for_datatype(self.get_datatype_name())
            native_value = self.parse_to_value(dto_value, format) if format is not None else dto_value

        return native_value


    def export_value_for_dto(self, dtoms, native_value):

        datatype_name = self.get_datatype_name()

        if native_value is not None and dtoms.is_serialization_required(datatype_name):                  
            format = dtoms.get_format_for_datatype(datatype_name)
            raw_dto_value = self.get_serialized_value(native_value, format) 
        else:
            raw_dto_value = native_value

        return dtoms.dto_value(raw_dto_value, datatype_name)


    # Exchanging values with a DB 

    def set_expr(self, expr):

        self.expr = expr

        return self


    def has_expr(self):

        return self.expr is not None


    def get_expr(self):

        return self.expr


    def import_from_query_output(self, query_output_value):

        return query_output_value  


    # Comparing field values

    def compare(self, val1, val2):

        return 0 if val1 == val2 or (val1 is None and val2 is None) else None


    def eq(self, val1, val2):

        cmp = self.compare(val1, val2)

        return cmp == 0 if cmp is not None else False


    def is_null(self, val):

        return (val is None) if self.get_null_value() is None else self.eq(val, self.get_null_value())


    def is_zero(self, val):

        return self.eq(val, self.get_zero_value())


    def le(self, val1, val2):

        cmp = self.compare(val1, val2)

        return cmp < 0 if cmp is not None else False


    def ge(self, val1, val2):

        cmp = self.compare(val1, val2)

        return cmp > 0 if cmp is not None else False


class UuidField(Field):

    def __init__(self, varname, datatype_name=datatypes.DTN_UUID):

        super().__init__(varname, datatype_name, datatypes.DTN_UUID)

        self.zero_value = utils.str2uuid('00000000-0000-0000-0000-000000000000')


    def get_default_value(self):
        
        return uuid.uuid4()


    def parse_to_value(self, serialized_value, format=None):

        return utils.str2uuid(serialized_value)


class BooleanField(Field):

    def __init__(self, varname, datatype_name=datatypes.DTN_BOOLEAN):

        super().__init__(varname, datatype_name, datatypes.DTN_BOOLEAN)


    def parse_to_value(self, serialized_value, format=None):

        return serialized_value.lower() == "true"


class NumericField(Field):

    def __init__(self, varname, datatype_name=datatypes.DTN_NUMERIC, base_datatype_name=datatypes.DTN_NUMERIC):

        super().__init__(varname, datatype_name, base_datatype_name)

        self.zero_value = 0


    def parse_to_value(self, serialized_value, format=None):

        f_v = float(serialized_value)
        a_f_v = abs(f_v)

        return f_v if math.floor(a_f_v) < a_f_v else int(f_v) 


    def compare(self, val1, val2):

        return val1 - val2


class BigintField(NumericField):

    def __init__(self, varname, datatype_name=datatypes.DTN_BIGINT):

        super().__init__(varname, datatype_name, datatypes.DTN_BIGINT)


    def parse_to_value(self, serialized_value, format=None):

        return int(serialized_value)


class DoubleField(NumericField):

    def __init__(self, varname, datatype_name=datatypes.DTN_DOUBLE):

        super().__init__(varname, datatype_name, datatypes.DTN_DOUBLE)


    def parse_to_value(self, serialized_value, format=None):

        return float(serialized_value)


class StringField(Field):

    def __init__(self, varname, datatype_name=datatypes.DTN_STRING):

        super().__init__(varname, datatype_name, datatypes.DTN_STRING)

        self.zero_value = ""

    
    def eq(self, val1, val2):

        return val1 == val2


    def le(self, val1, val2):

        return val1 < val2


    def ge(self, val1, val2):

        return val1 > val2


class StrListField(StringField):

    def __init__(self, varname, datatype_name=datatypes.DTN_STRLIST):

        super().__init__(varname, datatype_name)

        self.zero_value = ""
        

class TimestampField(Field):

    def __init__(self, varname, datatype_name=datatypes.DTN_TIMESTAMP):

        super().__init__(varname, datatype_name, datatypes.DTN_TIMESTAMP)

        self.zero_value = datetime.now()
        self.serialize_format = datatypes.get_default_timestamp_format()
        self.parse_format = datatypes.get_default_timestamp_format()


    def get_default_value(self):

        return datetime.now()


    def get_serialized_value(self, native_value, format=None):

        fmt = utils.safeval(format, self.get_serialize_format())
        
        return native_value.strftime(fmt) if native_value is not None else None


    def parse_to_value(self, serialized_value, format=None):
    
        fmt = utils.safeval(format, self.get_parse_format())
        
        return datetime.strptime(serialized_value, fmt)        


    def compare(self, val1, val2):

        return val1 - val2
    

class TimestampTzField(TimestampField):

    def __init__(self, varname, datatype_name=datatypes.DTN_TIMESTAMP_TZ):

        super().__init__(varname, datatype_name)


class DateField(TimestampField):

    def __init__(self, varname, datatype_name=datatypes.DTN_DATE):

        super().__init__(varname, datatype_name)

        self.serialize_format = datatypes.get_default_date_format()
        self.parse_format = datatypes.get_default_date_format()


class FieldKeeper:

    def __init__(self):

        self.fields = []
        self.fields_by_varnames = {}

        self.subkey_varnames = []
        self.mandatory_varnames = []
        self.autoins_varnames = []


class FieldManager:

    def __init__(self, owner, field_keeper=None):

        self.owner = owner

        self.fk = field_keeper if field_keeper is not None else FieldKeeper()
        
        self.field_values = {}
        self.reset_field_values()


    def set_owner(self, owner):

        self.owner = owner

        return self


    def get_owner(self):

        return self.owner


    def set_field_keeper(self, field_keeper):

        self.fk = field_keeper

        return self


    def get_field_keeper(self):

        return self.fk

    @property
    def fields(self):

        return self.get_field_keeper().fields

    @property 
    def fields_by_varnames(self):

        return self.get_field_keeper().fields_by_varnames

    @property 
    def subkey_varnames(self):

        return self.get_field_keeper().subkey_varnames

    @property 
    def mandatory_varnames(self):

        return self.get_field_keeper().mandatory_varnames

    @property 
    def autoins_varnames(self):

        return self.get_field_keeper().autoins_varnames


    def define_subkey(self, varname):

        self.subkey_varnames.append(varname)

        return self


    def define_mandatory(self, varname):

        self.mandatory_varnames.append(varname)

        return self


    def define_autoins(self, varname):

        self.autoins_varnames.append(varname)


    def add_field(self, field, options="optional"):

        varname = field.get_varname()
                 
        self.fields.append(field)
        self.fields_by_varnames[varname] = field

        if "subkey" in options:
            self.define_subkey(varname)

        if "subkey" in options or "mandatory" in options:
            self.define_mandatory(varname)

        if "autoins" in options:
            self.define_autoins(varname)

        return self


    def count_fields(self):

        return len(self.fields)


    def get_varnames(self):

        return self.fields_by_varnames.keys()


    def has_field(self, varname):

        return varname in self.get_varnames()


    def get_field(self, varname):

        return self.fields_by_varnames[varname]


    def is_subkey(self, varname):

        return varname in self.subkey_names


    def is_mandatory(self, varname):

        return varname in self.mandatory_field_names


    def is_insertable(self, varname):

        return not (varname in self.autoins_field_names or self.get_field(varname).has_expr())


    def set_field_value(self, varname, native_value):

        self.field_values[varname] = native_value

        return self
            

    def set_field_values(self, native_values):

        for _, (varname, native_value) in enumerate(native_values.items()):
            if self.has_field(varname):
                self.set_field_value(varname, native_value)

        return self


    def reset_field_values(self):

        for field in self.fields:
            self.set_field_value(field.get_varname(), field.get_default_value())
                
        return self


    def get_field_value(self, varname):

        return utils.safedic(self.field_values, varname)


    def parse_to_native_value(self, varname, serialized_value, format=None):

        native_value = self.get_field(varname).parse_to_value(serialized_value, format)

        return self.set_field_value(varname, native_value)


    def get_serialized_field_value(self, varname, format=None):

        native_value = self.get_field_value(varname)
        
        return self.get_field(varname).get_serialized_value(native_value, format)


    def import_field_value_from_dto(self, dtoms, varname, dto_value):

        native_value = self.get_field(varname).import_value_from_dto(dtoms, dto_value)

        return self.set_field_value(varname, native_value)


    def export_field_value_for_dto(self, dtoms, varname):

        native_value = self.get_field_value(varname)

        return self.get_field(varname).export_value_for_dto(dtoms, native_value)


    def fetch_field_value_from_query_output(self, varname, dto_value):

        native_value = self.get_field(varname).import_value_from_dto(dto_value)

        return self.set_field_value(varname, native_value)


    def eq_field_value(self, field_name, compare_value):

        field = self.get_field(field_name)

        return field.eq(self.get_field_value(field_name), compare_value)
