# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dtoms.py                                    (\(\
# Func:    Achieving compatibility with DTO formats    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List, Tuple
from datetime import datetime
import uuid
import datatypes, bureaucrat


class DtoMs(bureaucrat.Bureaucrat):

    def __init__(self, chief: bureaucrat.Bureaucrat):

        super().__init__(chief)


    def dto_varname(self, icap_varname: str) -> str:

        return icap_varname


    def dto_datatype_name(self, icap_datatype_name: str) -> str:

        dt_map = {
            datatypes.DTN_UUID:         "string", 
            datatypes.DTN_BOOLEAN:      "boolean",
            datatypes.DTN_NUMERIC:      "numeric",
            datatypes.DTN_BIGINT:       "numeric",
            datatypes.DTN_DOUBLE:       "numeric",
            datatypes.DTN_STRING:       "string",
            datatypes.DTN_STRLIST:      "string",
            datatypes.DTN_TIMESTAMP:    "string",
            datatypes.DTN_TIMESTAMP_TZ: "string",
            datatypes.DTN_DATE:         "string",
            datatypes.DTN_JSON:         "json"
        }

        return dt_map.get(icap_datatype_name, "string")


    def get_format_for_datatype(self, icap_datatype_name: str) -> bool:

        format_map = {
            datatypes.DTN_TIMESTAMP:    datatypes.get_default_timestamp_format(),
            datatypes.DTN_TIMESTAMP_TZ: datatypes.get_default_timestamp_tz_format(),
            datatypes.DTN_DATE:         datatypes.get_default_date_format(),
            datatypes.DTN_TIME:         datatypes.get_default_time_format()
        }

        return format_map.get(icap_datatype_name)


    def get_datetime_datatype_names(self) -> List:

        dt_names = [datatypes.DTN_TIMESTAMP, 
                    datatypes.DTN_TIMESTAMP_TZ, 
                    datatypes.DTN_DATE, 
                    datatypes.DTN_TIME]

        return dt_names


    def repair_value_from_dto(self, dto_value: any, icap_datatype_name: str) -> any:
        
        if icap_datatype_name == datatypes.DTN_UUID:
            try:
                native_value = uuid.UUID(dto_value)
            except:
                native_value = None
        elif icap_datatype_name in self.get_datetime_datatype_names():
            try:
                parse_format = self.get_format_for_datatype(icap_datatype_name)
                native_value = datetime.strptime(dto_value, parse_format)
            except:
                native_value = None
        else:
            native_value = dto_value
            
        return native_value


    def prapare_value_for_dto(self, native_value: any, icap_datatype_name: str) -> any:

        if native_value is None or datatypes.is_undefined(native_value):
            dto_value = None
        elif icap_datatype_name == datatypes.DTN_UUID:
            dto_value = str(native_value)
        elif icap_datatype_name in self.get_datetime_datatype_names():               
            serialize_format = self.get_format_for_datatype(icap_datatype_name)
            dto_value = datetime.strftime(native_value, serialize_format) 
        else:
            dto_value = native_value

        return dto_value