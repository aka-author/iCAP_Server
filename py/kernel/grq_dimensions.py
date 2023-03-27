# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  grq_dimensions.py                             (\(\
# Func:    Defining one of gpouping diensions           (^.^)
# # ## ### ##### ######## ############# #####################

import fields, dtos, workers, models, grq_groups


class Dimension(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.groups = []


    def define_fields(self) -> models.Model:

        self.get_field_manager()\
                .add_field(fields.StringField("varname"))\
                .add_field(fields.StringField("group_by_value_datatype_name"))

        return self
    

    def get_varname(self) -> str:

        return self.get_field_value("varname")
    

    def get_group_by_value_datatype_name(self):

        return self.get_field_value("group_by_value_datatype_name")


    def import_submodels_from_dto(self, dim_dto: dtos.Dto) -> models.Model:

        groups_list = dim_dto.get_payload().get("groups")

        if isinstance(groups_list, list):
            for group_dict in groups_list:
                group_dto = dtos.Dto(group_dict)
                self.groups.append(\
                    grq_groups.Group(self, self.get_group_by_value_datatype_name())\
                        .import_dto(group_dto))

        return self
    

    def assemble_group_by_item(self, sql_builder) -> str:

        if len(self.groups) > 0:     

            when_clauses = []
            
            for group in self.groups:
                when_clauses.append(group.assemble_case_pair(self.get_varname(), sql_builder))         
            
            expr = sql_builder.case(*when_clauses)
        else:
            expr = sql_builder.sql_varname(self.get_varname())

        return expr
    

    def assemble_select_item(self, sql_builder) -> str:

        group_by_item = self.assemble_group_by_item(sql_builder)

        if len(self.groups) > 0:     
            gr_varname = sql_builder.sql_varname(self.get_varname()) + "_group"
            select_item = sql_builder.AS(group_by_item, gr_varname)
        else:
            select_item = sql_builder.sql_varname(self.get_varname())

        return select_item