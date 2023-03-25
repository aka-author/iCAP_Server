

import dtos, workers, models, grq_scopes, grq_granularity


class ReportQuery(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.scope = None
        self.granularity = None


    def import_submodels_from_dto(self, rq_dto: dtos.Dto) -> models.Model:

        rq_dict = rq_dto.get_payload()
        scope_dict = rq_dict.get("scope")
        granularity_dict = rq_dict.get("granularity")

        if isinstance(scope_dict, dict):
            scope_dto = dtos.Dto(scope_dict)
            self.scope = grq_scopes.Scope(self).import_dto(scope_dto)

        if isinstance(granularity_dict, dict):
            granularity_dto = dtos.Dto(granularity_dict)
            self.granularity = grq_granularity.Granularity(self).import_dto(granularity_dto)

        return self
    

    def assemble_select_fields(self) -> str:

        return ""


    def assemble_where_expression(self) -> str:

        return ""
    

    def assemble_group_by_list(self) -> str:

        return ""
    

    
