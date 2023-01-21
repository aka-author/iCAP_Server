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
