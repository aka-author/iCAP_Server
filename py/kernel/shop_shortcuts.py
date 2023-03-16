# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  shop_shortcuts.py                          (\(\
# Func:    Accessing an analytical shop metadata      (^.^)
# # ## ### ##### ######## ############# #####################

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


    def get_module_name(self, local: str) -> str:

        return "_".join([self.get_package_name(), local])


    def get_module_full_name(self, module_name: str) -> str:

        return ".".join([self.get_package_name(), module_name])


    def get_admin_module_full_name(self):

        return self.get_module_full_name(self.get_module_name("admin"))
    

    def get_processor_module_full_name(self):

        return self.get_module_full_name(self.get_module_name("processor"))
    

    def get_reporter_module_full_name(self):

        return self.get_module_full_name(self.get_module_name("reporter"))