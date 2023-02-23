# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop.py                                      (\(\
# Func:    Giving a portotype for each analytical shop  (^.^)
# # ## ### ##### ######## ############# #####################

import workers

class Shop(workers.Worker):

    def __init__(self, chief: workers.Worker, shop_name: str):

        super().__init__(chief)

        self.shop_name = shop_name


    def get_shop_name(self) -> str:

        return self.shop_name


    def build_report(self, request):






    
    