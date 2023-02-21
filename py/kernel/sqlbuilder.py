# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  sqlbuilder.py                        (\(\
# Func:    Assembling SQL queries               (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
import utils, datatypes, fields, bureaucrat


def sql_datatype_name(self, icap_datatype_name: str) -> str:

    return icap_datatype_name


def get_format_for_datatype(self, icap_datatype_name: str) -> str:

    return datatypes.get_format(icap_datatype_name)


def sql_list(self, items: List) -> str:

    return ", ".join(items)


def sql_typed_phrase(self, phrase: str, icap_datatype_name: str) -> str:

    return phrase + "::" + self.sql_datatype_name(icap_datatype_name)


def sql_table_alias(self, table_alias: str) -> str:

    return table_alias + "." if table_alias is not None else ""


def sql_varname(self, icap_varname: str, table_alias: str=None) -> str:

    return self.sql_table_alias(table_alias) + icap_varname.replace(".", "__").replace(" ", "_")


def sql_typed_varname(self, icap_varname: str, icap_datatype_name: str, table_alias: str=None) -> str:

    return self.sql_typed_phrase(self.sql_varname(icap_varname, table_alias), icap_datatype_name)


def sql_substitute_varnames(self, expr: str, varnames: str, table_alias: str=None) -> str:

    # {price}*{numner} -> t.price*t.number 

    expr_sv = expr

    for varname in varnames:
        varname_pattern = "{" + varname + "}"
        expr_sv = expr_sv.replace(varname_pattern, self.sql_varname(varname, table_alias))

    return expr_sv 


def sql_value(self, raw_value_for_sql: str, icap_datatype_name: str) -> str:

    s_v = "null"

    if raw_value_for_sql is not None:
        sql_datatype_name = self.sql_datatype_name(icap_datatype_name)
        need_apos = ["uuid", "varchar", "timestamp", "timestamptz", "json"]
        s_v = utils.apos(raw_value_for_sql) if sql_datatype_name in need_apos else raw_value_for_sql

    return s_v
        

def sql_typed_value(self, serialized_value: str, icap_datatype_name: str) -> str:

    return self.sql_typed_phrase(self.sql_value(serialized_value), icap_datatype_name)


def sql_table_name(self, table_local_name: str, scheme_name: str=None) -> str:

    sql_tn = table_local_name

    if scheme_name is not None:
        sql_tn = scheme_name + "." + table_local_name

    return sql_tn 



class Sql(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)

        self.snippet = ""





    def get_things(self, fm, varname):

        return self.get_dbms(), fm.get_field(varname), fm.get_field_value(varname)


    def sql_varname(self, varname, table_alias=None):

        return self.get_dbms().sql_varname(varname, table_alias)


    def sql_typed_varname(self, fm, varname, table_alias=None):

        dbms, field, _ = self.get_things(fm, varname)

        return dbms.sql_typed_varname(varname, field.get_base_datatype_name(), table_alias)


    def sql_all_varnames(self, fm, table_alias=None):

        varname_snippets = [self.sql_varname(fm, varname, table_alias) for varname in fm.get_varnames()]

        return self.get_dbms().sql_list(varname_snippets)


    def sql_value(self, fm, varname, other_native_value=datatypes.DTN_UNDEFINED):

        dbms, field, field_native_value = self.get_things(fm, varname)

        native_value = other_native_value if not datatypes.is_undefined(other_native_value) else field_native_value

        base_datatype_name = field.get_base_datatype_name()

        if native_value is not None:
            format = dbms.get_format_for_datatype(base_datatype_name)
            raw_sql_value = field.get_serialized_value(native_value, format)
        else:
            raw_sql_value = None

        return dbms.sql_value(raw_sql_value, base_datatype_name)


    def sql_typed_value(self, fm, varname, native_value=datatypes.DTN_UNDEFINED):
        
        return self.get_dbms().sql_typed_phrase(self.sql_value(fm, varname, native_value))

    
    def sql_expr(self, fm, varname, table_alias=None):

        dbms, field, _ = self.get_things(fm, varname)

        varnames = [varname for varname in fm.get_varnames()]

        return dbms.sql_substitute_varnames(field.get_expr(), varnames, table_alias)

    def as_varname(self, expr, varname):

        return utils.separate(expr, " AS ", self.get_dbms().sql_varname(varname))


    def sql_selectable_field(self, fm, varname, alias_table=None):

        _, field, _ = self.get_things(fm, varname)

        return self.as_varname(self.sql_expr(fm, varname, alias_table), varname) if field.has_expr() \
                    else self.sql_varname(fm, varname, alias_table)


    def sql_insertable_fields(self, fm, table_alias=None):

        dbms = self.get_dbms()

        return dbms.sql_list([self.sql_varname(dbms, varname, table_alias) \
                                for varname in self.get_varnames() if fm.get_field(varname).is_insertable()])


    def sql_all_typed_values(self, fm):

        dbms = self.get_dbms()

        return dbms.sql_list([self.sql_typed_value(fm, varname) for varname in fm.get_varnames()])


    def sql_insertable_typed_values(self, fm):

        dbms = self.get_dbms()

        return dbms.sql_list([self.sql_typed_value(fm, varname) \
                                for varname in fm.get_varnames() if fm.get_field(varname).is_insertable()])


    def sql_equal(self, fm, varname, native_value=datatypes.DTN_UNDEFINED, table_alias=None):

        _, _, native_value = self.get_things(fm, varname)

        return self.sql_varname(fm, varname, table_alias) + " = " + self.sql_typed_value(fm, varname, native_value)


    def set_snippet(self, snippet):

        self.snippet = snippet 

        return self


    def set(self, snippet=""):

        return self.set_snippet(snippet)


    def set_list_items(self, snippets):

        return self.set_snippet(", ".join(snippets))


    def add(self, snippet, separ=" "):

        return self.set_snippet(utils.separate(self.snippet, separ, snippet))


    def add_list_items(self, snippets, separ=" "):

        return self.set_snippet(utils.separate(self.snippet, separ, ", ".join(snippets)))


    def add_selectable_fields(self, fm, table_alias=None):

        dbms = self.get_dbms()

        return dbms.sql_list([self.sql_selectable_field(fm, varname, table_alias) for varname in fm.get_varnames()])


    def sql_add_field_equal(self, fm, varname, native_value=datatypes.DTN_UNDEFINED, table_alias):

        return self.add_list_items([self.sql_equal(fm, varname, native_value, table_alias)])


    def get_snippet(self):

        return self.snippet


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











