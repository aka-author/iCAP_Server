# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  srcdesk.py                        (\(\
# Func:    Managing source data              (^.^)
# # ## ### ##### ######## ############# #####################

import bureaucrat, fields, ramtable


class SourceDesk(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def check_measurement(self, hashkey):

        measurement_exists = False

        rt_cc = ramtable.Table("measurements")\
            .add_field(fields.IntField("count_competitors").set_sql_agg_expr("count(uuid)"))

        dbl = self.get_dbl()

        q_cc = dbl.new_select("count_competitors", "icap").set_output_ramtable(rt_cc)\
            .WHERE.sql.set("hashkey='" + hashkey + "'").q

        dbl = self.get_dbl().execute(q_cc)

        if rt_cc.count_rows() == 1: 
            measurement_exists = rt_cc.select_by_index(0).get_field_value("count_competitors") > 0

        return measurement_exists


    def get_measurements_query(self, mandatory_varnames, optional_varnames=[]):

        q = self.get_dbl().new_select(self)
        q.COLUMNS.sql.add_list_items(["m.uuid", "m.accepted_at"])
        q.FROM.sql.set("icap.measurements m")

        varcol  = "v{0}.serialized_value::{2} as {1}"
        varsubq = "(SELECT * FROM icap.varvalues WHERE variable_uuid = '{1}') v{0}"
        varon   = "ON (m.uuid = v{0}.measurement_uuid)"
        varfrom = varsubq + " " + varon 

        dd = self.get_app().get_directory_desk()
        count = 0

        for varname in mandatory_varnames + optional_varnames:

            var = dd.get_variable_by_name(varname)

            if var is not None:

                var_uuid = var.get_uuid()
                sql_varname = var.get_sql_varname()
                sql_dt = var.get_sql_datatype_name() 

                q.COLUMNS.sql.add_list_items([varcol.format(count, sql_varname, sql_dt)], ", ")
                join = "JOIN" if varname in mandatory_varnames else "LEFT JOIN" 
                q.FROM.sql.add_list_items([varfrom.format(count, var_uuid)], " " + join + " ")

            count += 1

        return q
