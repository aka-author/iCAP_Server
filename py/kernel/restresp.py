# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  restresp.py                                (\(\
# Func:    Assembling text for an HTTP responce       (^.^)                                                                                                                                            
# # ## ### ##### ######## ############# #####################

import dtos
import json


class RestResponse: 

    def __init__(self):

        self.result_code = 200
        self.result_wording = "OK"
        self.headers = {}
        self.body = None 
        self.serialized_text = None


    # Result 

    def set_result_code(self, code: int, wording: str) -> 'RestResponse':

        self.result_code = code
        self.result_wording = wording

        return self


    def set_result_401(self) -> 'RestResponse':

        self.set_result_code(401, "Unauthorized")
    
        return self


    def set_result_404(self) -> 'RestResponse':

        self.set_result_code(404, "Not found")

        return self
    

    def set_result_500(self) -> 'RestResponse':

        self.set_result_code(500, "Internal server error")

        return self


    def get_result_code(self) -> int:

        return self.result_code


    def get_result_wording(self) -> str:

        return self.result_wording
    

    def serialize_result(self) -> str:

        return "Status: " + str(self.get_result_code()) + " " + self.get_result_wording() + "\n"


    # HTTP headers

    def set_header(self, header_name: str, content: str) -> 'RestResponse':

        self.headers[header_name] = content

        return self


    def get_header(self, header_name: str) -> str:

        return self.headers.get(header_name)


    def serialize_header(self, header_name: str) -> str:

        return header_name + ": " + self.headers[header_name] if header_name in self.headers else ""


    # Body

    def is_empty(self) -> bool:

        return self.body is None


    def set_content_type(self, content_type: str) -> 'RestResponse':
   
        self.set_header("Content-type", content_type) 

        return self


    def get_content_type(self) -> str:

        return self.get_header("Content-type")


    def set_body(self, content: str, content_type: str="application/json") -> 'RestResponse':

        self.set_header("Content-type", content_type)

        self.body = content

        return self


    def get_body(self) -> str:

        return self.body


    def serialize_body(self) -> str:

        content_type = self.get_content_type()

        if content_type == 'application/json':

            # tmp_dto = dtos.Dto(self.get_body())
            # print(self.get_body())
            # serializable_body = tmp_dto.export_payload()

            try:
                body_text = json.dumps(self.get_body())
            except:
                body_text = json.dumps({"error:": "Failed to serialize body"})
        else:
            body_text = self.get_body()
        
        return body_text


    # Entire response

    def serialize(self) -> str:

        if self.serialized_text is None:

            self.serialized_text = self.serialize_result() 

            if self.is_empty():
                self.set_header("Content-length", "0")

            self.serialized_text += "\n".join([self.serialize_header(header_name) for header_name in self.headers])
        
            self.serialized_text += "\n"

            if not self.is_empty() and self.get_result_code() == 200:
                self.serialized_text += "\n" + self.serialize_body()  

        return self.serialized_text