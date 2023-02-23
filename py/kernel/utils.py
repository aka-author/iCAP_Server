# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  utils.py                               (\(\
# Func:    Service functions                      (^.^)
# # ## ### ##### ######## ############# #####################

import hashlib, uuid, re
from datetime import datetime


# Avoiding None-related errors 

def safeval(primary_value, default_value):

    return primary_value if primary_value is not None else default_value


def safestr(s):

    return s if s is not None else ""


def safedic(dic, key, default_value=None):

    return safeval((dic[key] if key in dic else None) if dic is not None else None, default_value) 


def safearg(func, val):

    return func(val) if val is not None else None


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


def pars(s):

    return "(" + safeval(s, "") + ")" 


def apos(s):

    return "'" + safeval(str(s), '') + "'" 


def quot(s):

    return '"' + safeval(str(s), "") + '"' 


def escsql(s):

    return s.replace("'", "''")


def consep(prefix, separ, postfix):

    if prefix is not None and postfix is not None:
        return prefix + separ + postfix
    elif prefix is None:
        return postfix
    else:
        return prefix


def separate(s1, separ, s2):

    return s1 + s2 if s1 == "" or s2 == "" or s1.endswith(separ) \
           or s2.startswith(separ) else s1 + separ + s2
    

def md5(str):

    return hashlib.md5(str.encode("utf-8")).hexdigest()


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


def timestamp2str(timestamp, custom_format=None):

    format = safeval(custom_format, get_default_timestamp_format())

    return datetime.strftime(timestamp, format) if timestamp is not None else None


class TimestampFormat():

    def __init__(self, fname=None, fstring=None):

        self.fname = fname
        self.fstring = fstring


    def is_defined(self):

        return self.get_fname() is not None


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


    def get_fstring_by_fname(self, fname):

        return safedic(safedic(self.get_formats(), fname), "fstring")


    def detect(self, s):

        formats = self.get_formats()

        for fname in formats:
            if re.search(formats[fname]["regexp"], s) is not None:
                self.fname, self.fstring = fname, formats[fname]["fstring"]
                break

        return self


    def get_fname(self):

        return self.fname


    def get_fstring(self):

        return self.fstring


def str2timestamp(src_s, custom_fstring=None):

    ts = None

    if custom_fstring is not None:
        ts = datetime.strptime(s, custom_fstring)
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

def extract_fields_from_url_encoded_form(form_urlencoded):

    params = {}

    param_pairs = form_urlencoded.split("&")
    for param_pair in param_pairs:
        param_pair_arr = param_pair.split("=")
        params[param_pair_arr[0]] = param_pair_arr[1]

    return params


def extract_fields_from_storage(fs):

    params = {}

    for param_name in fs:
        params[param_name] = fs[param_name].value

    return params