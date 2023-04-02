# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  srcdesk.py                        (\(\
# Func:    Managing source data              (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import workers, desks, measurements, sql_select


class SourceDesk(desks.Desk):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)


    def new_measurement(self) -> measurements.Measurement:

        return measurements.Measurement(self)


    def insert_measurement(self, measurement: measurements.Measurement) -> 'SourceDesk':

        if measurement.is_valid() and measurement.is_unique():
            measurement.insert()

        return self


    # Measurements

    # def get_measurements_query(self, mandatory_varnames, optional_varnames=[]):

    #    q = self.get_dbl().new_select(self)
    #    q.COLUMNS.sql.add_list_items(["m.uuid", "m.accepted_at"])
    #    q.FROM.sql.set("icap.measurements m")

    #    varcol  = "v{0}.serialized_value::{2} as {1}"
    #    varsubq = "(SELECT * FROM icap.varvalues WHERE variable_uuid = '{1}') v{0}"
    #    varon   = "ON (m.uuid = v{0}.measurement_uuid)"
    #    varfrom = varsubq + " " + varon 

    #    dd = self.get_app().get_directory_desk()
    #    count = 0

    #    for varname in mandatory_varnames + optional_varnames:

    #        var = dd.get_variable_by_name(varname)

    #        if var is not None:

    #            var_uuid = var.get_uuid()
    #            sql_varname = var.get_sql_varname()
    #            sql_dt = var.get_sql_datatype_name() 

    #            q.COLUMNS.sql.add_list_items([varcol.format(count, sql_varname, sql_dt)], ", ")
    #            join = "JOIN" if varname in mandatory_varnames else "LEFT JOIN" 
    #            q.FROM.sql.add_list_items([varfrom.format(count, var_uuid)], " " + join + " ")

    #        count += 1

    #    return q
    

    def assemble_measurements_query(self, args: List, outs: List) -> sql_select.Select:

        measurements_query = self.get_default_dbms().new_select()

        dd = self.get_app().get_directory_desk()

        args_prof = dd.assemble_args_prof(args)
        # outs_prof = dd.assemble_outs_prof(outs)

        sch_name = self.get_app().get_default_db_scheme_name()

        measurements_query.FROM(("measurements", sch_name))
        
        for idx, varname in enumerate(args):
            recordset_idx = idx + 1
            measurements_query\
                .INNER_JOIN(("varvalues", sch_name))\
                .ON("{0}={1} AND {2}={3}", 
                    ("uuid", 0), ("measurement_uuid", recordset_idx),
                    ("varname", recordset_idx), varname)

        measurements_query\
            .WHERE("{0}={1}", ("argprof", 0), args_prof)
        
        measurements_query\
            .SELECT_field(("uuid", 0))\
            .SELECT_field(("accepted_at", 0))            

        for idx, varname in enumerate(args):
            recordset_idx = idx + 1
            measurements_query.SELECT_field(
                ("serialized_value", recordset_idx), varname)

        return measurements_query       


    def assemble_messages_query(self) -> sql_select.Select:

        # messages_query = self.get_default_dbms().new_select()\
        #        .FROM(("measurements", self.get_default_db_scheme_name()))\
        #        .WHERE("True")\
        #        .SELECT_field(("message", 0))


        messages_query = self.assemble_measurements_query(
            ["icap.cms.doc.uid", "icap.cms.doc.verno", 
             "icap.cms.topic.uid", "icap.cms.topic.verno",
             "icap.action.code"], 
            []
        )

        return messages_query 
