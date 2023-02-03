# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dtoms.py                                    (\(\
# Func:    Achieving compatibility with DTO formats    (^.^)
# # ## ### ##### ######## ############# #####################

import utils, datatypes, bureaucrat


class DtoMs(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def dto_datatype_name(self, icap_datatype_name):

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
            datatypes.DTN_JSON:         "json"
        }

        return utils.safeval(utils.safedic(dt_map, icap_datatype_name), "string")


    def get_format_for_datatype(self, icap_datatype_name):

        format_map = {
            datatypes.DTN_TIMESTAMP:    "%Y-%m-%d %H:%M:%S.%f",
            datatypes.DTN_TIMESTAMP_TZ: "%Y-%m-%d %H:%M:%S.%f %z"
        }

        return utils.safedic(format_map, icap_datatype_name)


    def dto_varname(self, icap_varname):

        return icap_varname


    def dto_value(self, raw_dto_value, icap_datatype_name):

        return utils.safeval(raw_dto_value, "undefined")