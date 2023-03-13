# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  srcdesk.py                        (\(\
# Func:    Managing source data              (^.^)
# # ## ### ##### ######## ############# #####################

import workers, desks, measurements


class SourceDesk(desks.Desk):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def new_measurement(self) -> measurements.Measurement:

        return measurements.Measurement(self)


    def insert_measurement(self, measurement: measurements.Measurement) -> 'SourceDesk':

        if measurement.is_valid() and measurement.is_unique():
            measurement.insert()

        return self


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
