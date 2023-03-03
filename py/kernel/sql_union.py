

import sql_queries

class Union(sql_queries.SelectiveQuery):

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