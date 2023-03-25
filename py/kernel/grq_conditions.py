

import fields, dtos, workers, models, grq_ranges


class Condition(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.range = None


    def define_fields(self) -> models.Model:

        self.get_field_manager()\
                .add_field(fields.StringField("cond_name"))\
                .add_field(fields.StringField("varname"))

        return self
    

    def import_submodels_from_dto(self, dto: dtos.Dto) -> models.Model:

        range_dict = dto.get_prop_value("range")
        
        if isinstance(range_dict, dict):
            self.range = grq_ranges.Range(self).import_dto(dtos.Dto(range_dict))

        return self
    

    def get_cond_name(self) -> str:

        return self.get_field_value("cond_name")
    

    def get_varname(self) -> str:

        return self.get_field_value("varname")
    

    def get_range(self) -> grq_ranges.Range:

        return self.range
    

    def assemble_expression(self, sql_builder) -> str:

        return self.range.assemble_expression(self.get_varname(), sql_builder)