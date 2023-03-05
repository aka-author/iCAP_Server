# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_select.py                     (\(\
# Func:     Building SELECT queries           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import utils, fields, db_objects, query_runners, sql_builders, sql_queries


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


class DistinctClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Clause):

        super().__init__(chief)

        self.clause_name = "DISTINCT"
    

class SelectClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Clause):

        super().__init__(chief)

        self.clause_name = "SELECT"

        self.set_headless_flag()

        self.field_defs = []


    def add_field(self, alias: str, expr: str, *operands) -> 'SelectClause':

        # add_field("k_burb", "100*{0}/{1}", ("weight", "t0"), ("count_pets", "t1"))

        self.field_defs.append({"alias": alias, "expr": expr, "operands": operands})

        return self


    def assemble_field_snippet(self, field_def: Dict) -> str:
        
        operand_snippets = \
            [self.sql.operand(operand_def) for operand_def in field_def["operands"]]

        expr_snippet = \
            field_def["expr"].format(*operand_snippets)

        return self.sql.as_subst(expr_snippet, field_def["alias"])


    def assemble_snippet(self) -> str:

        defs = [self.assemble_field_snippet(field_def) for field_def in self.field_defs]

        return self.sql.list(defs)
    

class FromClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Clause):

        super().__init__(chief)

        self.clause_name = "FROM"

        self.src_recordsets = []


    def add_src_recordset(self, 
                          join_mode: str, 
                          recordset_name: str, db_scheme_name: str,
                          alias: str) -> 'FromClause':

        src_info = {
            "join_mode":        join_mode,
            "recordset_name":   recordset_name,
            "db_scheme_name":   db_scheme_name,
            "alias":            alias
        }

        self.src_recordsets.append(src_info)

        return self
    

    def define_join_condition(self, join_expr: str, *operands) -> 'FromClause':

        last_idx = len(self.src_recordsets) - 1

        self.src_recordsets[last_idx]["join_expr"] = join_expr
        self.src_recordsets[last_idx]["operands"] = operands

        return self


    def assemble_src_recordset_snippet(self, src_info: Dict) -> str:

        snippet = ""

        if src_info["join_mode"] is not None:
            snippet += src_info["join_mode"] + " "

        snippet += \
            self.sql.qualified_table_name(src_info["recordset_name"], src_info["db_scheme_name"])
        
        snippet += " " + src_info["alias"]

        if src_info["join_mode"] is not None:
            snippet += " ON " 
            operands = [self.sql.operand(operand) for operand in src_info["operands"]]
            snippet += src_info["join_expr"].format(*operands)

        return snippet


    def assemble_snippet(self) -> str:

        sources = [self.assemble_src_recordset_snippet(sr) for sr in self.src_recordsets]

        return " ".join(sources)


class GroupByClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "GROUP BY"


    def assemble_snippet(self) -> str:

        snippet = ""

        return snippet


class OrderByClause(sql_queries.Clause):

    def __init__(self, chief: sql_queries.Query):

        super().__init__(chief)

        self.clause_name = "ORDER BY"


    def assemble_snippet(self) -> str:

        snippet = ""

        return snippet


class Select(sql_queries.SelectiveQuery):

    def __init__(self, chief, query_name: str=None):

        super().__init__(chief, "SELECT", query_name)    

        self.field_groups = []
        self.field_groups_by_aliases = {}
        self.table_alias_count = 0


    def create_clauses(self) -> 'sql_queries.Query':

        self.add_clause(DistinctClause(self))\
            .add_clause(SelectClause(self))\
            .add_clause(FromClause(self))\
            .add_clause(sql_queries.WhereClause(self))\
            .add_clause(GroupByClause(self))\
            .add_clause(OrderByClause(self))
        
        return self


    def DISTINCT(self) -> 'Select':

        self.clauses_by_names["DISTINCT"].turn_on()

        return self


    def SELECT_field(self, alias: str, expr: str, *operands) -> 'Select':

        self.clauses_by_names["SELECT"].add_field(alias, expr, *operands).turn_on()
        
        return self
    

    def count_src_recordsets(self) -> int:

        return len(self.clauses_by_names["FROM"].src_recordsets)


    def get_next_alias(self, alias: str) -> str:

        return utils.safeval(alias, "t" + str(self.count_src_recordsets()))
    

    def get_field_group_alias_by_index(self, group_index: int) -> str:

        return self.clauses_by_names["FROM"].src_recordsets[group_index]["alias"]


    def FROM(self, recordset: tuple, alias: str=None) -> 'Select':

        self.clauses_by_names["FROM"].add_src_recordset(\
            None,
            recordset[0], 
            recordset[1] if len(recordset) > 1 else None, 
            self.get_next_alias(alias)).turn_on()        
            
        return self
    

    def INNER_JOIN(self, recordset: tuple, alias: str=None) -> 'Select':

        self.clauses_by_names["FROM"].add_src_recordset(\
            "INNER JOIN",
            recordset[0], 
            recordset[1] if len(recordset) > 1 else None, 
            self.get_next_alias(alias)) 

        return self


    def LEFT_JOIN(self, recordset: tuple, alias: str=None) -> 'Select':
        
        self.clauses_by_names["FROM"].add_src_recordset(\
            "LEFT JOIN",
            recordset[0], 
            recordset[1] if len(recordset) > 1 else None, 
            self.get_next_alias(alias)) 

        return self
        

    def ON(self, join_expr, *operands) -> 'Select':
        
        self.clauses_by_names["FROM"].define_join_condition(join_expr, *operands)

        return self


    def WHERE(self, expression: str, *operands) -> 'Select':

        self.clauses_by_names["WHERE"].set_expression(expression).add_operands(*operands).turn_on()

        return self


    def GROUP_BY(self) -> 'Select':


        return self


    def ORDER_BY(self) -> 'Select':


        return self 
