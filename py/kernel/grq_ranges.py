# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  grq_ranges.py                               (\(\
# Func:    Defining constraints for source data        (^.^)
# # ## ### ##### ######## ############# #####################

import utils 
import datatypes
import fields
import dtos
import workers
import models


class Constraint(models.Model):

    def __init__(self, chief: workers.Worker, datatype_name: str=datatypes.DTN_STRING):

        self.datatype_name = datatype_name

        super().__init__(chief)


    def set_datatype_name(self, datatype_name: str) -> 'Constraint':

        self.datatype_name = datatype_name

        return self


    def get_datatype_name(self) -> str:

        return self.datatype_name
    

    def assemble_expression(self, varname: str, sql_builder) -> str:

        return varname
    

class NamedConstraint(Constraint):

    def __init__(self, chief: workers.Worker, datatype_name=datatypes.DTN_STRING):

        super().__init__(chief, datatype_name)

    
    def define_fields(self) -> models.Model:

        self.get_field_manager().add_field(fields.StringField("range_name"))

        return self 
    

    def get_range_name(self) -> str:
    
        return self.get_field_value("range_name")
    

    def get_constraints_expression(self) -> str:

        if self.get_range_name() == "any":
            expr = "true"
        else:
            expr = "false"

        return expr
    

class SetConstraint(Constraint):

    def __init__(self, chief: workers.Worker, datatype_name=datatypes.DTN_STRING):

        super().__init__(chief, datatype_name)

    
    def define_fields(self) -> models.Model:

        self.get_field_manager().add_field(fields.ListField("members"))

        return self 


    def get_members(self) -> list:

        return self.get_field_value("members")
    

    def assemble_expression(self, varname, sql_builder) -> str:

        members_str = ", ".join([sql_builder.typed_value(m) for m in self.get_members()])

        sql_varname = sql_builder.sql_varname(varname)

        return "({0} in {1})".format(sql_varname, utils.pars(members_str))


class SegmentConstraint(Constraint):

    def __init__(self, chief: workers.Worker, datatype_name=datatypes.DTN_STRING):

        super().__init__(chief, datatype_name)

    
    def define_fields(self) -> models.Model:

        datatype_name = self.get_datatype_name()

        self.get_field_manager()\
                .add_field(fields.new_native_field("min", datatype_name))\
                .add_field(fields.new_native_field("max", datatype_name))

        return self 
        

    def get_min(self) -> any:

        return self.get_field_value("min")
    

    def get_max(self) -> any:

        return self.get_field_value("max")


    def assemble_expression(self, varname: str, sql_builder) -> str:

        min_sql = sql_builder.typed_value(self.get_min())
        max_sql = sql_builder.typed_value(self.get_max())

        sql_varname = sql_builder.sql_varname(varname)

        return "({0} <= {1} AND {1} <= {2})".format(min_sql, sql_varname, max_sql)


class PatternConstraint(Constraint):

    def __init__(self, chief: workers.Worker, datatype_name=datatypes.DTN_STRING):

        super().__init__(chief, datatype_name)

    
    def define_fields(self) -> models.Model:

        self.get_field_manager()\
                .add_field(fields.StringField("expression_type"))\
                .add_field(fields.ListField("expressions"))

        return self 


    def get_expression_type(self) -> list:

        return self.get_field_value("expression_type")
    

    def get_expressions(self) -> list:

        return self.get_field_value("expressions")
    

    def assemble_expression(self, varname, sql_builder) -> str:

        expr_type = self.get_expression_type()
        expressions  = self.get_expressions()

        if expr_type == "strlistitem":
            expr_template = sql_builder.check_list_vs_string_list_field(expressions, 0)
            sql_varname = sql_builder.sql_varname(varname)
            expression = expr_template.format(sql_varname)
        else:
            expression = "true"

        return expression


class Range(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.constraints = None


    def define_fields(self) -> models.Model:

        self.get_field_manager() \
            .add_field(fields.StringField("datatype_name")) \
            .add_field(fields.StringField("range_type_name"))

        return self
    

    def get_datatype_name(self) -> str:

        return self.get_field_value("datatype_name") 


    def get_range_type_name(self) -> str:

        return self.get_field_value("range_type_name") 
    

    def import_submodels_from_dto(self, range_dto: dtos.Dto) -> models.Model:

        constraints_dict = range_dto.get_payload().get("constraints")

        if isinstance(constraints_dict, dict):

            datatype_name = self.get_datatype_name()
            range_type_name = self.get_range_type_name()

            if range_type_name == "named":
                self.constraints = NamedConstraint(self, datatype_name)
            elif range_type_name == "set":
                self.constraints = SetConstraint(self, datatype_name)
            elif range_type_name == "segment":
                self.constraints = SegmentConstraint(self, datatype_name)
            elif range_type_name == "pattern":
                self.constraints = PatternConstraint(self, datatype_name)
            else: 
                self.constraints = None

            if self.constraints is not None:
                self.constraints.import_dto(dtos.Dto(constraints_dict))
                
        return self
    

    def assemble_expression(self, varname: str, sql_builder) -> str:

        expr = (
            self.constraints.assemble_expression(varname, sql_builder) \
            if self.constraints is not None else "true"
        )

        return expr
