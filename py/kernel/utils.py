# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  utils.py                               (\(\
# Func:    Service functions                      (^.^)
# # ## ### ##### ######## ############# #####################

import os, hashlib, uuid, re, urllib.parse
from datetime import datetime


# Avoiding errors the None and empty strings may cause

def safeval(primary_value, default_value):

    return primary_value if primary_value is not None else default_value


def safestr(s):

    return s if s is not None else ""


def safearg(func, arg):

    return func(arg) if arg is not None else None


def is_empty(s: str) -> bool:

    return (s is None) or (s == "")


def is_useful(s: str) -> bool:

    return not is_empty(s)


def prefix(prefix: str, separ: str, term: str="") -> str:

    return (str(prefix) + str(separ) if is_useful(prefix) else "") + str(term)


def postfix(postfix: str, separ: str, term: str="") -> str:

    return term + (separ + postfix if is_useful(postfix) else "")


def infix(term1: str, infix: str, term2: str) -> str: 

    if is_useful(term1) and is_useful(term2):
        return str(term1) + str(infix) + str(term2)
    elif is_useful(term1) and is_empty(term2):
        return term1
    elif is_empty(term1) and is_useful(term2):
        return term2
    else:
        return ""
    

# Formatting, assembling, and processing strings

def is_str(some_value):

    return type(some_value) == type("foobar")


def snake_to_camel(snake):

    camel = snake[0]
    for idx in range(1, len(snake)):
        if snake[idx] != '_':
            if snake[idx-1] == "_":
                camel += snake[idx].upper()
            else:
                camel += snake[idx]      

    return camel


def is_latin_upper(c):

    return c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def camel_to_snake(camel):

    snake = camel[0]
    for idx in range(1, len(camel)):
        snake += "_" + camel[idx].lower() if is_latin_upper(camel[idx]) else camel[idx]
        
    return snake


def pad(s: str, left: str, right: str=None) -> str:

    return left + s + safeval(right, left)


def wspad(s: str) -> str:

    return pad(s, " ")


def pars(s: str) -> str:

    return pad(safestr(s), "(", ")") 


def brackets(s: str) -> str:

    return pad(safestr(s), "[", "]") 


def braces(s: str) -> str:

    return pad(safestr(s), "{", "}") 


def apos(s: str) -> str:

    return pad(safestr(s), "'") 


def quot(s):

    return pad(safestr(s), '"') 


def separate(s1, separ, s2):

    return s1 + s2 if s1 == "" or s2 == "" or s1.endswith(separ) \
           or s2.startswith(separ) else s1 + separ + s2
    

def md5(str):

    return hashlib.md5(str.encode("utf-8")).hexdigest()


def substring_before(s: str, separ: str) -> str:

    return s.split(separ)[0]


def substring_after(s: str, separ: str) -> str:

    return s.split(separ)[1]


# UUID and unique names

def str2uuid(str):

    native_uuid = None

    try:
        native_uuid = uuid.UUID(str)
    except:
        native_uuid = None

    return native_uuid 


def unique_name(prefix: str="n") -> str: 

    return prefix + str(uuid.uuid4()).replace("-", "")


# Date & time

def get_default_timestamp_format():

    return "%Y-%m-%d %H:%M:%S.%f"


class TimestampFormat():

    def __init__(self, format_name=None, format_string=None):

        self.format_name = format_name
        self.format_string = format_string


    def get_format_name(self):

        return self.format_name


    def get_format_string(self):

        return self.format_string
    

    def is_defined(self):

        return self.get_format_name() is not None


    def get_formats(self):

        return {
            "i12_date": 
                {"fstring": "%Y-%m-%d", 
                 "regexp": "^\d{4}\-\d\d\-\d\d$"},
            "i12_datetime": 
                {"fstring": "%Y-%m-%d %H:%M:%S", 
                 "regexp": "^\d{4}\-\d\d\-\d\d \d\d:\d\d:\d\d$"},
            "i12_datetime_with_ms": 
                {"fstring": "%Y-%m-%d %H:%M:%S.%f", 
                 "regexp": "^\d{4}\-\d\d\-\d\d \d\d:\d\d:\d\d\.\d*$"},
            "i12_datetime_with_utc": 
                {"fstring": None, 
                 "regexp": "^(\d{4}\-\d\d\-\d\d \d\d:\d\d:\d\d)(\.\d*)? UTC[\+|\-]\d\d$"}
        }


    def get_format_string_by_name(self, format_name):

        format_info = self.get_formats().get(format_name)

        return format_info.get("fstring") if format_info is not None else "" 


    def detect(self, s):

        formats = self.get_formats()

        for format_name in formats:
            if re.search(formats[format_name]["regexp"], s) is not None:
                self.format_name = format_name
                self.format_string = formats[format_name]["fstring"]
                break

        return self


def timestamp2str(timestamp, format=None):
    
    actual_format = safeval(format, get_default_timestamp_format())

    return datetime.strftime(timestamp, actual_format) if timestamp is not None else None    


def str2timestamp(src_s, format_string=None):

    ts = None

    if format_string is not None:
        ts = datetime.strptime(s, format_string)
    else:
        format = TimestampFormat().detect(src_s)

        if format.is_defined():

            if format.get_fname() == "i12_datetime_with_utc":
                s = src_s.split(" UTC")[0]
                f = format.get_fstring_by_fname("i12_datetime_with_ms")
            else:
                s = src_s
                f = format.get_fstring()
            
            ts = datetime.strptime(s, f)

    return ts


def strnow():

    return timestamp2str(datetime.now())


# CGI 

def check_content_type(content_type: str) -> bool:

    return content_type in os.environ.get("CONTENT_TYPE", "Not provided")


def extract_fields_from_url_encoded_form(form_urlencoded):

    params = {}

    param_pairs = form_urlencoded.split("&")
    for param_pair in param_pairs:
        param_pair_arr = param_pair.split("=")
        params[param_pair_arr[0]] = urllib.parse.unquote(param_pair_arr[1])

    return params


def extract_fields_from_storage(fs):

    params = {}
    
    for param_name in fs:
        params[param_name] = fs[param_name].value

    return params


def cgi_baundary(content_type: str) -> str:

    return substring_after(content_type, "boundary=")


def cgi_form_field(body: str, content_type: str) -> str:

    boundary = cgi_baundary(content_type)

    items = body.split(boundary)

    return items[1] if len(items) > 1 else ""  


def extract_json_body_from_pseudoform(cgi_body, ctype):
    tmp = cgi_form_field(cgi_body, ctype)
    items = tmp.split("\n")
    pseudo = "\n".join([items[i] for i in range(3,len(items)-1)])
    return pseudo