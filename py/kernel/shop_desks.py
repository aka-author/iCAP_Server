# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop_desks.py                            (\(\
# Func:    Accessing a set if analytical shops      (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List, Tuple

import workers, apps, desks, shop_shortcuts, shops, assay_responses


class ShopDesk(desks.Desk):

    def __init__(self, chief: apps.Application):

        super().__init__(chief)

        self.shop_shortcuts, self.shop_shortcuts_by_names = self.load_shop_shortcuts()


    def load_shop_shortcuts(self) -> Tuple[List, Dict]:

        loaded_shop_shortcuts = shops.ShopShortcut(self).load_all() 

        shop_shortcuts_by_names = {}

        for shop_shortcut in loaded_shop_shortcuts:
            shop_shortcuts_by_names[shop_shortcut.get_shop_name()] = shop_shortcut

        return loaded_shop_shortcuts, shop_shortcuts_by_names


    def new_shop(self) -> object:

        for shop in self.shops:
            shop_name = shop.get_shop_name()
            file_pointer, file_path, description = imp.find_module(shop_name)
            load_module = imp.load_module(shop_name, file_pointer, file_path, description)
            
        return shop


    def get_shop(self, shop_name: str) -> shops.Shop:

        return self.shops_by_names.get(shop_name)
    

    def get_failure_assay_response(self) -> assay_responses.AssayResponse:

        return assay_responses.FailureAssayResponse(self)