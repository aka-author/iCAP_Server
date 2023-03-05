# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   sql_queries.py                 
# Func:     Building SQL queries                 (\(\ 
# Usage:    Query is an abstract class           (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import utils
import sql_workers, dbms_instances, db_recordsets


class Subqueries(sql_workers.SqlWorker):

    def __init__(self, chief: 'Query'):

        super().__init__(chief)

        self.subqueries = {}


    def get_query(self) -> 'Query':

        return self.get_chief()
    

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

    def __init__(self, chief: 'Query'):

        super().__init__(chief)

        self.clause_name = ""

        self.headless_flag = False

        self.useful_flag = False


    def get_clause_name(self) -> str:

        return self.clause_name
    

    def get_query(self) -> 'Query':

        return self.get_chief()


    def set_headless_flag(self, flag: bool=True) -> 'Clause':

        self.headless_flag = flag

        return self


    def is_headless(self) -> bool:

        return self.headless_flag
    

    def turn_on(self) -> 'Clause': 

        self.useful_flag = True

        return self


    def is_useful(self) -> bool:

        return self.useful_flag   


    def set_snippet(self, snippet: str) -> 'Clause':

        self.snippet = snippet
        self.turn_on()

        return self 
    

    def get_snippet(self) -> str:

        if not self.is_headless():
            snippet = " ".join([self.get_clause_name(), super().get_snippet()])
        else:
            snippet = super().get_snippet()

        return snippet
    

class MonotableClause(Clause):

    def __init__(self, chief: 'Query'):

        super().__init__(chief)

        self.db_scheme_name = None
        self.table_name = None


    def set_db_scheme_name(self, db_scheme_name: str) -> 'MonotableClause':

        self.db_scheme_name = db_scheme_name

        return self
    

    def get_db_scheme_name(self) -> str: 

        return self.db_scheme_name
    

    def set_table_name(self, table_name: str) -> 'MonotableClause':

        self.table_name = table_name

        return self
    

    def get_table_name(self) -> str: 

        return self.table_name 
    

    def get_qualified_table_name(self) -> str:

        return self.sql.qualified_table_name(self.get_table_name(), self.get_db_scheme_name())


class WhereClause(Clause):

    def __init__(self, chief: 'Query'):

        super().__init__(chief)

        self.clause_name = "WHERE"

        self.expression = ""
        self.operands = []


    def set_expression(self, expression: str) -> 'WhereClause':

        self.expression = expression

        return self


    def extend_expression(self, logfunc: str, *expressions: str) -> 'WhereClause':

        logfunc_padded = " " + logfunc.upper() + " "
        expression_in_parses = [utils.pars(expression) for expression in expressions]
        head = utils.pars(self.expression)
        tail = logfunc_padded.join(expression_in_parses)

        self.expression = logfunc_padded.join(head, tail)

        return self


    def add_operands(self, *operands) -> 'WhereClause':

        for operand in operands:
            self.operands.append(self.sql.operand(operand))

        return self


    def assemble_snippet(self) -> str:
        
        return self.expression.format(*self.operands)


class Query(db_recordsets.Recordset):

    def __init__(self, chief: 'dbms_instances.Dbms', operator_name: str, query_name: str=None):

        super().__init__(chief, utils.safeval(query_name, self.assemble_unique_query_name()))

        self.operator_name = operator_name

        self.clauses = []
        self.clauses_by_names = {}
        self.create_clauses()

        self.subqueries = self.get_dbms().new_subqueries(self).set_chief(self)
        self.subquery_flag = False

        self.explicit_template = None

        self.selective_flag = False


    def get_operator_name(self) -> str:

        return self.operator_name


    def assemble_unique_query_name(self) -> str:

        return utils.unique_name("q")


    def add_clause(self, clause: Clause) -> 'Query':

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

        return self.selective_flag
    
    
    def get_field_group_alias_by_index(self, field_group_index: int) -> str:

        return None


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

    def __init__(self, chief: 'dbms_instances.Dbms', operator_name: str, query_name: str=None):

        super().__init__(chief, operator_name, query_name)

        self.selective_flag = True
