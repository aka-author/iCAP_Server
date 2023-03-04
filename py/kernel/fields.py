# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  fields.py                                  
# Func:    Managing data fields                      (\(\   
# Usage:   Create objects bases on the classes       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List, Dict
import copy, math, uuid
from datetime import datetime
import utils, datatypes


class Field: 

    def __init__(self, varname: str, datatype_name: str):

        self.varname = varname
        self.datatype_name = datatype_name

        self.null_value = None
        self.zero_value = None
        self.default_value_flag = False
        self.default_value = None

        self.parse_format = None
        self.serialize_format = None

        self.expr = None


    def get_varname(self) -> str:

        return self.varname


    def get_datatype_name(self) -> str:

        return self.datatype_name


    def is_atomic(self) -> bool:

        return datatypes.is_atomic(self.get_datatype_name())
            

    # Dealing with empty, zero, and default values 

    def set_null_value(self, null_value: any) -> object:

        self.null_value = null_value

        return self


    def get_null_value(self) -> any:

        return self.null_value


    def set_zero_value(self, zero_value: any) -> object:

        self.zero_value = zero_value

        return self


    def get_zero_value(self) -> any:

        return self.zero_value


    def set_default_value(self, default_value: any=None) -> object:

        self.default_value = utils.safeval(default_value,  self.get_zero_value()) 

        self.default_value_flag = True

        return self


    def has_default_value(self) -> bool:

        return self.default_value_flag


    def get_default_value(self) -> any:

        return self.default_value if self.has_default_value() else self.get_null_value()

    
    # Parsing strings into native values 

    def set_parse_format(self, parse_format: str) -> object:

        self.parse_format = parse_format

        return self


    def get_parse_format(self) -> str:

        return self.parse_format


    def parse_to_native_value(self, serialized_value: str, format: str=None) -> any:

        return serialized_value


    # Serializing native values into strings

    def set_serialize_format(self, serialize_format: str) -> object:

        self.serialize_format = serialize_format

        return self


    def get_serialize_format(self) -> str:

        return self.serialize_format


    def get_serialized_value(self, native_value: any, format: str=None) -> str:

        serialized_value = "null"

        if native_value is not None:
            try:    
                serialized_value = str(native_value) 
            except: 
                serialized_value = "Serializaton failed"

        return serialized_value


    # Providing an expression for SQL 

    def set_expr(self, expr: str) -> object:

        self.expr = expr

        return self


    def has_expr(self) ->  bool:

        return self.expr is not None


    def get_expr(self) -> str:

        return self.expr


    # Comparing field values

    def compare(self, val1: any, val2: any) -> int:

        return 0 if val1 == val2 or (val1 is None and val2 is None) else None


    def eq(self, val1: any, val2: any) -> bool:

        cmp = self.compare(val1, val2)

        return cmp == 0 if cmp is not None else False


    def is_null(self, val: any) -> bool:

        return (val is None) if self.get_null_value() is None else self.eq(val, self.get_null_value())


    def is_zero(self, val: any) -> bool:

        return self.eq(val, self.get_zero_value())


    def le(self, val1: any, val2: any) -> bool:

        cmp = self.compare(val1, val2)

        return cmp < 0 if cmp is not None else False


    def ge(self, val1: any, val2: any) -> bool:

        cmp = self.compare(val1, val2)

        return cmp > 0 if cmp is not None else False

    # Misc.

    def clone(self) -> 'Field':

        return type(self)(self.get_varname())


class UuidField(Field):

    def __init__(self, varname: str):

        super().__init__(varname, datatypes.DTN_UUID)

        self.zero_value = utils.str2uuid('00000000-0000-0000-0000-000000000000')


    def get_default_value(self) -> uuid:
        
        return uuid.uuid4()


    def parse_to_native_value(self, serialized_value: str, format: str=None) -> uuid:

        return utils.str2uuid(serialized_value)


class BooleanField(Field):

    def __init__(self, varname: str):

        super().__init__(varname, datatypes.DTN_BOOLEAN)


    def parse_to_native_value(self, serialized_value: str, format: str=None) -> bool:

        return serialized_value.lower() == "true"


class NumericField(Field):

    def __init__(self, varname: str, datatype_name=datatypes.DTN_NUMERIC):

        super().__init__(varname, datatype_name)

        self.zero_value = 0


    def parse_to_native_value(self, serialized_value: str, format: str=None) -> any:

        f_v = float(serialized_value)
        a_f_v = abs(f_v)

        return f_v if math.floor(a_f_v) < a_f_v else int(f_v) 


    def compare(self, val1: any, val2: any) -> any:

        return val1 - val2


class BigintField(NumericField):

    def __init__(self, varname: str):

        super().__init__(varname, datatypes.DTN_BIGINT)


    def parse_to_native_value(self, serialized_value: str, format: str=None) -> int:

        return int(serialized_value)


class DoubleField(NumericField):

    def __init__(self, varname: str):

        super().__init__(varname, datatypes.DTN_DOUBLE)


    def parse_to_native_value(self, serialized_value: str, format: str=None) -> float:

        return float(serialized_value)


class StringField(Field):

    def __init__(self, varname: str, datatype_name: str=datatypes.DTN_STRING):

        super().__init__(varname, datatype_name)

        self.zero_value = ""

    
    def eq(self, val1: str, val2: str) -> bool:

        return val1 == val2


    def le(self, val1: str, val2: str) -> bool:

        return val1 < val2


    def ge(self, val1: str, val2: str) -> bool:

        return val1 > val2


class StrListField(StringField):

    def __init__(self, varname: str):

        super().__init__(varname, datatypes.DTN_STRLIST)

        self.zero_value = ""
        

class TimestampField(Field):

    def __init__(self, varname: str, datatype_name: str=datatypes.DTN_TIMESTAMP):

        super().__init__(varname, datatype_name)

        self.zero_value = datetime.now()
        self.serialize_format = datatypes.get_default_timestamp_format()
        self.parse_format = datatypes.get_default_timestamp_format()


    def get_default_value(self) -> datetime:

        return datetime.now()


    def get_serialized_value(self, native_value: datetime, format: str=None) -> str:

        fmt = utils.safeval(format, self.get_serialize_format())
        
        return native_value.strftime(fmt) if native_value is not None else None


    def parse_to_native_value(self, serialized_value: str, format: str=None) -> datetime:
    
        parse_format = utils.safeval(format, self.get_parse_format())

        try:
            native_value = datetime.strptime(serialized_value, parse_format) 
        except:
            native_value = None
        
        return native_value        


    def compare(self, val1: datetime, val2: datetime) -> int:

        return int(val1) - int(val2)
    

class TimestampTzField(TimestampField):

    def __init__(self, varname: str):

        super().__init__(varname, datatypes.DTN_TIMESTAMP_TZ)


class DateField(TimestampField):

    def __init__(self, varname: str):

        super().__init__(varname, datatypes.DTN_DATE)

        self.serialize_format = datatypes.get_default_date_format()
        self.parse_format = datatypes.get_default_date_format()


class FieldKeeper:

    def __init__(self, recordset_name: str=None):

        self.recordset_name = recordset_name

        self.fields = []
        self.fields_by_varnames = {}

        self.surrogate_key_name = None
        self.subkey_varnames = []
        self.mandatory_varnames = []
        self.autoins_varnames = []


    def set_recordset_name(self, recordset_name: str) -> 'FieldKeeper':

        self.recordset_name = recordset_name

        return self


    def get_recordset_name(self) -> str:

        return self.recordset_name


    def define_subkey(self, varname: str) -> 'FieldKeeper':

        self.masubkey_varnames.append(varname)

        return self


    def define_mandatory(self, varname: str) -> 'FieldKeeper':

        self.mandatory_varnames.append(varname)

        return self


    def define_autoins(self, varname: str) -> 'FieldKeeper':

        self.autoins_varnames.append(varname)

        return self


    def define_surrogate_key(self, varname: str) -> 'FieldKeeper':

        self.surrogate_key_name = varname


    def get_surrogate_key_name(self) -> str:

        if self.surrogate_key_name is not None:
            return self.surrogate_key_name
        elif self.has_field("uuid"):
            return "uuid"
        else:
            return None


    def add_field(self, field: Field, options: str="optional") -> 'FieldKeeper':

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


    def count_fields(self) -> int:

        return len(self.fields)


    def get_fields(self) -> List:

        return self.fields


    def get_varnames(self):

        return [field.get_varname() for field in self.fields]


    def has_field(self, varname: str) -> bool:

        return varname in self.get_varnames()


    def get_field(self, varname: str) -> Field:

        return self.fields_by_varnames[varname]


    def is_subkey(self, varname: str) -> bool:

        return varname in self.subkey_names


    def is_mandatory(self, varname: str) -> bool:

        return varname in self.mandatory_field_names


    def is_insertable(self, varname: str) -> bool:

        return not (varname in self.autoins_varnames or self.get_field(varname).has_expr())


class FieldManager:

    def __init__(self, field_keeper: FieldKeeper=None):

        self.fk = field_keeper if field_keeper is not None else FieldKeeper()
        
        self.field_values = {}
        self.reset_field_values()


    def set_field_keeper(self, field_keeper: FieldKeeper) -> 'FieldManager':

        self.fk = field_keeper

        return self


    def get_field_keeper(self) -> FieldKeeper:

        return self.fk


    def set_recordset_name(self, recordset_name: str) -> 'FieldManager':

        self.get_field_keeper().set_recordset_name(recordset_name)

        return self


    def get_recordset_name(self) -> str:

        return self.get_field_keeper().get_recordset_name()


    def define_subkey(self, varname: str) -> object:

        self.get_field_keeper().define_subkey(varname)

        return self


    def define_mandatory(self, varname: str) -> 'FieldManager':

        self.get_field_keeper().define_mandatory(varname) 

        return self


    def define_autoins(self, varname: str) -> 'FieldManager':

        self.get_field_keeper().define_autoins(varname)

        return self


    def add_field(self, field: Field, options: str="optional") -> 'FieldManager':

        self.get_field_keeper().add_field(field, options)

        return self


    def count_fields(self) -> int:

        return self.get_field_keeper().count_fields() 


    def get_varnames(self):

        return self.get_field_keeper().get_varnames()


    def has_field(self, varname: str) -> bool:

        return self.get_field_keeper().has_field(varname)


    def get_field(self, varname: str) -> Field:

        return self.get_field_keeper().get_field(varname)


    def get_surrogate_key_name(self) -> str:

        return self.get_field_keeper().get_surrogate_key_name()


    def is_subkey(self, varname: str) -> bool:

        return self.get_field_keeper().is_subkey(varname)


    def is_mandatory(self, varname: str) -> bool:

        return self.get_field_keeper().is_mandatory(varname)


    def is_insertable(self, varname: str) -> bool:

        return self.get_field_keeper().is_insertable(varname)


    def set_field_value(self, varname: str, native_value: any) -> 'FieldManager':
        
        self.field_values[varname] = native_value

        return self

    
    def set_field_values(self, native_values: Dict) -> 'FieldManager':

        for (varname, native_value) in native_values.items():
            if self.has_field(varname):
                self.set_field_value(varname, native_value)

        return self


    def set_field_values_from_field_manager(self, fm: 'FieldManager') -> 'FieldManager':

        for varname in fm.get_varnames():
            self.set_field_value(varname, fm.get_field_value(varname))

        return self


    def reset_field_values(self) -> 'FieldManager':

        for field in self.get_field_keeper().get_fields():
            self.set_field_value(field.get_varname(), field.get_default_value())
                
        return self


    def get_field_value(self, varname: str) -> any:

        return self.field_values.get(varname, self.get_field(varname).get_default_value())


    def get_field_values(self) -> Dict:

        return copy.copy(self.field_values)
    

    def get_insertable_field_values(self) -> List:

        insertables = {}

        for varname in self.get_varnames():
            if self.is_insertable(varname):
                insertables[varname] = self.get_field_value(varname)

        return insertables


    def parse_to_native_value(self, varname: str, serialized_value: str, format: str=None) -> any:

        native_value = self.get_field(varname).parse_to_native_value(serialized_value, format)

        return self.set_field_value(varname, native_value)


    def get_serialized_field_value(self, varname: str, format: str=None) -> str:

        native_value = self.get_field_value(varname)
        
        return self.get_field(varname).get_serialized_value(native_value, format)


    def eq_field_value(self, field_name: str, compare_with_value: any) -> bool:

        field = self.get_field(field_name)

        return field.eq(self.get_field_value(field_name), compare_with_value)
