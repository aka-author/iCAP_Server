# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop_desks.py                            (\(\
# Func:    Accessing a set if analytical shops      (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List, Tuple
import sys, os, pathlib, importlib
import workers, desks, shop_shortcuts, shops, assayresp

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.absolute()) + "/shops"))


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


    def has_shop(self, shop_name: str) -> bool:

        return shop_name in self.shop_shortcuts_by_names


    def get_shop_shortcut(self, shop_name: str) -> shop_shortcuts.ShopShortcut:

        return self.shop_shortcuts_by_names.get(shop_name)
    

    def involve_shop_reporter(self, shop_name: str) -> shops.Shop:

        if self.has_shop(shop_name):

            shop_shortcut = self.get_shop_shortcut(shop_name)
            shop_package_name = shop_shortcut.get_package_name()
            reporter_module_name = shop_shortcut.get_reporter_module_name()

            shop_module = importlib.import_module(reporter_module_name, shop_package_name)

            shop_reporter = shop_module.new_shop(self)
        else:
            shop_reporter = None

        return shop_reporter
    

    def get_failure_assay_response(self) -> assayresp.AssayResponse:

        return assayresp.FailureAssayResponse(self)