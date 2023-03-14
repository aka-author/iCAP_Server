# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop_shortcuts.py                          (\(\
# Func:    Accessing an analytical shop metadata      (^.^)
# # ## ### ##### ######## ############# #####################

import sys, os, pathlib
import fields, workers, models


class ShopShortcut(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("shop_shortcut")


    def define_fields(self) -> 'ShopShortcut':

        self.get_field_manager()\
                .add_field(fields.UuidField("uuid"))\
                .add_field(fields.StringField("shop_name"))\
                .add_field(fields.StringField("details"))

        return self


    def get_shop_name(self) -> str:

        return self.get_field_value("shop_name")
    

    def get_package_name(self) -> str:

        return self.get_shop_name()


    def get_reporter_module_name(self):

        return self. get_package_name() + "_reporter"
    

    def get_processor_module_name(self):

        return self. get_package_name() + "_processor"