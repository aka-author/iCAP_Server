# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  controller.py                               (\(\
# Func:    Defining common behavior of controllers     (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat


class Controller(bureaucrat.Bureaucrat):

    def __init__(self, chief=None):

        super().__init__(chief)


    def get_result_format_ver(self, payload_type_name):

        return 1


    def export_result_dto(self, status_code, payload_type_name=None, payload_dto=None):

        dto = {
            "ver": self.get_result_format_ver(payload_type_name),
            "statusCode": status_code,
            "payloadTypeName": payload_type_name,
            "payload": payload_dto
        }
        
        return dto