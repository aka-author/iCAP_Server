# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  grq_ranges.py                               (\(\
# Func:    Defining a group for grouping source data   (^.^)
# # ## ### ##### ######## ############# #####################

import sql_builders, datatypes, fields, dtos, workers, models, grq_ranges


class Group(models.Model):

    def __init__(self, chief: workers.Worker, datatype_name: str=datatypes.DTN_STRING):

        self.datatype_name = datatype_name

        super().__init__(chief)
     
        self.range = None


    def get_datatype_name(self) -> str:

        return self.datatype_name
    

    def define_fields(self) -> models.Model:

        self.get_field_manager()\
                .add_field(fields.new_native_field("group_by_value", self.get_datatype_name()))

        return self
    

    def get_group_by_value(self) -> any:

        return self.get_field_value("group_by_value")
    

    def import_submodels_from_dto(self, group_dto: dtos.Dto) -> models.Model:

        range_dict = group_dto.get_payload().get("range")
        
        if isinstance(range_dict, dict):
            self.range = grq_ranges.Range(self).import_dto(dtos.Dto(range_dict))

        return self
    

    def assemble_case_pair(self, varname, sql_builder: sql_builders.SqlBuilder) -> str:

        if self.range is not None:
            range_conditions_expr = self.range.assemble_expression(varname, sql_builder)
            group_by_typed_value = sql_builder.typed_value(self.get_group_by_value())
        else:
            range_conditions_expr = None
            group_by_typed_value = None

        return (range_conditions_expr, group_by_typed_value)