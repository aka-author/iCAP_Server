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
        self.base_datatype_name = base_datatype_name

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


    def get_base_datatype_name(self):

        return self.base_datatype_name  


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


    def set_default_value(self, default_value=None):

        self.default_value = utils.safeval(default_value,  self.get_zero_value()) 

        self.default_value_flag = True

        return self


    def has_default_value(self):

        return self.default_value_flag


    def get_default_value(self):

        return self.default_value if self.has_default_value() else self.get_null_value()

    
    # Parsing strings into native values 

    def set_parse_format(self, pf):

        self.parse_format = pf

        return self


    def get_parse_format(self):

        return self.parse_format


    def parse_to_value(self, serialized_value, format=None):

        return serialized_value


    # Serializing native values into strings

    def set_serialize_format(self, sf):

        self.serialize_format = sf

        return self


    def get_serialize_format(self):

        return self.serialize_format


    def get_serialized_value(self, native_value, format=None):

        s = ""

        if native_value is not None:
            try:    
                s = str(native_value) 
            except: 
                s = "N/S"
        else:
            s = "null"

        return s


    # Exchanging values with DTOs

    def import_value_from_dto(self, dto_value, dtoms):

        return dto_value


    def export_value_for_dto(self, native_value, dtoms):

        raw_dto_value = None

        datatype_name = self.get_datatype_name()

        if native_value is not None:
            format = dtoms.get_format_for_datatype(datatype_name)
            raw_dto_value = \
                self.get_serialized_value(native_value, format) if format is not None \
                else native_value

        return dtoms.dto_value(self, raw_dto_value, datatype_name)


    # Exchanging values with a DB 

    def code_varname_for_sql(self, dbms):

        return dbms.sql_varname(self.get_varname())


    def code_typed_varname_sql(self, dbms):

        varname = self.get_varname()

        return dbms.sql_typed_varname(self.code_varname_for_sql(varname, dbms))


    def code_value_for_sql(self, native_value, dbms):

        raw_value_for_sql = None

        if native_value is not None:
            datatype_name = self.get_datatype_name()
            format = dbms.get_format_for_datatype(datatype_name)
            raw_value_for_sql = self.get_serialized_value(native_value, format)

        return dbms.sql_value(raw_value_for_sql, datatype_name)


    def code_typed_value_for_sql(self, native_value, dbms):

        base_datatype_name = self.get_base_datatype_name()
        sql_value = self.code_value_for_sql(native_value, base_datatype_name)
        
        return dbms.sql_typed_phrase(sql_value, base_datatype_name)


    def set_sql_agg_expr(self, snippet, dbms=None):

        if dbms is not None:
            sql_varname = dbms.sql_varname(self.get_varname())
            self.sql_agg_expr = snippet.format(sql_varname)
        else:
            self.sql_agg_expr = snippet

        return self


    def has_sql_agg_expr(self):

        return self.sql_agg_expr is not None


    def code_sql_agg_expr(self):

        return self.sql_agg_expr


    def import_from_query_output(self, query_output_value):

        return query_output_value  


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

        self.base_datatype_name = datatypes.DTN_UUID

        self.zero_value = utils.str2uuid('00000000-0000-0000-0000-000000000000')


    def get_default_value(self):
        
        return uuid.uuid4()


    def parse_to_value(self, serialized_value, format=None):

        return utils.str2uuid(serialized_value)


class BooleanField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_BOOLEAN, "boolean")

        self.base_datatype_name = datatypes.DTN_BOOLEAN


    def parse_to_value(self, serialized_value, format=None):

        return serialized_value.lower() == "true"


    def export_value_for_dto(self, native_value):

        return native_value


    def compare(self, val1, val2):

        return val1 == val2


class NumericField(Field):

    def __init__(self, varname, datatype_name):

        super().__init__(varname, datatype_name, "numeric")

        self.base_datatype_name = datatypes.DTN_NUMERIC

        self.zero_value = 0


    def parse_to_value(self, serialized_value, format=None):

        f_v = float(serialized_value)
        a_f_v = abs(f_v)

        return f_v if math.floor(a_f_v) < a_f_v else int(f_v) 


    def export_value_for_dto(self, native_value):

        return native_value


    def compare(self, val1, val2):

        return val1 - val2


class BigintField(NumericField):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_BIGINT)

        self.base_datatype_name = datatypes.DTN_BIGINT


    def parse_to_value(self, serialized_value, format=None):

        return int(serialized_value)


class DoubleField(NumericField):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_DOUBLE)

        self.base_datatype_name = datatypes.DTN_DOUBLE


    def parse_to_value(self, serialized_value, format=None):

        return float(serialized_value)


class StringField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_STRING)

        self.base_datatype_name = datatypes.DTN_STRING

        self.zero_value = ""

    
    def eq(self, val1, val2):

        return val1 == val2


    def le(self, val1, val2):

        return val1 < val2


    def ge(self, val1, val2):

        return val1 > val2


class StrListField(StringField):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_STRLIST)

        self.base_datatype_name = datatypes.DTN_STRING

        self.zero_value = ""
        

class TimestampField(Field):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_TIMESTAMP)

        self.base_datatype_name = datatypes.DTN_TIMESTAMP

        self.zero_value = datetime.now()
        self.serialize_format = utils.get_default_timestamp_format()
        self.parse_format = utils.get_default_timestamp_format()


    def get_default_value(self):

        return datetime.now()


    def serialize_value(self, native_value, custom_format=None):

        return native_value.strftime(self.get_serialize_format()) if native_value is not None else None


    def parse_to_value(self, serialized_value):

        return datetime.strptime(serialized_value, self.get_parse_format())        


    def compare(self, val1, val2):

        return val1 - val2
    

class TimestampTzField(TimestampField):

    def __init__(self, varname):

        super().__init__(varname, datatypes.DTN_TIMESTAMP_TZ)

        self.base_datatype_name = datatypes.DTN_TIMESTAMP_TZ


class FieldsManager:

    def __init__(self, owner=None, field_values=None):

        self.owner = owner

        self.fields = []
        self.fields_by_varnames = {}

        self.subkey_varnames = []
        self.mandatory_varnames = []

        if field_values is not None:
            self.reset_field_values()
        else:
            self.field_values = field_values


    def set_owner(self, owner):

        self.owner = owner

        return self


    def get_owner(self):

        return self.owner


    def set_field_values_storage(self, field_values):

        self.field_values = field_values

        return self


    def get_field_values_storage(self):

        return self.field_values


    def add_field(self, field, options=""):

        varname = field.get_varname()
                 
        self.fields.append(field)
        self.fields_by_varnames[varname] = field

        if "subkey" in options:
            self.subkey_varnames.append(varname)

        if "subkey" in options or "mandatory" in options:
            self.mandatory_varnames.append(varname)

        return self


    def get_varnames(self):

        return self.fields_by_varnames.keys()


    def has_field(self, varname):

        return varname in self.get_varnames()


    def is_subkey(self, varname):

        return varname in self.subkey_varnames


    def is_mandatory(self, varname):

        return varname in self.mandatory_varnames

    
    def get_field(self, varname):

        return self.fields_by_varnames[varname]


    def set_field_value(self, varname, native_value):

        self.field_values[varname] = native_value

        return self
            

    def reset_field_values(self):

        for field in self.fields:
            self.set_field_value(\
                field.get_varname(), \
                self.get_default_value() if field.has_default_value() else self.get_null_value()) 

        return self


    def get_field_value(self, varname):

        return self.field_values[varname]


    def parse_to_field_value(self, varname, serialized_value, custom_format=None):

        native_value = self.get_field(varname).parse_to_value(serialized_value, custom_format)

        return self.set_field_value(varname, native_value)


    def get_serialized_field_value(self, varname, custom_format=None):

        native_value = self.get_field_value(varname)

        return self.get_field(varname).get_serialized_value(native_value, custom_format)


    def import_field_value_from_dto(self, varname, dto_value):

        native_value = self.get_field(varname).import_value_from_dto(dto_value)

        return self.set_field_value(varname, native_value)


    def export_field_value_for_dto(self, varname):

        native_value = self.get_field_value(varname)

        return self.get_field(varname).export_value_for_dto(native_value)


    def code_field_value_for_sql(self, varname, dbms):

        native_value = self.get_field_value(varname)

        return self.get_field(varname).code_value_for_sql(native_value, dbms)


    def code_typed_field_value_for_sql(self, varname, dbms):

        native_value = self.get_field_value(varname)

        return self.get_field(varname).code_typed_value_for_sql(native_value, dbms)


    def fetch_field_value_from_query_output(self, varname, dto_value):

        native_value = self.get_field(varname).import_value_from_dto(dto_value)

        return self.set_field_value(varname, native_value)




    

    