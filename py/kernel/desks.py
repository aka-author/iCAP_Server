# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   desks.py                                    (\(\
# Func:     The base class for UserDesk and other desks (^.^)
# # ## ### ##### ######## ############# #####################

import workers


class Desk(workers.Worker):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)