# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop.py                                      (\(\
# Func:    Giving a portotype for each analytical shop  (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat

class Shop(bureaucrat.Bureaucrat):

    def __init__(self, chief, shop_name):

        super().__init__(chief)

        self.shop_name = shop_name


    def get_shop_name(self):

        return self.shop_name


    def build_report(self, request):






    
    