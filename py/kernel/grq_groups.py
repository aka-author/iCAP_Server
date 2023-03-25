

import datatypes, fields, dtos, workers, models, grq_ranges


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
    

    def import_submodels_from_dto(self, group_dto: dtos.Dto) -> models.Model:

        range_dict = group_dto.get_payload().get("range")
        
        if isinstance(range_dict, dict):
            self.range = grq_ranges.Range(self).import_dto(dtos.Dto(range_dict))

        return self
    

    def assemble_expression(self, sql_builder) -> str:

        return self.range.assemble_expression(self.get_varname(), sql_builder)