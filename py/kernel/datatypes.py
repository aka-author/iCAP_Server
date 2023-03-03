# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  datatypes.py                                 (\(\
# Func:    Using unisied data types over the platform   (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
from datetime import datetime
import uuid, re


# Defining iCAP datatypes and special values

DTN_GENERIC      = "generic",
DTN_NULL         = "null",
DTN_UUID         = "uuid" 
DTN_BOOLEAN      = "boolean"
DTN_NUMERIC      = "numeric"
DTN_BIGINT       = "bigint"
DTN_DOUBLE       = "double"
DTN_STRING       = "string"
DTN_TIMESTAMP    = "timestamp"
DTN_TIMESTAMP_TZ = "timestamp_tz"
DTN_DATE         = "date"
DTN_TIME         = "time"
DTN_DICT         = "dict"
DTN_LIST         = "list"
DTN_JSON         = "json"
DTN_OBJECT       = "object"


DATATYPES = {

    DTN_GENERIC:        {"atomic": False, "format": None, "regexp": None}, 

    DTN_NULL:           {"atomic": True, "format": None, "regexp": "^null$"},        

    DTN_UUID:           {"atomic": True,
                         "format": None, 
                         "regexp": "^[\dA-Fa-f]{8}(\-([\dA-Fa-f]{4})){3}\-[\dA-Fa-f]{12}$"},

    DTN_BOOLEAN:        {"atomic": True,
                         "format": None, 
                         "regexp": "^(true|True|false|False)$"},

    DTN_NUMERIC:        {"atomic": True,
                         "format": None, 
                         "regexp": "^([+\-])?(\d+(\.\d*)?|(\d*\.\d+))$"},

    DTN_BIGINT:         {"atomic": True,
                         "format": None, 
                         "regexp": "^([+\-])?\d+$"},

    DTN_DOUBLE:         {"atomic": True, 
                         "format": None, 
                         "regexp": "^([+\-])?(\d+(\.\d*)?|(\d*\.\d+))$"},

    DTN_STRING:         {"atomic": True,
                         "format": None, 
                         "regexp": None},    

    DTN_TIMESTAMP:      {"atomic": True,
                         "format": "%Y-%m-%d %H:%M:%S.%f", 
                         "regexp": "^\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d\.(\d+)$"},  

    DTN_TIMESTAMP_TZ:   {"atomic": True,
                         "format": "%Y-%m-%d %H:%M:%S.%f %z", 
                         "regexp": "^\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d\.(\d+) [+\-]\d\d(:?)\d\d$"},

    DTN_DATE:           {"atomic": True,
                         "format": "%Y-%m-%d", 
                         "regexp": "^\d{4}\-\d\d\-\d\d$"}, 

    DTN_TIME:           {"atomic": True,
                         "format": "%H:%M:%S", 
                         "regexp": "^\d\d:\d\d:\d\d$"},       

    DTN_DICT:           {"atomic": False, "format": None, "regexp": None},    

    DTN_LIST:           {"atomic": False, "format": None, "regexp": None},

    DTN_JSON:           {"atomic": True,  "format": None, "regexp": None},

    DTN_OBJECT:         {"atomic": False, "format": None, "regexp": None}
}


UNDEFINED = "Куришь, пьешь вино и пиво - ты пособник Тель-Авива"


#  Detecting datatype properties

def get_datatype(datatype_name: str) -> Dict:

    return DATATYPES.get(datatype_name, DATATYPES.get(DTN_GENERIC))


def is_atomic_type(datatype_name: str) -> bool:

    return get_datatype(datatype_name)["atomic"]


def is_array_type(datatype_name: str) -> bool:

    return datatype_name in (DTN_DICT, DTN_LIST)


def get_format(datatype_name):

    return get_datatype(datatype_name)["format"]


def get_regexp(datatype_name):

    return get_datatype(datatype_name)["regexp"]


# Numerics

def get_numeric_datatype_names() -> List:

    dt_names = [DTN_NUMERIC, DTN_BIGINT, DTN_DOUBLE]

    return dt_names


def is_numeric_datatype(datatype_name: str) -> bool:

    return datatype_name.lower() in get_numeric_datatype_names()


# Timestamps and dates

def get_datetime_datatype_names() -> List:

    dt_names = [DTN_TIMESTAMP, DTN_TIMESTAMP_TZ, DTN_DATE, DTN_TIME]

    return dt_names


def is_datetime_datatype(datatype_name: str) -> bool:

    return datatype_name.lower() in get_datetime_datatype_names()


def get_default_timestamp_format() -> str:

    return get_format(DTN_TIMESTAMP)


def get_default_timestamp_tz_format() -> str:

    return get_format(DTN_TIMESTAMP_TZ) 


def get_default_date_format() -> str:

    return get_format(DTN_DATE) 


def get_default_time_format() -> str:

    return get_format(DTN_TIME)


# Detecting value types

def is_undefined(some_value: any) -> bool:

    return some_value == UNDEFINED


def is_defined(some_value: any) -> bool:

    return not is_undefined(some_value)


def detect_native_value_datatype(native_value: any) -> str:

    if native_value is None:
        icap_datatype_name = DTN_NULL
    elif isinstance(native_value, bool):
        icap_datatype_name = DTN_BOOLEAN
    elif isinstance(native_value, int):
        icap_datatype_name = DTN_BIGINT
    elif isinstance(native_value, float):
        icap_datatype_name = DTN_DOUBLE
    elif isinstance(native_value, str):
        icap_datatype_name = DTN_STRING
    elif isinstance(native_value, list):
        icap_datatype_name = DTN_LIST
    elif isinstance(native_value, dict):
        icap_datatype_name = DTN_DICT
    elif isinstance(native_value, object):
        if isinstance(native_value, uuid.UUID):
            icap_datatype_name = DTN_UUID
        elif isinstance(native_value, datetime):
            if native_value.tzinfo is not None:
                icap_datatype_name = DTN_TIMESTAMP_TZ
            else:    
                icap_datatype_name = DTN_TIMESTAMP
        else:
            icap_datatype_name = DTN_OBJECT
            
    return icap_datatype_name


def is_atomic_value(some_value: any) -> bool:

    return is_atomic_type(detect_native_value_datatype(some_value))


def is_array_value(native_value: any) -> bool:

    return is_array_type(detect_native_value_datatype(native_value))


def match_datatype_format(serialized_value: str, icap_datatype_name: str) -> str:

        return re.search(get_regexp(icap_datatype_name), serialized_value) is not None


def detect_serialized_value_datatype(serialized_value: any) -> str:

    if match_datatype_format(serialized_value, DTN_NULL):
        icap_type_name = DTN_NULL
    elif match_datatype_format(serialized_value, DTN_UUID):
        icap_type_name = DTN_UUID
    elif match_datatype_format(serialized_value, DTN_BOOLEAN):
        icap_type_name = DTN_BOOLEAN
    elif match_datatype_format(serialized_value, DTN_BIGINT):
        icap_type_name = DTN_BIGINT
    elif match_datatype_format(serialized_value, DTN_DOUBLE):
        icap_type_name = DTN_DOUBLE
    elif match_datatype_format(serialized_value, DTN_TIMESTAMP_TZ):
        icap_type_name = DTN_TIMESTAMP_TZ
    elif match_datatype_format(serialized_value, DTN_TIMESTAMP):
        icap_type_name = DTN_TIMESTAMP
    elif match_datatype_format(serialized_value, DTN_DATE):
        icap_type_name = DTN_DATE
    elif match_datatype_format(serialized_value, DTN_TIME):
        icap_type_name = DTN_TIME
    else:
        icap_type_name = DTN_STRING

    return icap_type_name


def is_string(native_value):

    return detect_native_value_datatype(native_value) == DTN_STRING
