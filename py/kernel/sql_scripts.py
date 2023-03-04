# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sqlscript.py                    (\(\
# Func:    Bundling SQL queries            (^.^)
# # ## ### ##### ######## ############# #####################

import sql_workers, sql_builders, sql_queries


class Script(sql_workers.SqlWorker):

    def __init__(self, chief, script_name: str="noname"):

        super().__init__(chief)

        self.script_name = script_name
        self.queries = []
        self.selective_query = None


    def get_script_name(self) -> str:

        return self.script_name


    def assemble_snippet(self) -> str:

        return ";\n".join([q.get_snippet() for q in self.queries]) + (";" if self.count_queries() > 0 else "")


    def is_selective(self) -> bool:

        return self.selective_query is not None


    def add_query(self, query: sql_queries.Query) -> object:

        self.queries.append(query)

        if query.is_selective():
            self.selective_query = query

        return self


    def count_queries(self) -> int:

        return len(self.queries)


    def get_selective_query(self) -> sql_queries.Query:

        return self.selective_query