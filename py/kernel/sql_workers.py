# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sql_workers.py                               
# Func:    Performing common operations related to SQL  (\(\
# Usage:   The class is abstract                        (^.^)
# # ## ### ##### ######## ############# #####################

import workers


class SqlWorker(workers.Worker):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.snippet = None
        self.sql_builder = self.get_dbms().new_sql_builder(self)


    def get_dbms(self) -> 'SqlWorker':

        return self.get_chief().get_dbms() if self.has_chief() else None


    @property
    def sql(self):

        return self.sql_builder
    

    def set_snippet(self, snippet: str) -> 'SqlWorker':

        self.snippet = snippet

        return self


    def extend_snippet(self, snippet_extension: str, separ: str=" ") -> "SqlWorker":

        curr_snippet = str(self.snippet)

        snippet_head = curr_snippet + separ if curr_snippet != "" else "" 

        self.set_snippet(snippet_head + snippet_extension)

        return self


    def assemble_snippet(self) -> str:

        return ""


    def get_snippet(self) -> str:

        return self.snippet if self.snippet is not None else self.assemble_snippet()