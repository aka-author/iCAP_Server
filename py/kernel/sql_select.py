# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_select.py                     (\(\
# Func:     Building SELECT queries           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import fields, query_runners, sql_builders, sql_queries


class FieldGroup(fields.FieldKeeper):

    def __init__(self, field_group_name: str, field_group_alias: str=None):

        super().__init__(field_group_name)

        self.field_group_alias = field_group_alias


    def get_field_group_name(self) -> str:

        return self.get_recordset_name()


    def set_field_group_alias(self, field_group_alias: str) -> 'FieldGroup':

        self.field_group_alias = field_group_alias

        return self


    def get_field_group_alias(self) -> str:

        return self.field_group_alias


class ClauseSelect(sql_queries.Clause):

    def __init__(self, chief, clause_name: str=""):

        super().__init__(chief)

        self.clause_name = "SELECT"
        self.useful_flag = False


    def add_field(self, field_info: Dict) -> 'ClauseSelect':

        if "varname" in field_info:
            field_group_alias = self.get_chief().get_field_group_alias(field_info)
            varname = field_info["varname"]
            field_ref_snippet = self.sql.qualified_varname(varname, field_group_alias)
        elif "value" in field_info: 
            field_ref_snippet = self.sql.get_typed_value(field_info["value"])

        self.extend_snippet(field_ref_snippet, ", ")

        return self


    def all_fields(self) -> List:

        for field_group in self.get_chief().field_groups:
            field_group_alias = field_group.get_field_group_alias()
            for varname in field_group.get_varnames():
                qualified_varname = self.sql_builder.qualified_varname(varname, field_group_alias)
                field_refs.append(qualified_varname)


    def set_snippet(self) -> 'ClauseSelect':

        # field_info:
        #   {"field_group_name": "pets", "varname": "pet_name"}
        #   {"field_group_index": 0,     "varname": "pet_name"}
        #   {"field_group_alias": "t0",  "varname": "pet_name"}

        field_refs = []

        if len(field_infos) == 1 and field_infos[0].get("varname") == "*":
            
        else:
            for field_info in field_infos:
                

                field_refs.append(field_ref_snippet)

        self.clause_select.set_snippet(self.sql_builder.list(field_refs))


    def get_snippet(self) -> str:

        return self.snippet
    

class ClauseFrom(sql_queries.Clause):

    def get_snippet(self) -> str:

        return self.snippet


class ClauseWhere(sql_queries.Clause):

    def get_snippet(self) -> str:

        return self.snippet


class Select(sql_queries.SelectiveQuery):

    def __init__(self, chief: query_runners.QueryRunner, query_name: str=None):

        super().__init__(chief, "SELECT", query_name)    

        self.field_groups = []
        self.field_groups_by_aliases = {}
        self.table_alias_count = 0


    def create_clauses(self) -> 'sql_queries.Query':

        self.add_clause("DISTINCT")\
            .add_clause("SELECT")\
            .add_clause("FROM")\
            .add_clause("WHERE")\
            .add_clause("GROUP BY")\
            .add_clause("ORDER BY")
        
        return self


    def count_field_groups(self) -> int:

            return len(self.field_groups)


    def get_field_group_alias_by_recordset_name(self, recordset_name: str) -> str:

        for group in self.field_groups:
            if group.get_recordset_name() == recordset_name:
                alias = group.get_field_group_alias()
                break

        return alias


    def get_field_group_alias_by_index(self, group_index: int) -> str:

        return self.field_groups[group_index].get_field_group_alias()


    def get_group_alias_by_field_info(self, field_info: Dict) -> str:

        # Field info:
        #    {"recordset_name": "rabbits", ...blah-blah-blah, whatever}
        #    recordset_name|group_index|alias

        if "recordset_name" in field_info:
            alias = self.get_field_group_alias_by_recordset_name(field_info.get("recordset_name"))
        elif "field_group_index" in field_info:
            alias = self.get_field_group_alias_by_index(field_info.get("group_index"))
        elif "field_group_alias" in field_info:
            alias = field_info.get("field_group_alias")
        else:
            alias = self.get_group_alias_by_group_index(0)

        return alias
    

    def add_fields(self, fk: fields.FieldKeeper, field_group_name: str=None) -> 'Query':

        for varname in fk.get_varnames():
            if not self.fk.has_field(varname):
                self.add_field(fk.get_field(varname), field_group_name)

        return self


    def SELECT(self, *field_infos) -> 'Select':

        
        
        return self
    

    def FROM(self, *field_group_infos) -> 'Select':

        # field_group_info:
        #   {"join": "left", "field_group_name": "pets", }
        #   {"field_group_index": 0,     ...whatever }
        #   {"field_group_alias": "t0",  ...whatever }


        # for field_group_info in field_group_infos:


            
        return self


    def WHERE(self, expr: str, *references) -> 'Select':


        return self


    def GROUP_BY(self) -> 'Select':


        return self


    def ORDER_BY(self) -> 'Select':


        return self 


    def import_ramtable_row(self, rt_row):

        self.COLUMNS.sql.add_ramtable_values(rt_row)

        return self
    

    


    def assemble_new_field_froup_alias(self) -> str:

        return "t" + str(self.count_field_groups())


    def new_field_group(self, field_keeper: fields.FieldKeeper, field_group_alias: str=None) -> 'FieldGroup':

        alias = utils.safeval(field_group_alias, self.assemble_new_field_group_alias())

        return FieldGroup(field_keeper, alias)


    def add_field_group(self, field_group: FieldGroup) -> 'Recordset':

        self.field_groups.append(field_group)
        self.field_groups_by_aliases[field_group.get_field_group_alias()] = field_group

        return self


    def add_field_group_from_scratch(self, field_group_name: str, alias: str=None) -> 'Recordset':

        empty_field_keeper = fields.FieldKeeper(field_group_name)
        
        return self.add_field_group(self.new_field_group(empty_field_keeper, alias)) 


    def add_field_group_from_field_keeper(self, field_keeper, field_group_alias: str=None) -> 'Recordset':

        return self.add_field_group(self.new_field_group(field_keeper, field_group_alias))


    def add_field_group_from_table(self, table: db_objects.Table, field_group_alias: str=None) -> 'Recordset':

        table_field_group = self.new_field_group(table.get_field_keeper(), field_group_alias)

        table_field_group.set_scheme_name(table.get_scheme_name())

        return self.add_field_group(table_field_group)


    def has_field_group(self, field_group_name: str) -> bool:

        return field_group_name in self.field_groups_by_names


    def get_field_group(self, field_group_name: str) -> FieldGroup:

        return self.field_groups.get(field_group_name)


    def get_field_group_by_alias(self, alias: str) -> FieldGroup:

        return self.field_groups_by_aliases.get(alias)


    def get_field_group_index(self, field_group_name: str) -> int:

        return self.field_groups_enum.get(field_group_name)
        

    def adapt_field(self, field: fields.Field, field_group_name: str=None) -> fields.Field:

        return field


    def check_field_group(self, field_group_name) -> 'Recordset':

        if self.has_field_group(field_group_name):
            self.add_field_group(field_group_name)

        return self


    def enroll_field_to_group(self, field: fields.Field, field_group_name: str) -> 'Recordset':

        actual_group_name = utils.safeval(field_group_name, "default")

        self.check_field_group(actual_group_name)

        self.get_field_group(actual_group_name).add_field(field)

        return self


    def add_field(self, field: fields.Field, field_group_name: str=None) -> 'Recordset':

        adapted_field = self.adapt_field(field, field_group_name)

        self.fk.add_field(adapted_field)
        self.enroll_field_to_group(adapted_field, field_group_name)

        return self


    def add_from_field_keeper(self, fk: fields.FieldKeeper, field_group_name: str=None) -> 'Recordset':

        actual_field_group_name = utils.safeval(field_group_name, fk.get_recordset_name())

        if self.has_field_group(actual_field_group_name):
            actual_field_group_name = utils.unique_name("g")

        for field_name in fk.get_field_names():
            self.add_field(fk.get_field(field_name), actual_field_group_name)

        return self


    def get_field_full_name(self, field_name: str, field_group_name: str) -> str:

        return self.sql.qualified_field_name(field_name, self.get_alias(field_group_name))