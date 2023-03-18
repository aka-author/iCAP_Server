# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  performer_shortcuts.py                (\(\
# Func:    Accessing metadata of a performer     (^.^)
# # ## ### ##### ######## ############# #####################

import fields, workers, models


class PerformerShortcut(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("performer_shortcut")


    def define_fields(self) -> 'PerformerShortcut':

        self.get_field_manager()\
                .add_field(fields.UuidField("uuid"))\
                .add_field(fields.StringField("performer_name"))\
                .add_field(fields.StringField("performer_title"))\
                .add_field(fields.StringField("master_app_name"))\
                .add_field(fields.StringField("details"))

        return self


    def get_performer_name(self) -> str:

        return self.get_field_value("performer_name")
    

    def get_package_name(self) -> str:

        return self.get_performer_name()
    

    def get_performer_title(self) -> str:

        return self.get_field_value("performer_title")
    

    def get_master_app_name(self) -> str:

        return self.get_field_value("master_app_name")


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