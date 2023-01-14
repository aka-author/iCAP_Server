# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  fields.py                                  (\(\
# Func:    Mamaging data fields                       (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
from datetime import datetime
import utils


class Field: 

    def __init__(self, varname, datatype_name):

        self.varname = varname
        self.datatype_name = datatype_name

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


    # Exporting values to a SELECT operator

    def quote_sql(self, serialized_value):

        return serialized_value


    def export_sql(self, native_value):

        return self.quote_sql(self.serialize(native_value))


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


class StringField(Field):

    def __init__(self, varname):

        super().__init__(varname, "string")

        self.zero_value = ""


    def quote_sql(self, serialized_value):
        
        return utils.apos(serialized_value)


class UuidField(Field):

    def __init__(self, varname):

        super().__init__(varname, "uuid")


    def get_default_value(self):
        
        return uuid.uuid4()


    def serialize(self, native_value):

        return str(native_value)


    def parse(self, serialized_value):

        return utils.str2uuid(serialized_value)


    def quote_sql(self, serialized_value):
        
        return utils.apos(serialized_value)


class IntField(Field):

    def __init__(self, varname):

        super().__init__(varname, "int")
        
        self.zero_value = 0


    def parse(self, serialized_value):

        return int(serialized_value)


class FloatField(Field):

    def __init__(self, varname):

        super().__init__(varname, "float")

        self.zero_value = 0.0


    def parse(self, serialized_value):

        return float(serialized_value)


class TimestampField(Field):

    def __init__(self, varname):

        super().__init__(varname, "timestamp")

        self.zero_value = datetime.now()
        self.serialize_format = utils.get_default_timestamp_format()
        self.parse_format = utils.get_default_timestamp_format()


    def serialize(self, native_value):

        return native_value.strftime(self.get_serialize_format())


    def parse(self, serialized_value):

        return datetime.strptime(serialized_value, self.get_parse_format())        


    def quote_sql(self, serialized_value):

        return utils.apos(serialized_value)
