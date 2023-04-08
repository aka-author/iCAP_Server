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


    # Measurements

    def new_measurement(self) -> measurements.Measurement:

        return measurements.Measurement(self)


    def insert_measurement(self, measurement: measurements.Measurement) -> 'SourceDesk':

        if measurement.is_valid() and measurement.is_unique():
            measurement.insert()

        return self


    def assemble_measurements_query(self, arg_varnames: List, out_varnames: List) -> sql_select.Select:

        measurements_query = self.get_default_dbms().new_select()

        dd = self.get_app().get_directory_desk()
        sql = self.get_default_dbms().new_sql_builder(None)
        sch_name = self.get_app().get_default_db_scheme_name()

        # Measurements 

        measurements_query.FROM(("measurements", sch_name))
        
        arg_shortcuts = [dd.get_variable_shortcut(varname) for varname in arg_varnames]
        argprof = measurements.assemble_varprof(arg_shortcuts)
        
        if len(out_varnames) > 0:
            out_shortcuts = [dd.get_variable_shortcut(varname) for varname in out_varnames]
            outprof = measurements.assemble_varprof(out_shortcuts)
            measurements_query\
                .WHERE("({0}={1}) AND " + sql.match_measurement_profiles(2, 3), 
                    ("argprof", 0), argprof, ("outprof", 0), outprof) 
        else:
            measurements_query\
                .WHERE("{0}={1}", ("argprof", 0), argprof) 
        
        measurements_query\
            .SELECT_field(("uuid", 0))\
            .SELECT_field(("accepted_at", 0)) 

        # Argument variable values

        for idx, varname in enumerate(arg_varnames):
            recordset_idx = idx + 1
            measurements_query\
                .INNER_JOIN(("varvalues", sch_name))\
                .ON("{0}={1} AND {2}={3}", 
                    ("uuid", 0), ("measurement_uuid", recordset_idx),
                    ("varname", recordset_idx), varname)        

        for idx, varname in enumerate(arg_varnames):
            recordset_idx = idx + 1
            datatype_name = dd.get_variable_datatype_name(varname)
            measurements_query.SELECT_field(
                ("serialized_value", recordset_idx, datatype_name), varname)
            
        # Outpot variable values 

        for idx, varname in enumerate(out_varnames):
            recordset_idx = len(arg_varnames) + idx + 1
            measurements_query\
                .LEFT_JOIN(("varvalues", sch_name))\
                .ON("{0}={1} AND {2}={3}", 
                    ("uuid", 0), ("measurement_uuid", recordset_idx),
                    ("varname", recordset_idx), varname)

        for idx, varname in enumerate(out_varnames):
            recordset_idx = len(arg_varnames) + idx + 1
            datatype_name = dd.get_variable_datatype_name(varname)
            measurements_query.SELECT_field(
                ("serialized_value", recordset_idx, datatype_name), varname)
        
        return measurements_query       


    def assemble_messages_query(self) -> sql_select.Select:

        topic_pageread_query = self.assemble_measurements_query(
            ["icap.pagereadId"],
            ["icap.cms.doc.uid", "icap.cms.doc.verno", 
             "icap.cms.topic.uid", "icap.cms.topic.verno"])

        reader_action_query = self.assemble_measurements_query(\
            ["icap.pagereadId", "icap.action.code", "icap.action.timeOffset"],[])

        combo_query = self.get_default_dbms().new_select()

        combo_query.subqueries\
            .add(topic_pageread_query)\
            .add(reader_action_query)
        
        combo_query\
            .FROM((topic_pageread_query.get_query_name(),))\
            .INNER_JOIN((reader_action_query.get_query_name(),))\
            .ON("{0}={1}", ("icap.pagereadId", 0), ("icap.pagereadId", 1))\
            .SELECT_field(("icap.pagereadId", 0))\
            .SELECT_field(("icap.cms.doc.uid", 0))\
            .SELECT_field(("icap.cms.doc.verno", 0))\
            .SELECT_field(("icap.cms.topic.uid", 0))\
            .SELECT_field(("icap.cms.topic.verno", 0))\
            .SELECT_field(("icap.action.code", 1))\

        return combo_query 
