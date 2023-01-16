# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  bureaucrat.py                               (\(\
# Func:    Giving a pattern for all the objects here   (^.^)
# # ## ### ##### ######## ############# ##################### 

import uuid
import status, utils


class Bureaucrat:

    def __init__(self, chief=None):

        self.chief = chief
        self.id = uuid.uuid4()
        
        self.status_code = status.OK

        self.app = None
        self.cfg = None
        self.dbl = None
        self.req = None


    def set_chief(self, chief):

        self.chief = chief

        return self


    def get_chief(self):

        return self.chief


    def get_id(self):

        return self.id 


    def set_status_code(self, status_code):

        self.status_code = status_code

        return self


    def get_status_code(self):

        return self.status_code


    def isOK(self):

        return self.get_status_code() == status.OK


    def get_app(self):

        return utils.safeval(self.app, self.get_chief().get_app())    


    def set_cfg(self, cfg):

        self.cfg = cfg

        return self


    def get_cfg(self):

        return self.cfg if self.cfg is not None \
               else (self.get_chief().get_cfg() if self.get_chief() is not None \
               else None)     


    def set_dbl(self, dbl):

        self.dbl = dbl

        return self


    def get_dbl(self):

        return utils.safeval(self.dbl, self.get_chief().get_dbl())  

    
    def set_req(self, req):

        self.req = req

        return self


    def get_req(self):

        return utils.safeval(self.req, self.get_chief().get_req())