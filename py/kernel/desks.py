# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   desks.py                                    (\(\
# Func:     The base class for UserDesk and other desks (^.^)
# # ## ### ##### ######## ############# #####################

import workers, db_instances


class Desk(workers.Worker):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def set_db(self, db: db_instances.Db) -> 'Desk':

        self.db = db

        return self


    def get_db(self) -> db_instances.Db:

        return self.db