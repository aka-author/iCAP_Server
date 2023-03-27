# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  grq_scopes.py                               (\(\
# Func:    Converting scopes to boolean expressions    (^.^)
# # ## ### ##### ######## ############# #####################

import fields, dtos, workers, models, grq_conditions


class Scope(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.conditions = []
        self.conditions_by_names = {}


    def define_fields(self) -> models.Model:

        self.get_field_manager()\
                .add_field(fields.StringField("expression"))

        return self
    

    def add_condition(self, condition) -> 'Scope':

        self.conditions.append(condition)
        self.conditions_by_names[condition.get_condition_name()] = condition

        return self


    def import_submodels_from_dto(self, scope_dto: dtos.Dto) -> models.Model:
        
        conditions_list = scope_dto.get_payload().get("conditions")
        
        if isinstance(conditions_list, list):
            for condition_dict in conditions_list:
                cond_dto = dtos.Dto(condition_dict)
                self.add_condition(grq_conditions.Condition(self).import_dto(cond_dto))
        
        return self
    

    def get_expression(self) -> str:

        return self.get_field_value("expression")
    

    def count_conditions(self) -> int:

        return len(self.conditions)
    

    def get_condition_by_index(self, index: int) -> grq_conditions.Condition:

        return self.conditions[index]
    

    def assemble_where_expression(self, sql_builder) -> str:

        condition_expressions = []

        for condition in self.conditions:
            condition_expressions.append(condition.assemble_expression(sql_builder))

        return " AND ".join(condition_expressions)