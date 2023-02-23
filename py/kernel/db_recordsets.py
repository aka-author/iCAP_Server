# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  dbrecordsets.py                              (\(\
# Func:    Implementing tables, queries, query results  (^.^)
# # ## ### ##### ######## ############# #####################

import utils, fields, workers


class FieldGroup(fields.FieldKeeper):

    def __init__(self, field_group_name: str, alias: str=None):

        super().__init__(field_group_name)

        self.alias = alias


    def get_field_group_name(self) -> str:

        return self.get_recordset_name()


    def set_alias(self, alias: str) -> 'Recordset':

        self.alias = alias

        return self


    def get_alias(self) -> str:

        return self.alias


class Recordset(workers.Worker):

    def __init__(self, chief: workers.Worker, recordset_name: str):

        super().__init__(chief)

        self.recordset_name = recordset_name

        self.fk = fields.FieldKeeper(recordset_name)

        self.field_groups = []
        self.field_groups_by_names = {}


    def get_recordset_name(self) -> str:

        return self.recordset_name


    def assemble_new_alias(self) -> str:

        return "t" + str(self.count_field_groups())


    def add_field_group(self, field_group_name: str, alias: str=None) -> 'Recordset':

        fg = FieldGroup(field_group_name, alias if alias is not None else self.assemble_new_alias())
        self.field_groups_enum[field_group_name] = len(self.field_groups)
        self.field_groups.append(fg)

        return self


    def has_field_group(self, field_group_name: str) -> bool:

        return field_group_name in self.field_groups_by_names


    def get_field_group(self, field_group_name: str) -> FieldGroup:

        return self.field_groups.get(field_group_name)


    def adapt_field(self, field: fields.Field, field_group_name: str=None) -> fields.Field:

        return field


    def add_field_to_group(self, field: fields.Field, field_group_name: str) -> 'Recordset':

        actual_group_name = field_group_name if field_group_name is not None else "default"

        if self.has_field_group(actual_group_name):
            self.add_field_group(actual_group_name)

        self.get_field_group(field_group_name).add_field(field)

        return self

    
    def add_field(self, field: fields.Field, field_group_name: str=None) -> 'Recordset':

        adapted_field = self.prepare_field(field, field_group_name)

        self.fk.add_field(adapted_field)
        self.add_field_to_group(adapted_field, field_group_name)

        return self


    def add_from_field_keeper(self, fk: fields.FieldKeeper, field_group_name: str=None) -> 'Recordset':

        actual_field_group_name = utils.safeval(field_group_name, fk.get_recordset_name())

        if self.has_field_group(actual_field_group_name):
            actual_field_group_name = utils.unique_name("g")

        for field_name in fk.get_field_names():
            self.add_field(fk.get_field(field_name), actual_field_group_name)

        return self