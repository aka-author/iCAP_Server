# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  worker.py                               
# Func:    Giving a pattern for all the objects here    (\(\
# Usage:   The class is abstract                        (^.^)
# # ## ### ##### ######## ############# ##################### 

from typing import Dict
import uuid
import status


class Worker:

    def __init__(self, chief: 'Worker'=None):

        self.chief = chief
        self.id = uuid.uuid4()
        
        self.status_code = status.OK

        self.app = None
        self.cfg = None
        self.default_dbms = None
        self.default_db = None
        self.default_db_scheme_name = None
        self.req = None


    def set_chief(self, chief: 'Worker') -> 'Worker':

        self.chief = chief

        return self


    def has_chief(self) -> bool:

        return self.chief is not None
    

    def get_chief(self) -> 'Worker':

        return self.chief


    def get_id(self) -> uuid.UUID:

        return self.id 


    def set_status_code(self, status_code: int) -> 'Worker':

        self.status_code = status_code

        return self


    def get_status_code(self) -> int:

        return self.status_code


    def isOK(self) -> bool:

        return self.get_status_code() == status.OK


    def get_app(self) -> 'Worker':

        return self.app if self.app is not None \
               else (self.get_chief().get_app() if self.get_chief() is not None \
               else None) 


    def set_cfg(self, cfg: Dict) -> 'Worker':

        self.cfg = cfg

        return self


    def get_cfg(self) -> Dict:

        return self.cfg if self.cfg is not None \
               else (self.get_chief().get_cfg() if self.get_chief() is not None \
               else None)     


    def get_default_dbms(self) -> object:

        return self.default_dbms if self.default_dbms is not None \
                else (self.get_chief().get_default_dbms() if self.has_chief() \
                else None)

    
    def get_default_db(self) -> object:

        return self.default_db if self.default_db is not None \
                else (self.get_chief().get_default_db() if self.has_chief() \
                else None)


    def get_default_db_scheme_name(self) -> str:

        return self.default_db_scheme_name if self.default_db_scheme_name is not None \
                else (self.get_chief().get_default_db_scheme_name() if self.has_chief() \
                else None)


    def set_req(self, req: object) -> object:

        self.req = req

        return self


    def get_req(self) -> object:

        return self.req if self.req is not None \
               else (self.get_chief().get_req() if self.get_chief() is not None \
               else None)


    def is_debug_mode(self) -> bool:

        return self.get_app().is_debug_mode()


    def is_console_mode(self) -> bool:

        return self.get_app().is_console_mode()


    def is_cgi_mode(self) -> bool:

        return self.get_app().is_cgi_mode()


    def is_batch_mode(self) -> bool:

        return self.get_app().is_batch_mode()


    def deb(self, debinfo: str) -> None:

        if self.get_cfg().is_debug_mode():
            print(debinfo)