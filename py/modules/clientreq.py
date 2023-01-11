# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  clientreq.py                             (\(\
# Func:    Accessing client request data            (^.^) 
# # ## ### ##### ######## ############# #####################

import json
from . import utils


class ClientRequest:

    def __init__(self, environ, field_storage, body):

        self.environ = environ
        self.field_storage = field_storage
        self.body = body


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

        return self.field_storage[field_name].value if field_name in self.field_storage else None


    def get_single_field(self):

        return self.field_storage[self.field_storage.keys()[0]].value


    def get_credentials(self):

        username = self.get_field("user") 
        password = self.get_field("password")

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


    def get_payload(self):

        payload = None

        content_type = self.get_content_type()
                            
        if content_type == "application/json":
            payload = json.loads(self.body) 
        elif content_type == "multipart/form-data":
            payload = json.loads(self.get_single_field())
            
        return payload