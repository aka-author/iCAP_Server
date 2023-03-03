# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  db_instances.py                      (\(\
# Func:    Working with database structures     (^.^)
# # ## ### ##### ######## ############# ##################### 

from typing import Dict 
import workers, db_objects


class Db(workers.Worker):

    def __init__(self, chief: workers.Worker, connection_params: Dict):

        super().__init__(chief)

        self.connetion_params = connection_params

        self.schemes = []
        self.schemes_by_names = {}


    def get_dbms(self):

        return self.get_chief()
    

    def get_connection_param(self, param_name: str) -> str:

        return self.connetion_params.get(param_name)


    def add_scheme(self, scheme: db_objects.Scheme) -> 'Db':

        self.schemes.append(scheme)
        self.schemes_by_names[scheme.get_table_name()] = scheme

        return self


    def get_table(self, scheme_name: str) -> db_objects.Table:

        return self.schemes.get(scheme_name)