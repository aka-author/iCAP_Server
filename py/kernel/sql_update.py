
import sql_queries


class Update(sql_queries.Query):

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