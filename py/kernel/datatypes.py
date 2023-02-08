# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  datatypes.py                                 (\(\
# Func:    Using unisied data types over the platform   (^.^)
# # ## ### ##### ######## ############# #####################

# Atomic data types 

DTN_UUID         = "uuid" 
DTN_BOOLEAN      = "boolean"
DTN_NUMERIC      = "numeric"
DTN_BIGINT       = "bigint"
DTN_DOUBLE       = "double"
DTN_STRING       = "string"
DTN_STRLIST      = "strlist"
DTN_TIMESTAMP    = "timestamp"
DTN_TIMESTAMP_TZ = "timestamp_tz"
DTN_DATE         = "date"
DTN_JSON         = "json"
DTN_UNDEFINED    = "fd3034bd-565b-4823-81f4-19cc2f47915f"


#  Detecting atomic data types

def get_atomic_datatype_names():

    return [DTN_UUID, DTN_BOOLEAN, DTN_BIGINT, DTN_DOUBLE, DTN_STRING, \
            DTN_STRLIST, DTN_TIMESTAMP, DTN_TIMESTAMP_TZ, DTN_DATE, DTN_JSON]


def is_atomic(datatype_name):

    return datatype_name.lower() in get_atomic_datatype_names()


def is_undefined(some_value):

    return some_value == DTN_UNDEFINED


# Timestamps

def get_default_timestamp_format():

    return "%Y-%m-%d %H:%M:%S.%f"


def get_default_timestamp_tz_format():

    return "%Y-%m-%d %H:%M:%S.%f %z" 


def get_default_date_format():

    return "%Y-%m-%d" 