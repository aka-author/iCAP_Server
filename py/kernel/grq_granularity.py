# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  grq_granularity.py                           (\(\
# Func:    Grouping source data for a generic report    (^.^)
# # ## ### ##### ######## ############# #####################

import sql_builders 
import dtos
import workers 
import models 
import grq_dimensions


class Granularity(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.dimensions = []


    def import_submodels_from_dto(self, gran_dto: dtos.Dto) -> models.Model:

        dimension_list = gran_dto.get_payload().get("dimensions")

        if isinstance(dimension_list, list):
            for dimension_dict in dimension_list:
                dim_dto = dtos.Dto(dimension_dict)
                self.dimensions.append(grq_dimensions.Dimension(self).import_dto(dim_dto))

        return self
    

    def get_dimensions(self) -> list:

        return self.dimensions


    def assemble_group_by_list(self, sql_builder: sql_builders.SqlBuilder) -> str:

        group_by_items = []

        for dimension in self.dimensions:
           group_by_items.append(dimension.assemble_group_by_item(sql_builder))

        return sql_builder.list(group_by_items)
    

    def assemble_select_fields(self, sql_builder: sql_builders.SqlBuilder) -> str:

        select_fields = []

        for dimension in self.dimensions:
           select_fields.append(dimension.assemble_select_item(sql_builder))

        return sql_builder.list(select_fields) 
