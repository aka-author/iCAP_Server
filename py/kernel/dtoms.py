# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dtoms.py                                    (\(\
# Func:    Achieving compatibility with DTO formats    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List, Tuple
from datetime import datetime
import uuid, re
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
            datatypes.DTN_OBJECT:       "object",
            datatypes.DTN_JSON:         "json"
        }

        return dt_map.get(icap_datatype_name, "string")


    def get_datetime_datatype_names(self) -> List:

        dt_names = [datatypes.DTN_TIMESTAMP, 
                    datatypes.DTN_TIMESTAMP_TZ, 
                    datatypes.DTN_DATE, 
                    datatypes.DTN_TIME]

        return dt_names


    def get_format_for_datatype(self, icap_datatype_name: str) -> bool:

        format_map = {       
            datatypes.DTN_TIMESTAMP:    datatypes.get_default_timestamp_format(),
            datatypes.DTN_TIMESTAMP_TZ: datatypes.get_default_timestamp_tz_format(),
            datatypes.DTN_DATE:         datatypes.get_default_date_format(),
            datatypes.DTN_TIME:         datatypes.get_default_time_format()
        }

        return format_map.get(icap_datatype_name)


    def get_datatype_regexp(self, icap_datatype_name: str) -> str:

        format_map = {                  
            datatypes.DTN_UUID:         "^[\dA-Fa-f]{8}(\-([\dA-Fa-f]{4})){3}\-[\dA-Fa-f]{12}$",
            datatypes.DTN_TIMESTAMP:    "^\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d\.(\d+)$",
            datatypes.DTN_TIMESTAMP_TZ: "^\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d\.(\d+) [+\-]\d\d:\d\d$",
            datatypes.DTN_DATE:         "^\d{4}\-\d\d\-\d\d$",
            datatypes.DTN_TIME:         "^\d\d:\d\d:\d\d$"
        }

        return format_map.get(icap_datatype_name, ".*")


    def match_datatype(self, serialized_value: str, icap_datatype_name: str) -> str:

        return re.search(self.get_datatype_regexp(icap_datatype_name), serialized_value) is not None


    def detect_datatype(self, dto_value: any) -> str:

        if isinstance(dto_value, bool):
            icap_type_name = datatypes.DTN_BOOLEAN
        elif isinstance(dto_value, int):
            icap_type_name = datatypes.DTN_BIGINT
        elif isinstance(dto_value, float):
            icap_type_name = datatypes.DTN_DOUBLE
        elif isinstance(dto_value, list):
            icap_type_name = datatypes.DTN_OBJECT
        elif isinstance(dto_value, dict):
            icap_type_name = datatypes.DTN_OBJECT
        elif isinstance(dto_value, str):
            if self.match_datatype(dto_value, datatypes.DTN_UUID):
                icap_type_name = datatypes.DTN_UUID
            elif self.match_datatype(dto_value, datatypes.DTN_TIMESTAMP_TZ):
                icap_type_name = datatypes.DTN_TIMESTAMP_TZ
            elif self.match_datatype(dto_value, datatypes.DTN_TIMESTAMP):
                icap_type_name = datatypes.DTN_TIMESTAMP
            elif self.match_datatype(dto_value, datatypes.DTN_DATE):
                icap_type_name = datatypes.DTN_DATE
            elif self.match_datatype(dto_value, datatypes.DTN_TIME):
                icap_type_name = datatypes.DTN_TIME
            else:
                icap_type_name = datatypes.DTN_STRING

        return icap_type_name
            

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
        elif icap_datatype_name == datatypes.DTN_OBJECT:
            native_value = self.repair_object(dto_value)
        else:
            native_value = dto_value
            
        return native_value


    def repair_object(self, obj: Dict) -> object:

        for (prop_name, prop_value) in obj.items():
            if isinstance(prop_value, str):
                icap_datatype_name = self.detect_datatype(prop_value)
                obj[prop_name] = self.repair_value_from_dto(prop_value, icap_datatype_name)
            elif isinstance(prop_value, list):
                for item_idx, item_value in enumerate(prop_value):
                    icap_datatype_name = self.detect_datatype(item_value)
                    if icap_datatype_name == datatypes.DTN_OBJECT:
                        self.detect_datatype(item_value)
                    else:
                        prop_value[item_idx] = self.repair_value_from_dto(item_value, icap_datatype_name)   
            elif isinstance(prop_value, dict):
                self.repair_object(prop_value)

        return self


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


    def set_prop(self, prop_name, native_value, source_icap_datatype_name) -> object:

        self.payload[prop_name] = self.prapare_value_for_dto(native_value, source_icap_datatype_name)

        return self


    def get_prop(self, prop_name: str, required_icap_datatype_name: str) -> any:

        

        return 


d = DtoMs(None)


pl = {
    "uuid": "fd3034bd-565b-4823-81f4-19cc2f47915f",
    "name": "Tuzik",
    "weight": 12,
    "date_of_birth": "2020-03-12",
    "arnocles": ["2020-03-12", "2020-03-13", "2020-03-14"],
    "arnocles2": [{"foo": ["a", "b", "c"]}, "2020-03-12 10:10:10.123456", "2020-03-13 10:10:10.123456", "2020-03-14 10:10:10.123456"],
    "arnocles3": {"pivo": "raki"}
}

d.repair_object(pl)

print(pl)