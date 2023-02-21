# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sqlscript.py                    (\(\
# Func:    Bundling SQL queries            (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat, sqlbuilder


class Script(bureaucrat.Bureaucrat):

    def __init__(self, chief: bureaucrat.Bureaucrat, script_name: str="noname"):

        super().__init__(chief)

        self.script_name = script_name
        self.queries = []
        self.selective_query = None

        self.sqlprop = sqlbuilder.Sql(self)


    def get_script_name(self) -> str:

        return self.script_name


    def assemble_snippet(self) -> str:

        return ";\n".join([q.get_snippet() for q in self.queries]) + (";" if self.count_queries() > 0 else "")


    @property
    def sql(self) -> sqlbuilder.Sql:

        self.sqlprop.set(self.assemble_snippet(self))

        return self.sqlprop


    def is_selective(self) -> bool:

        return self.selective_query is not None


    def add_query(self, query: sqlbuilder.Query) -> object:

        self.queries.append(query)

        if query.is_selective():
            self.selective_query = query

        return self


    def count_queries(self) -> int:

        return len(self.queries)


    def import_source_ramtable(self, src_rt):

        if src_rt is not None: 
            for idx in range(0, src_rt.count_rows()):
                self.add_query(Insert(self, None, \
                    self.get_scheme_name()).import_source_ramtable_row(src_rt.select_by_index(idx)))

        return self 


    def get_selective_query(self) -> sqlbuilder.Query:

        return self.selective_query