# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_queries.py                 
# Func:     Building SQL queries                 (\(\ 
# Usage:    Query is an abstract class           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import utils
import query_runners, db_recordsets, sql_builders, sql_workers


class Subqueries(sql_workers.SqlWorker):

    def __init__(self, chief: 'Query'):

        super().__init__(chief)

        self.subqueries = {}


    def count(self) -> int:

        return len(self.subqueries)


    def add(self, query: 'Query') -> 'Subqueries':

        self.subqueries[query.get_query_name()] = query.set_chief(self)
        query.set_subquery_flag()
        self.get_chief().adopt_subquery(query)

        return self


    def get_subquery(self, subquery_name: str) -> 'Query':

        return self.subqueries[subquery_name]


    def get_subquery_names(self) -> List:

        return [self.subqueries[sq_name].get_query_name() for sq_name in self.subqueries]


    def get_subquery_def(self, query: 'Query') -> str:

        # Code depends on a certain CMDB.

        return ""


    def get_snippet(self) -> str:

        # Code depends on a certain CMDB.
        # Postgres and MySQL 8 supports WITH, while earlier MySQL versions don't.
        
        return ""


    def is_subquery(self) -> bool:

        return False


    def is_main_query(self) -> bool:

        return False


class Clause(sql_workers.SqlWorker):

    def __init__(self, chief, clause_name: str=""):

        super().__init__(chief)

        self.clause_name = clause_name
        self.useful_flag = False


    def get_clause_name(self) -> str:

        return self.clause_name


    def turn_on(self) -> 'Clause': 

        self.useful_flag = True

        return self


    def is_useful(self) -> bool:

        return self.useful_flag   


    def set_snippet(self, snippet: str) -> 'Clause':

        self.get_chief().turn_on()

        return super().set_snippet(snippet) 
    

    def get_snippet(self) -> str:

        return utils.separate(self.get_clause_name(), " ", super().get_snippet())


class Query(db_recordsets.Recordset):

    def __init__(self, chief: query_runners.QueryRunner, operator_name: str, query_name: str=None):

        super().__init__(chief, utils.safeval(query_name, self.assemble_unique_query_name()))

        self.operator_name = operator_name

        self.clauses = []
        self.clauses_by_names = {}
        self.create_clauses()

        self.subqueries = self.get_default_dbms().new_subqueries().set_chief(self)
        self.subquery_flag = False

        self.explicit_template = None

        self.selective_flag = False


    def get_operator_name(self) -> str:

        return self.operator_name


    def assemble_unique_query_name(self) -> str:

        return utils.unique_name("q")


    def new_clause(self, clause_name: str) -> Clause:

        if clause_name == "SELECT":
            clause = ClauseSelect(self)
        else:
            clause = Clause(self, clause_name)

        return clause


    def add_clause(self, clause_name: str) -> 'Query':

        clause = self.new_clause(clause_name)

        self.clauses.append(clause)
        self.clauses_by_names[clause.get_clause_name()] = clause 

        return self
    

    def get_clause(self, clause_name: str) -> Clause:

        return self.clauses_by_names.get(clause_name)


    def set_clause_snippet(self, clause_name: str, snippet: str) -> 'Query':

        self.get_clause(clause_name).set_snippet(snippet)

        return self


    def extend_clause_snippet(self, clause_name: str, snippet: str, separ: str=" ") -> 'Query':

        clause = self.get_clause(clause_name)
        curr_snippet = clause.get_snippet()
        clause.set_stippet(curr_snippet + separ + snippet)

        return self


    def get_clauses_snippet(self) -> str:

        return "\n".join([clause.get_snippet() for clause in self.clauses if clause.is_useful()])


    def new_subqueries(self) -> Subqueries:

        return Subqueries(self)


    def has_subqueries(self) -> bool:

        return self.subqueries.count() > 0


    def adopt_subquery(self, query: object) -> 'Query':

        return self


    def set_subquery_flag(self, is_subquery: bool=True) -> 'Query':

        self.subquery_flag = is_subquery

        return self


    def set_explicit_template(self, template: str) -> 'Query':

        self.explicit_template = template

        return self


    def has_explicit_template(self) -> bool:

        return self.explicit_template is not None
    

    def get_explicit_template(self) -> str:

        return self.explicit_template


    def is_subquery(self) -> bool:

        return self.subquery_flag


    def is_main_query(self) -> bool:

        return not self.is_subquery()


    def is_selective(self) -> bool:

        return self.selective_flag;


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

    def __init__(self, chief: query_runners.QueryRunner, operator_name: str, query_name: str=None):

        super().__init__(chief, operator_name, query_name)

        self.selective_flag = True
