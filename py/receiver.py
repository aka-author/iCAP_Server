#!C:/Program Files/Python37/python
#encoding: utf-8

# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  receiver.py                               (\(\
# Func:    Saving measurements to a database         (^.^)
# # ## ### ##### ######## ############# ##################### 

import cgi, os, sys, math, json 
from distutils.command.config import config
from modules import script


class Receiver(script.Script):

    def do_the_job(self, request):
        
        log_file = open("log.txt", "a")

        log_file.write(str(self.get_req().get_payload()));

        log_file.write("\n");

Receiver().process_request()





