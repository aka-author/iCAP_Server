# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  buildsql.py                          (\(\
# Func:    Assembling SQL queries               (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
import utils, bureaucrat


class Sql(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.snippet = ""


    def set_snippet(self, snippet):

        self.snippet = snippet 

        return self


    def get_snippet(self):

        return self.snippet


    def set(self, snippet=""):

        return self.set_snippet(snippet)


    def add(self, snippet, separ=" "):

        return self.set_snippet(utils.separate(self.snippet, separ, snippet))


    def add_list_items(self, snippets, separ=" "):

        return self.set_snippet(utils.separate(self.snippet, separ, ", ".join(snippets)))

    
    def assembe_field_snippet(self, field):

        if field.has_sql_agg_expr():
            return utils.separate(field.get_sql_agg_expr(), " AS ", field.get_varname())
        else:
            return field.get_varname()


    def add_ramtable_fields(self, rt):

        self.add_list_items([self.assembe_field_snippet(rt.get_field(field_name)) \
                                  for field_name in rt.get_field_names()])

        return self


    def assemble_datatype_qualifier(self, nature):

        datatype_qualifiers = {
            "string":    "::varchar",
            "numeric":   "::numeric",
            "boolean":   "::boolean",
            "uuid":      "::uuid",
            "timestamp": "::timestamp"
        }

        return datatype_qualifiers[nature]


    def assemble_pure_value_snippet(self, row, field_name):

        field = row.get_table().get_field(field_name)
        nature = field.get_nature()
        dtq = self.assemble_datatype_qualifier(nature)
        field_value = row.get_field_value(field_name)

        if field_value is not None:
            if nature == "string":
                value_snippet = utils.apos(utils.escsql(field_value))
            elif nature == "numeric" or nature == "boolean":
                value_snippet = field.serialize(field_value)
            elif nature == "uuid":
                value_snippet = utils.apos(field.serialize(field_value)) + dtq
            elif nature == "timestamp":
                value_snippet = utils.apos(field.serialize(field_value)) + dtq
            else:
                value_snippet = utils.apos(field_value)
        else:
            value_snippet = "null" + dtq

        return value_snippet


    def assemble_value_snippet(self, row, field_name):

        field = row.get_table().get_field(field_name)

        return utils.separate(self.assemble_pure_value_snippet(row, field_name), " AS ", field.get_varname())


    def add_ramtable_values(self, row):

        table = row.get_table()
        field_names = table.get_field_names()

        self.add_list_items(\
            [self.assemble_value_snippet(row, field_name) \
                for field_name in field_names if table.is_insertable(field_name)])

        return self


class ClauseSql(Sql):

    def set_snippet(self, snippet):

        self.get_chief().turn_on()

        return super().set_snippet(snippet)


    def get_snippet(self):

        return utils.separate(self.get_chief().get_clause_name(), " ", super().get_snippet())


    @property
    def q(self):

        return self.get_chief().get_chief()


class Clause(bureaucrat.Bureaucrat):

    def __init__(self, chief, clause_name=""):

        super().__init__(chief)

        self.clause_name = clause_name
        self.useful_flag = False
        self.sql = ClauseSql(self)


    def get_clause_name(self):

        return self.clause_name


    def turn_on(self): 

        self.useful_flag = True

        return self


    def is_useful(self):

        return self.useful_flag    


class Subqueries(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.subqueries = {}


    def count(self):

        return len(self.subqueries)


    def add(self, query):

        self.subqueries[query.get_query_name()] = query.set_chief(self)
        query.set_subquery_flag()
        self.get_chief().adopt_subquery(query)

        return self


    def get_subquery(self, subquery_name):

        return self.subqueries[subquery_name]


    def get_subquery_names(self):

        return [self.subqueries[sq_name].get_query_name() for sq_name in self.subqueries]


    def get_def_snippet(self, query):

        return utils.separate(query.get_query_name(), " AS ", utils.pars(query.get_snippet()))


    def get_snippet(self):

        if len(self.subqueries) > 0:
            defs = ",\n".join([self.get_def_snippet(self.subqueries[sq_name]) \
                               for sq_name in self.subqueries])
            return "WITH\n" + defs + "\n"
        else:
            return ""


class Query(bureaucrat.Bureaucrat):

    def __init__(self, chief, operator_name, query_name=None, schema_name=None):

        super().__init__(chief)
        
        self.schema_name = schema_name
        self.operator_name = operator_name
        self.query_name = utils.safeval(query_name, self.assemble_auto_query_name())
        self.subqueries = self.new_subqueries().set_chief(self)
        self.clauses = []
        self.explicit_template = None

        self.subquery_flag = False
        self.selective_flag = False


    def is_query(self):

        return True


    def assemble_auto_query_name(self):

        return "q" + str(uuid.uuid4()).replace("-", "")


    def get_operator_name(self):

        return self.operator_name


    def get_query_name(self):

        return self.query_name


    def get_schema_name(self):

        return self.schema_name


    def qualify_table_name(self, table_name):

        return table_name if "." in utils.safestr(table_name) \
                          else utils.consep(self.get_schema_name(), ".", table_name)


    def get_full_table_name(self, table_name):

        sn = self.get_schema_name()

        return (sn + "." if sn is not None else "") + table_name


    def is_selective(self):

        return self.selective_flag;


    def set_explicit_template(self, template):

        self.explicit_template = template

        return self


    def has_explicit_template(self):

        return self.explicit_template is not None


    def new_subqueries(self):

        return Subqueries(self)


    def has_subqueries(self):

        return self.subqueries.count() > 0


    def adopt_subquery(self, query):

        return self


    def set_subquery_flag(self, is_subquery=True):

        self.subquery_flag = is_subquery


    def is_subquery(self):

        return self.subquery_flag


    def get_clauses_snippet(self):

        return "\n".join([cl.sql.get_snippet() for cl in self.clauses if cl.is_useful()])


    def get_snippet(self, substitutes=None):

        snippet = ""

        if self.has_explicit_template():
            snippet = self.get_explicit_template().format(*substitutes)
        else:
            snippet = self.subqueries.get_snippet() \
                      + self.get_operator_name() + " " \
                      + self.get_clauses_snippet()

        return snippet
         

class SelectiveQuery(Query):

    def __init__(self, chief, operator_name, query_name=None, scheme_name=None):

        super().__init__(chief, operator_name, query_name, scheme_name)

        self.selective_flag = True
        self.out_rt = None


    def set_output_ramtable(self, out_rt):

        self.out_rt = out_rt

        return self


    def has_output_ramtable(self):

        return self.out_rt is not None


    def get_output_ramtable(self):

        return self.out_rt


    def fill_output_ramtable(self, query_result):
        
        out_rt = self.get_output_ramtable()
        field_names = out_rt.get_field_names()
        buffer = {}

        for row in query_result:

            for field_idx in range(0, out_rt.count_fields()):
                buffer[field_names[field_idx]] = row[field_idx]

            out_rt.insert(buffer)

        return self
        

class Select(SelectiveQuery):

    def __init__(self, chief, query_name=None, scheme_name=None):

        super().__init__(chief, "SELECT", query_name, scheme_name)

        self.DISTINCT = Clause(self, "DISTINCT")
        self.COLUMNS = Clause(self)
        self.FROM = Clause(self, "FROM")
        self.WHERE = Clause(self, "WHERE")
        self.GROUP_BY = Clause(self, "GROUP BY")
        self.ORDER_BY = Clause(self, "ORDER BY")

        self.clauses = [self.DISTINCT, self.COLUMNS, self.FROM, self.WHERE, self.GROUP_BY, self.ORDER_BY]

    
    def set_output_ramtable(self, out_rt):
        
        super().set_output_ramtable(out_rt)

        self.COLUMNS.sql.add_ramtable_fields(out_rt)

        if out_rt.get_table_name() is not None:
            self.FROM.sql.set(self.qualify_table_name(out_rt.get_table_name()))

        return self 


    def import_ramtable_row(self, rt_row):

        self.COLUMNS.sql.add_ramtable_values(rt_row)

        return self


class Union(SelectiveQuery):

    def __init__(self, chief, query_name=None, scheme_name=None):

        super().__init__(chief, "UNION", query_name, scheme_name)


    def import_source_ramtable(self, src_rt):

        for idx in range(0, src_rt.count_rows()):
            self.subqueries.add(Select(self).import_ramtable_row(src_rt.select_by_index(idx)))

        return self


    def get_snippet(self):

        snippet = "\nUNION\n".join([utils.pars(self.subqueries.get_subquery(sq_name).get_snippet()) \
                                    for sq_name in self.subqueries.get_subquery_names()])

        return snippet


class Insert(Query):

    def __init__(self, chief, query_name=None, scheme_name=None):

        super().__init__(chief, "INSERT", query_name, scheme_name)

        self.INTO = Clause(self, "INTO")
        self.VALUES = Clause(self, "VALUES")
        self.SELECT = Clause(self, "SELECT")
        self.FROM = Clause(self, "FROM")
        self.WHERE = Clause(self, "WHERE")

        self.clauses = [self.INTO, self.VALUES, self.SELECT, self.FROM, self.WHERE]


    def import_source_ramtable_row(self, row):

        t = row.get_table()
        field_names = t.get_field_names()

        column_list = utils.pars(", ".join([fn for fn in field_names]))
        self.INTO.sql.set(self.qualify_table_name(t.get_table_name())).add(column_list)

        value_list = utils.pars(", ".join([self.VALUES.sql.assemble_pure_value_snippet(row, fn) for fn in field_names]))
        self.VALUES.sql.set(value_list)

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


class Script(bureaucrat.Bureaucrat):

    def __init__(self, chief, script_name="noname", scheme_name=None):

        super().__init__(chief)

        self.script_name = script_name
        self.scheme_name = scheme_name
        self.queries = []
        self.selective_query = None
    

    def is_query(self):

        return False


    def get_script_name(self):

        return self.script_name


    def get_scheme_name(self):

        return self.scheme_name


    def is_selective(self):

        return self.selective_query is not None


    def add_query(self, query):

        self.queries.append(query)

        if query.is_selective():
            self.selective_query = query

        return self


    def count_queries(self):

        return len(self.queries)


    def import_source_ramtable(self, src_rt):

        if src_rt is not None: 
            for idx in range(0, src_rt.count_rows()):
                self.add_query(Insert(self, None, \
                    self.get_scheme_name()).import_source_ramtable_row(src_rt.select_by_index(idx)))

        return self 


    def get_selective_query(self):

        return self.selective_query


    def get_snippet(self):

        return ";\n".join([q.get_snippet() for q in self.queries]) + (";" if self.count_queries() > 0 else "")