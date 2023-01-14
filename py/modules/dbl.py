# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  dbl.py                                   (\(\
# Func:    Assembling and running SQL queries       (^.^)
# # ## ### ##### ######## ############# ##################### 

import psycopg2
import status, utils, bureaucrat


class Sql(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.snippet = ""


    def set_snippet(self, snippet):

        self.snippet = snippet 

        return self


    def get_snippet(self):

        return self.snippet


    def separate(self, s1, separ, s2):

        return s1 + s2 if s1 == "" or s2 == "" or s1.endswith(separ) or s2.startswith(separ) else s1 + separ + s2


    def join(self, snippet, separ=" "):

        self.snippet = self.separate(self.snippet, separ, snippet)
 
        self.get_chief().turn_on()

        return self


    def join_list_items(self, snippets, separ=" "):

        self.snippet = self.separate(self.snippet, separ, ", ".join(snippets))

        self.get_chief().turn_on()

        return self

    
    def assembe_field_snippet(self, field):

        if field.has_sql_agg_expr():
            return field.get_sql_agg_expr() + " AS " + field.get_varname()
        else:
            return field.get_varname()


    def take_ramtable_fields(self, rt):

        self.join_list_items([self.assembe_field_snippet(rt.get_field(field_name)) \
                                  for field_name in rt.get_field_names()])

        return self


    def assemble_value_snippet(self, row, field_name):

        field = row.get_table().get_field(field_name)
        nature = field.get_nature()
        field_value = row.get_field_value(field_name)

        if nature == "string":
            value_snippet = utils.apos(field_value)
        elif nature == "numeric" or nature == "boolean":
            value_snippet = field.serialize(field_value)
        elif nature == "uuid":
            value_snippet = utils.apos(field.serialize(field_value)) + "::uuid"
        elif nature == "timestamp":
            value_snippet = utils.apos(field.serialize(field_value)) + "::timestamp"
        else:
            value_snippet = utils.apos(field_value)

        return value_snippet + " AS " + field.get_varname()


    def take_ramtable_values(self, row):

        field_names = row.get_table().get_field_names()

        self.join_list_items(\
            [self.assemble_value_snippet(row, field_name) for field_name in field_names])

        return self


class Clause(bureaucrat.Bureaucrat):

    def __init__(self, chief, clause_name=""):

        super().__init__(chief)

        self.clause_name = clause_name
        self.useful = False
        self.sql = Sql(self).set_snippet(self.get_clause_name())


    def get_clause_name(self):

        return self.clause_name


    def turn_on(self): 

        self.useful = True

        return self


    def is_useful(self):

        return self.useful    


class Subqueries(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.subqueries = {}


    def count(self):

        return len(self.subqueries)


    def add(self, query):

        self.subqueries[query.get_query_name()] = query.set_chief(self)
        query.set_subquery_flag()

        return self


    def get_subquery(self, subquery_name):

        return self.subqueries[subquery_name]


    def get_subquery_names(self):

        return [self.subqueries[sq_name].get_query_name() for sq_name in self.subqueries]


    def get_def_snippet(self, query):

        return query.get_query_name() + " AS " + utils.pars(query.get_snippet())


    def get_snippet(self):

        if len(self.subqueries) > 0:
            defs = ",\n".join([self.get_def_snippet(self.subqueries[sq_name]) for sq_name in self.subqueries])
            return "WITH\n" + defs + "\n"
        else:
            return ""


class Query(bureaucrat.Bureaucrat):

    def __init__(self, chief, operator_name, query_name, schema_name=None):

        super().__init__(chief)
        
        self.schema_name = schema_name
        self.operator_name = operator_name
        self.query_name = query_name
        self.subqueries = self.new_subqueries().set_chief(self)
        self.clauses = []
        self.explicit_template = None

        self.subquery_flag = False


    def get_operator_name(self):

        return self.operator_name


    def get_query_name(self):

        return self.query_name


    def get_schema_name(self):

        return self.schema_name


    def get_full_table_name(self, table_name):

        sn = self.get_schema_name()

        return (sn + "." if sn is not None else "") + table_name


    def set_explicit_template(self, template):

        self.explicit_template = template

        return self


    def has_explicit_template(self):

        return self.explicit_template is not None


    def new_subqueries(self):

        return Subqueries(self)


    def has_subqueries(self):

        return self.subqueries.count() > 0


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
         

class Select(Query):

    def __init__(self, chief, query_name):

        super().__init__(chief, "SELECT", query_name)

        self.DISTINCT = Clause(self, "DISTINCT")
        self.COLUMNS = Clause(self)
        self.FROM = Clause(self, "FROM")
        self.WHERE = Clause(self, "WHERE")
        self.GROUP_BY = Clause(self, "GROUP BY")
        self.ORDER_BY = Clause(self, "ORDER BY")

        self.clauses = [self.DISTINCT, self.COLUMNS, self.FROM, self.WHERE, self.GROUP_BY, self.ORDER_BY]


class Union(Query):

    def __init__(self, chief, query_name):

        super().__init__(chief, "UNION", query_name)


    def get_snippet(self):

        snippet = "\nUNION\n".join([utils.pars(self.subqueries.get_subquery(sq_name).get_snippet()) \
                                    for sq_name in self.subqueries.get_subquery_names()])

        return snippet


class Insert(Query):

    def __init__(self, chief, query_name):

        super().__init__(chief, "SELECT", query_name)

        self.INTO = Clause("INTO")
        self.VALUES = Clause("VALUES")
        self.SELECT = Clause("SELECT")
        self.FROM = Clause("FROM")
        self.WHERE = Clause("WHERE")

        self.clauses = [self.INTO, self.VALUES, self.SELECT, self.FROM, self.WHERE]


class QueryScript(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.queries = []
    

    def add_query(self, query):

        self.queries.append(query);

        return self


    def get_snippet(self):

        return "\n".join([q.get_snippet() + ";" for q in self.queries])


class Dbl(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.subqueries = []


    def new_select(self, query_name):

        return Select(self, query_name)


    def new_union(self, query_name):

        return Union(self, query_name)


    def new_insert(self, query_name):

        return Insert(self, query_name)


    def run_script(self, script):

        try:
            db_cursor.execute(script.get_snippet())
        except:
            status_code = status.ERR_DB_QUERY_FAILED

        return status_code


    def run_query(self, query):

        self.run_script(QueryScript(self).add_query(query))



    