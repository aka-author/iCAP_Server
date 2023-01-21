
import bureaucrat, fields, ramtable

class DbIcap(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def check_measurement(self, signature):

        rt_cc = ramtable.Table("measurements")\
            .add_field(fields.IntField("count_competitors").set_sql_agg_expr("count(uuid)"))

        dbl = self.get_dbl()

        q_cc = dbl.new_select("count_competitors", "icap").set_output_ramtable(rt_cc)\
        .WHERE.sql.set("signature='" + signature + "'").q

        print(q_cc.get_snippet())

        dbl = self.get_dbl()

        dbl.execute(q_cc)

        print(rt_cc.select_by_index(0).get_field_value("count_competitors"))

        return rt_cc.select_by_index(0).get_field_value("count_competitors") > 0
