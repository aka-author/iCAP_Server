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

    def assemble_measurements_query(self, arg_varnames: List, out_varnames: List) -> sql_select.Select:

        measurements_query = self.get_default_dbms().new_select()

        dd = self.get_app().get_directory_desk()
        sch_name = self.get_app().get_default_db_scheme_name()

        # Measurements 

        measurements_query.FROM(("measurements", sch_name))

        measurements_query\
            .SELECT_field(("uuid", 0))\
            .SELECT_field(("accepted_at", 0)) 

        # Args

        for idx, varname in enumerate(arg_varnames):
            recordset_idx = idx + 1
            measurements_query\
                .INNER_JOIN(("varvalues", sch_name))\
                .ON("{0}={1} AND {2}={3}", 
                    ("uuid", 0), ("measurement_uuid", recordset_idx),
                    ("varname", recordset_idx), varname)


        # arg_shortcuts = [dd.get_variable_shortcut(varname) for varname in arg_varnames]
        # argsprof = measurements.assemble_argprof(arg_shortcuts)
        #measurements_query\
        #    .WHERE("{0}={1}", ("argprof", 0), argsprof)           

        for idx, varname in enumerate(arg_varnames):
            recordset_idx = idx + 1
            datatype_name = dd.get_variable_datatype_name(varname)
            measurements_query.SELECT_field(
                ("serialized_value", recordset_idx, datatype_name), varname)
            
        # Outs 

        for idx, varname in enumerate(out_varnames):
            recordset_idx = len(arg_varnames) + idx + 1
            measurements_query\
                .LEFT_JOIN(("varvalues", sch_name))\
                .ON("{0}={1} AND {2}={3}", 
                    ("uuid", 0), ("measurement_uuid", recordset_idx),
                    ("varname", recordset_idx), varname)
        
        # out_shortcuts = [dd.get_variable_shortcut(varname) for varname in out_varnames]
        # outprof = measurements.assemble_outprof(out_shortcuts)
        # print("=== ", outprof)
        # measurements_query\
        #     .WHERE("string_to_array({0}, '+') && string_to_array({1}, '+')", 
        #           ("outprof", 0), outprof) 

        for idx, varname in enumerate(out_varnames):
            recordset_idx = len(arg_varnames) + idx + 1
            datatype_name = dd.get_variable_datatype_name(varname)
            measurements_query.SELECT_field(
                ("serialized_value", recordset_idx, datatype_name), varname)
            

        arg_shortcuts = [dd.get_variable_shortcut(varname) for varname in arg_varnames]
        argprof = measurements.assemble_argprof(arg_shortcuts)
        #measurements_query\
        #    .WHERE("{0}={1}", ("argprof", 0), argsprof) 

        out_shortcuts = [dd.get_variable_shortcut(varname) for varname in out_varnames]
        outprof = measurements.assemble_outprof(out_shortcuts)
        print("=== ", outprof)
        measurements_query\
            .WHERE("({0}={1}) AND (string_to_array({2}, '+') && string_to_array({3}, '+'))", 
                   ("argprof", 0), argprof,
                   ("outprof", 0), outprof) 
        
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
            ["icap.action.message"]
        )

        return messages_query 
