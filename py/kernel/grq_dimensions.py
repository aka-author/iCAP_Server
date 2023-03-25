

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