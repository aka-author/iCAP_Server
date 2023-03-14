# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop_desks.py                            (\(\
# Func:    Accessing a set if analytical shops      (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List, Tuple
import importlib
import workers, desks, shop_shortcuts, shops, assayresp


class ShopDesk(desks.Desk):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.shop_shortcuts, self.shop_shortcuts_by_names = self.load_shop_shortcuts()


    def load_shop_shortcuts(self) -> Tuple[List, Dict]:

        loaded_shop_shortcuts = shop_shortcuts.ShopShortcut(self).load_all() 

        shop_shortcuts_by_names = {}

        for shop_shortcut in loaded_shop_shortcuts:
            shop_shortcuts_by_names[shop_shortcut.get_shop_name()] = shop_shortcut

        return loaded_shop_shortcuts, shop_shortcuts_by_names


    def get_shop_shortcut(self, shop_name: str) -> shop_shortcuts.Shop:

        return self.shop_shortcuts_by_names.get(shop_name)
    

    def involve_shop(self, shop_name: str) -> shops.Shop:

        return None
    

    def get_failure_assay_response(self) -> assayresp.AssayResponse:

        return assayresp.FailureAssayResponse(self)