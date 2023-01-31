# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  restreq.py                              (\(\
# Func:    Reading data from REST requests         (^.^) 
# # ## ### ##### ######## ############# #####################

import json
import status, utils


class RestRequest:

    def __init__(self, environ, params, body):

        self.status_code = status.OK

        self.environ = environ
        self.form_fields = params
        self.body = body


    def set_status_code(self, status_code):

        self.status_code = status_code


    def get_status_code(self):

        return self.status_code


    # Working with HTTP headers

    def get_http_header(self, header_name):

        envname = ("http_" + header_name).upper()

        return self.environ[envname] if envname in self.environ else None      


    def get_cookie(self):

        return self.get_http_header("COOKIE")


    def get_host(self):

        return self.get_http_header("HOST")


    def get_content_type(self):

        ct_raw = utils.safedic(self.environ, "CONTENT_TYPE")

        return None if ct_raw == None else (ct_raw.split(";")[0] if ";" in ct_raw else ct_raw)


    # Working with form fields

    def get_form_field(self, field_name):

        return self.form_fields[field_name] if field_name in self.form_fields else None


    def get_pseudofield(self):

        field_names = self.form_fields.keys()

        return self.params[field_names[0]] if len(field_names) > 0 else ""


    def get_credentials(self):

        username = utils.safeval(self.get_form_field("username"), "") 
        password = utils.safeval(self.get_form_field("password"), "")

        return username, password


    # Working with in path parameters

    def get_in_path_param(self, param_name):

        param_value = ""

        params = self.environ["REQUEST_URI"].split("/")

        probable_param_name = ""

        for clause in params:

            if probable_param_name == param_name:
                param_value = clause
                break

            probable_param_name = clause

        return param_value


    # Working with a body and payload

    def get_body(self):

        return self.body


    def has_pseudofield(self):

        return "unloadMeasurement" in self.form_fields or "pseudofield" in self.form_fields


    def get_serialized_payload(self):

        s_payload = ""
        
        c_type = self.get_content_type()

        if c_type == "application/json":
            s_payload = self.get_body() 
        elif c_type == "multipart/form-data": 
            if self.has_pseudofield():
                s_payload = self.get_pseudofield()

        return s_payload


    def get_payload(self):

        payload = {}        

        try:
            payload = json.loads(self.get_serialized_payload())
        except:
            self.set_status_code(status.ERR_INCORRECT_REQUEST)
            
        return payload


    def serialize(self):

        return "Content-type:" + str(self.get_content_type()) + "\\n" + self.get_body().replace("\n", "\\n")