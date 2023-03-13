# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop.py                                      (\(\
# Func:    Giving a portotype for each analytical shop  (^.^)
# # ## ### ##### ######## ############# #####################

import workers, models

class Shop(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.model_name = "shop"


    def set_shop_name(self, shop_name: str) -> workers.Worker:

        self.shop_name = shop_name


    def get_shop_name(self) -> str:

        return self.shop_name


    def build_report(self, request):






    
    