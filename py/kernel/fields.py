# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  fields.py                                  (\(\
# Func:    Mamaging data fields                       (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
from datetime import datetime
import utils, datatypes


class Field: 

    def __init__(self, varname, datatype_name, nature=None):

        self.varname = varname
        self.datatype_name = datatype_name
        self.nature = nature if nature is not None else datatype_name

        self.null_value = None
        self.zero_value = None
        self.explicit_default_value_flag = False
        self.default_value = None

        self.serialize_format = ""
        self.parse_format = "" 
        self.sql_agg_expr = None


    def get_varname(self):

        return self.varname


    def get_datatype_name(self):

        return self.datatype_name


    def get_nature(self):

        return self.nature


    def is_atomic(self):

        return datatypes.is_atomic(self.get_datatype_name())
            

    # Dealing with empty, zero, and default values 

    def set_null_value(self, null_value):

        self.null_value = null_value


    def get_null_value(self):

        return self.null_value


    def set_zero_value(self, zero_value):

        self.zero_value = zero_value


    def get_zero_value(self):

        return self.zero_value


    def set_default_value(self, default_value):

        self.default_value = default_value
        self.explicit_default_value_flag = True

        return self


    def has_explicit_default_value(self):

        return self.explicit_default_value_flag


    def get_default_value(self):

        return self.default_value if self.has_explicit_default_value() else self.get_null_value()


    # Formatting native values into strings

    def set_serialize_format(self, sf):

        self.serialize_format = sf

        return self


    def get_serialize_format(self):

        return self.serialize_format


    def serialize(self, native_value):

        return str(native_value)


    # Parsing strings into native values 

    def set_parse_format(self, pf):

        self.parse_format = pf

        return self


    def get_parse_format(self):

        return self.parse_format


    def parse(self, serialized_value):

        return serialized_value


    # Loading field values from a database 

    def set_sql_agg_expr(self, snippet):

        self.sql_agg_expr = snippet

        return self


    def has_sql_agg_expr(self):

        return self.sql_agg_expr is not None


    def get_sql_agg_expr(self):

        return self.sql_agg_expr


    def import_from_dic(self, dic_pair_value):

        return dic_pair_value  


    # Comparing field values

    def compare(self, val1, val2):

        return 0 if val1 == val2 else None


    def eq(self, val1, val2):

        cmp = self.compare(val1, val2)

        return cmp == 0 if cmp is not None else False


    def le(self, val1, val2):

        cmp = self.compare(val1, val2)

        return cmp < 0 if cmp is not None else False


    def ge(self, val1, val2):

        cmp = self.compare(val1, val2)

        return cmp < 0 if cmp is not None else False


class UuidField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_UUID)


    def get_default_value(self):
        
        return uuid.uuid4()


    def serialize(self, native_value):

        return str(native_value)


    def parse(self, serialized_value):

        return utils.str2uuid(serialized_value)


    def quote_sql(self, serialized_value):
        
        return utils.apos(serialized_value)

    
    def import_from_dic(self, dic_pair_value):
        
        return self.parse(dic_pair_value) if utils.is_str(dic_pair_value) else dic_pair_value


class BooleanField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_BOOLEAN, "boolean")


    def compare(self, val1, val2):

        return val1 == val2


class NumericField(Field):

    def __init__(self, varname, datatype_name):

        super().__init__(varname, datatype_name, "numeric")


    def compare(self, val1, val2):

        return val1 - val2


class BigintField(NumericField):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_BIGINT)

        self.zero_value = 0


    def parse(self, serialized_value):

        return int(serialized_value)


class DoubleField(NumericField):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_DOUBLE)

        self.zero_value = 0.0


    def parse(self, serialized_value):

        return float(serialized_value)


class StringField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_STRING)

        self.zero_value = ""


    def quote_sql(self, serialized_value):
        
        return utils.apos(serialized_value)

    
    def eq(self, val1, val2):

        return val1 == val2


    def le(self, val1, val2):

        return val1 < val2


    def ge(self, val1, val2):

        return val1 > val2


class StrListField(StringField):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_STRLIST)
        

class TimestampField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_TIMESTAMP)

        self.zero_value = datetime.now()
        self.serialize_format = utils.get_default_timestamp_format()
        self.parse_format = utils.get_default_timestamp_format()


    def serialize(self, native_value):

        return native_value.strftime(self.get_serialize_format()) if native_value is not None else None


    def parse(self, serialized_value):

        return datetime.strptime(serialized_value, self.get_parse_format())        


    def quote_sql(self, serialized_value):

        return utils.apos(serialized_value)


    def compare(self, val1, val2):

        return val1 - val2
    

class TimestampTzField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_TIMESTAMP_TZ)
