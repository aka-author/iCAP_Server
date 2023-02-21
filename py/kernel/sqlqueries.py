# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sqlqueries.py                  (\(\
# Func:    Accessing SQL queries          (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import uuid
import utils, fields, ramtables, bureaucrat, dbms, sqlsnippets


class Subqueries(bureaucrat.Bureaucrat):

    def __init__(self, chief: 'Query'):

        super().__init__(chief)

        self.subqueries = {}


    def count(self) -> int:

        return len(self.subqueries)


    def add(self, query: 'Query') -> object:

        self.subqueries[query.get_query_name()] = query.set_chief(self)
        query.set_subquery_flag()
        self.get_chief().adopt_subquery(query)

        return self


    def get_subquery(self, subquery_name: str) -> 'Query':

        return self.subqueries[subquery_name]


    def get_subquery_names(self) -> List:

        return [self.subqueries[sq_name].get_query_name() for sq_name in self.subqueries]


    def get_snippet(self) -> str:

        if len(self.subqueries) > 0:
            defs = ",\n".join([self.get_def_snippet(self.subqueries[sq_name]) \
                               for sq_name in self.subqueries])
            return "WITH\n" + defs + "\n"
        else:
            return ""


    def get_subquery_definition_snippet(self, query: 'Query') -> str:

        return utils.separate(query.get_query_name(), " AS ", utils.pars(query.get_snippet()))


    def is_subquery(self) -> bool:

        return False


    def is_main_query(self) -> bool:

        return False


class FieldGroup(fields.FieldKeeper):

    def __init__(self, field_group_name: str):

        super().__init__(field_group_name)


class TableObject(bureaucrat.Bureaucrat):

    def __init__(self, chief: dbms.DbLayer, recordset_name: str):

        super().__init__(chief)

        self.recordset_name = recordset_name

        self.main_field_group = FieldGroup(self, "main")


    def get_recordset_name(self) -> str:

        return self.recordset_name


class Table(TableObject):

    def __init__(self, chief: dbms.DbLayer, table_name: str):

        super().__init__(chief, table_name)


class Query(TableObject):

    def __init__(self, chief: dbms.DbLayer, operator_name: str, query_name: str=None):

        super().__init__(chief, utils.safeval(query_name, self.assemble_unique_query_name()))

        self.operator_name = operator_name

        self.field_groups = []
        self.field_groups_by_names = {}
        
        self.subqueries = self.new_subqueries().set_chief(self)
        self.subquery_flag = False

        self.clauses = []

        self.explicit_template = None

        self.selective_flag = False

        self.table_alias_count = 0


    def get_operator_name(self) -> str:

        return self.operator_name


    def assemble_unique_query_name(self) -> str:

        return "q" + str(uuid.uuid4()).replace("-", "")


    def set_field_keeper(self, fk: fields.FieldKeeper) -> object:

        self.fk = fk

        return self


    def add_field_group(self, field_group_name: str) -> object:

        fg = FieldGroup(field_group_name)
        self.field_groups.append(fg)
        self.field_groups_by_names[field_group_name] = fg

        return self


    def get_field_group(self, field_group_name: str) -> FieldGroup:

        return self.field_groups[field_group_name]


    def add_field(self, field: fields.Field, field_group_name=None) -> object:

        self.fm.add_field(field)

        if field_group_name is not None:
            self.get_field_group(field_group_name).add_field(field)

        return self


    def new_subqueries(self) -> Subqueries:

        return Subqueries(self)


    def has_subqueries(self) -> bool:

        return self.subqueries.count() > 0


    def adopt_subquery(self, query: object) -> object:

        return self


    def set_subquery_flag(self, is_subquery: bool=True) -> object:

        self.subquery_flag = is_subquery

        return self


    def is_subquery(self) -> bool:

        return self.subquery_flag


    def is_main_query(self) -> bool:

        return not self.is_subquery()


    def set_explicit_template(self, template: str) -> object:

        self.explicit_template = template

        return self


    def has_explicit_template(self) -> bool:

        return self.explicit_template is not None


    def is_selective(self) -> bool:

        return self.selective_flag;


    def get_unique_table_alias(self) -> str:

        if self.is_main_query():
            self.table_alias_count += 1
            return "t" + str(self.table_alias_count)
        else:
            return self.get_chief().get_unique_table_alias(self)


    def get_clauses_snippet(self) -> str:

        return "\n".join([cl.sql.get_snippet() for cl in self.clauses if cl.is_useful()])


    def get_snippet(self, substitutes: List=None) -> str:

        snippet = ""

        if self.has_explicit_template():
            snippet = self.get_explicit_template().format(*substitutes)
        else:
            snippet = self.subqueries.get_snippet() \
                      + self.get_operator_name() + " " \
                      + self.get_clauses_snippet()

        return snippet
     

class SelectiveQuery(Query):

    def __init__(self, chief: dbms.DbLayer, operator_name: str, query_name: str=None):

        super().__init__(chief, operator_name, query_name)

        self.selective_flag = True


class Select(SelectiveQuery):

    def __init__(self, chief: dbms.DbLayer, query_name: str=None):

        super().__init__(chief, "SELECT", query_name)

        self.DISTINCT = sqlsnippets.Clause(self, "DISTINCT")
        self.COLUMNS = sqlsnippets.Clause(self)
        self.FROM = sqlsnippets.Clause(self, "FROM")
        self.WHERE = sqlsnippets.Clause(self, "WHERE")
        self.GROUP_BY = sqlsnippets.Clause(self, "GROUP BY")
        self.ORDER_BY = sqlsnippets.Clause(self, "ORDER BY")

        self.clauses = [self.DISTINCT, self.COLUMNS, self.FROM, self.WHERE, self.GROUP_BY, self.ORDER_BY]


    def import_ramtable_row(self, rt_row):

        self.COLUMNS.sql.add_ramtable_values(rt_row)

        return self


class Union(SelectiveQuery):

    def __init__(self, chief: dbms.DbLayer, query_name: str=None):

        super().__init__(chief, "UNION", query_name)


    def import_source_ramtable(self, src_rt):

        for idx in range(0, src_rt.count_rows()):
            self.subqueries.add(Select(self).import_ramtable_row(src_rt.select_by_index(idx)))

        return self


    def get_snippet(self) -> str:

        snippet = "\nUNION\n".join([utils.pars(self.subqueries.get_subquery(sq_name).get_snippet()) \
                                    for sq_name in self.subqueries.get_subquery_names()])

        return snippet


class Insert(Query):

    def __init__(self, chief: dbms.DbLayer, query_name: str=None):

        super().__init__(chief, "INSERT", query_name)

        self.INTO = sqlsnippets.Clause(self, "INTO")
        self.VALUES = sqlsnippets.Clause(self, "VALUES")
        self.SELECT = sqlsnippets.Clause(self, "SELECT")
        self.FROM = sqlsnippets.Clause(self, "FROM")
        self.WHERE = sqlsnippets.Clause(self, "WHERE")

        self.clauses = [self.INTO, self.VALUES, self.SELECT, self.FROM, self.WHERE]


    def set_field_values(self, fm, table_name=None):

        varnames = fm.get_varnames()
        actual_table_name = utils.safeval(table_name, fm.get_recordset_name())

        column_list = ", ".join([varname for varname in varnames])
        self.INTO.sql.set(self.qualify_table_name(actual_table_name)).add(utils.pars(column_list))

        dbms = self.get_app().get_dbms()
        value_list = ", ".join([fm.sql_typed_value(varname, dbms) for varname in varnames]) 
        self.VALUES.sql.set(utils.pars(value_list))

        return self


    def import_source_ramtable(self, src_rt):

        u = Union(self)
        for idx in range(0, src_rt.count_rows()):
            u.subqueries.add(Select(u).import_ramtable_row(src_rt.select_by_index(idx)))

        self.subqueries.add(u)

        self.INTO.sql.set(src_rt.get_table_name())
        self.SELECT.sql.set("*")
        self.FROM.sql.set(u.get_query_name())

        return self


class Update(Query):

    def __init__(self, chief: dbms.DbLayer, query_name: str=None):

        super().__init__(chief, "UPDATE", query_name)

        self.TABLE = sqlsnippets.Clause(self, "")
        self.SET = sqlsnippets.Clause(self, "SET")
        self.WHERE = sqlsnippets.Clause(self, "WHERE")

        self.clauses = [self.TABLE, self.SET, self.WHERE]


    def import_source_field_manager(self, table_name, fm):

        varnames = fm.get_varnames()

        dbms = self.get_dbms()

        self.TABLE.sql.set(self.qualify_table_name(table_name)).q\
            .SET.sql.setlist(dbms, [fm.sql_equal(dbms, varname) for varname in varnames])

        return self