# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dtos.py                                  (\(\
# Func:    Working with data transfer objects       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
from datetime import datetime
import copy, uuid
import datatypes


class Dto():

    def __init__(self, payload):

        self.payload = payload

        
    # Converting properties from JSON datatypes to iCAP datatypes 

    def detect_value_datatype(self, dto_value: any) -> str:

        if datatypes.is_string(dto_value):
            return datatypes.detect_serialized_value_datatype(dto_value)
        else:   
            return datatypes.detect_native_value_datatype(dto_value)
                     

    def repair_value_datatype(self, dto_value: any) -> any:

        icap_datatype_name = self.detect_value_datatype(dto_value)

        if icap_datatype_name == datatypes.DTN_UUID:
            native_value = uuid.UUID(dto_value)            
        elif datatypes.is_datetime_datatype(icap_datatype_name):
            parse_format = datatypes.get_format(icap_datatype_name)
            native_value = datetime.strptime(dto_value, parse_format)
        elif icap_datatype_name == datatypes.DTN_DICT:
            native_value = self.import_src_dict(dto_value)
        else:
            native_value = dto_value
            
        return native_value


    def repair_listitem_datatypes(self, dto_list: List) -> object:

        for listitem_idx, listitem_value in enumerate(dto_list):           
            if isinstance(listitem_value, list):
                self.repair_listitem_datatypes(listitem_value)
            if isinstance(listitem_value, dict):
                self.repair_prop_datatypes(listitem_value)
            else:
                dto_list[listitem_idx] = self.repair_value_datatype(listitem_value)  

        return self


    def repair_prop_datatypes(self, dto_dict: Dict) -> object:

        for (prop_name, prop_value) in dto_dict.items():
            if isinstance(prop_value, list):
                self.repair_listitem_datatypes(prop_value)
            elif isinstance(prop_value, dict):
                self.repair_prop_datatypes(prop_value)
            else:
                dto_dict[prop_name] = self.repair_value_datatype(prop_value)

        return self


    def repair_datatypes(self) -> object: 

        self.repair_prop_datatypes(self.payload)

        return self


    # Exporting a DTO for serialization

    def dto_varname(self, icap_varname: str) -> str:

        return icap_varname


    def prepare_value_datatype(self, native_value: any) -> any:

        icap_datatype_name = self.detect_value_datatype(native_value)

        if icap_datatype_name == datatypes.DTN_UUID:
            native_value = str(native_value)            
        elif datatypes.is_datetime_datatype(icap_datatype_name):
            parse_format = datatypes.get_format(icap_datatype_name)
            native_value = datetime.strftime(native_value, parse_format)
        elif icap_datatype_name == datatypes.DTN_DICT:
            native_value = self.import_src_dict(native_value)
        else:
            native_value = native_value
            
        return native_value


    def prepare_listitem_datatypes(self, native_list: List) -> object:

        for listitem_idx, listitem_value in enumerate(native_list):           
            if isinstance(listitem_value, list):
                self.prepare_listitem_datatypes(listitem_value)
            if isinstance(listitem_value, dict):
                self.prepare_prop_datatypes(listitem_value)
            else:
                native_list[listitem_idx] = self.prepare_value_datatype(listitem_value)  

        return self


    def prepare_prop_datatypes(self, native_dict) -> any:

        for (prop_name, prop_value) in native_dict.items():
            if isinstance(prop_value, list):
                self.prepare_listitem_datatypes(prop_value)
            elif isinstance(prop_value, dict):
                self.prepare_prop_datatypes(prop_value)
            else:
                native_dict[prop_name] = self.prepare_value_datatype(prop_value)

        return native_dict


    def export_payload(self) -> Dict:

        return self.prepare_prop_datatypes(copy.deepcopy(self.payload))


    # Accessing DTO properties

    def get_payload(self):

        return self.payload


    def set_prop(self, prop_name, native_value) -> object:

        self.payload[prop_name] = native_value

        return self


    def get_prop(self, prop_name: str) -> any:

        return self.payload.get(prop_name)


    def count_nested(self, prop_name: str) -> int:

        prop_value = self.get_prop(prop_name)

        if isinstance(prop_value, dict) or isinstance(prop_value, list):
            return len(prop_name)
        else:
            return 0


    def extract_dto(self, prop_name: str, index_key: int=None) -> object:

        prop_value = self.get_prop(prop_name)

        payload = prop_value[index_key] if index_key is not None else prop_value(prop_name)

        return Dto(payload)