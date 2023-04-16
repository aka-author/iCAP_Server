# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Basestat
# Module:  basestat_processor.py                  (\(\
# Func:    Preprocessing measurements             (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 
from kernel import status, fields, dtos, workers, performer_shortcuts, performers, perftask, \
                     sql_select, sql_insert, perfoutput, grq_report_query
# import basestat_queries

class BasestatQueryBuilder(workers.Worker):

    def get_basestat_actions_varnames(self): 

        varnames = \
            ["accepted_at", "icap.pagereadId",
             "icap.cms.doc.uid", "icap.cms.doc.localCode", "icap.cms.doc.verno", 
             "icap.cms.topic.uid", "icap.cms.topic.verno", 
             "icap.page.title", "icap.page.url", 
             "icap.action.code", "icap.action.timeOffset", "icap.action.message", 
             "icap.countryCode", "userLangCode", "userAgentInfo", "userOs", "userBrowser"]
        
        return varnames


    def assemble_pageread_country_query(self) -> sql_select.Select:

        arg_names = ["icap.pagereadId"]
        
        out_names = ["icap.countryCode"]

        src_desk = self.get_app().get_source_desk()
        pageread_country_query = src_desk.assemble_measurements_query(arg_names, out_names)\
                                    .set_query_name("countries")

        return pageread_country_query 
    

    def assemble_full_actions_query(self) -> sql_select.Select:
        
        source_desk = self.get_app().get_source_desk()

        pagereads_query = source_desk.assemble_measurements_query(
            ["icap.pagereadId"],
            ["icap.cms.doc.uid", "icap.cms.doc.localCode", "icap.cms.doc.verno", 
             "icap.cms.topic.uid", "icap.cms.topic.verno",
             "icap.page.title", "icap.page.url", "userLangCode", "userAgentInfo"])

        actions_query = source_desk.assemble_measurements_query(\
            ["icap.pagereadId", "icap.action.code", "icap.action.timeOffset"], 
            ["icap.action.message"], "flex")
        
        countries_query = self.assemble_pageread_country_query()

        expros = """CASE 
                  WHEN {0} LIKE '%Android%' THEN 'android' 
                  WHEN {0} LIKE '%iP%' THEN 'ios' 
                  WHEN {0} LIKE '%Linux%' THEN 'linux' 
                  WHEN {0} LIKE '%Mac%' THEN 'macos'
                  WHEN {0} LIKE '%Win%' THEN 'windows' 
                  ELSE 'other' 
                  END"""
      
        exprbr = """CASE
                  WHEN LOWER({0}) LIKE '%chrom%' THEN 'chrome'
                  WHEN LOWER({0}) LIKE '%edg%' THEN 'edge'  
                  WHEN LOWER({0}) LIKE '%firefox%' THEN 'firefox'
                  WHEN LOWER({0}) LIKE '%opr%' THEN 'opera'
                  WHEN LOWER({0}) LIKE '%safari%' THEN 'safari' 
                  ELSE 'other' 
                  END"""

        full_actions_query = self.get_default_dbms().new_select().set_query_name("full_actions")

        full_actions_query.subqueries\
            .add(pagereads_query)\
            .add(actions_query)\
            .add(countries_query)
        
        full_actions_query\
            .FROM((pagereads_query.get_query_name(),))\
            .INNER_JOIN((actions_query.get_query_name(),))\
            .ON("{0}={1}", ("icap.pagereadId", 0), ("icap.pagereadId", 1))\
            .LEFT_JOIN((countries_query.get_query_name(),))\
            .ON("{0}={1}", ("icap.pagereadId", 0), ("icap.pagereadId", 2))\
            .SELECT_field(("accepted_at", 0))\
            .SELECT_field(("icap.pagereadId", 0))\
            .SELECT_field(("icap.cms.doc.uid", 0))\
            .SELECT_field(("icap.cms.doc.localCode", 0))\
            .SELECT_field(("icap.cms.doc.verno", 0))\
            .SELECT_field(("icap.cms.topic.uid", 0))\
            .SELECT_field(("icap.cms.topic.verno", 0))\
            .SELECT_field(("icap.page.title", 0))\
            .SELECT_field(("icap.page.url", 0))\
            .SELECT_field(("icap.action.code", 1))\
            .SELECT_field(("icap.action.timeOffset", 1))\
            .SELECT_field(("icap.action.message", 1))\
            .SELECT_field(("icap.countryCode", 2))\
            .SELECT_field(("userLangCode", 0))\
            .SELECT_field(("userAgentInfo", 0))\
            .SELECT_expression("userOs", expros, ("userAgentInfo", 0))\
            .SELECT_expression("userBrowser", exprbr, ("userAgentInfo", 0))
      
        return full_actions_query


class BasestatProcessor(performers.Processor):

    def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


    def assemble_load_actions_query(self) -> sql_insert.Insert:
       
        bqb = BasestatQueryBuilder(self)

        dbms, db = self.get_default_dbms(), self.get_default_db()

        scheme_name = self.get_default_db_scheme_name()

        timebase_query = dbms.new_select().set_query_name("timebase")\
                .FROM(("basestat__actions", scheme_name))\
                .SELECT_expression("start_from", "max({0})", ("accepted_at",))

        full_actions_query = bqb.assemble_full_actions_query()

        basestat_actions_query = dbms.new_select().set_query_name("basestat_actions")

        basestat_actions_query.subqueries\
            .add(full_actions_query)\
            .add(timebase_query)
        
        basestat_actions_query\
            .FROM((full_actions_query.get_query_name(),))\
            .INNER_JOIN((timebase_query.get_query_name(),))\
            .ON("true")\
            .WHERE("CASE WHEN {1} IS NOT null THEN {0}>{1} ELSE true END", ("accepted_at", 0), ("start_from", 1))
        
        for varname in bqb.get_basestat_actions_varnames():
            basestat_actions_query.SELECT_field((varname, 0))
                
        load_actions = dbms.new_insert().set_query_name("load_actions")

        load_actions.subqueries\
            .add(basestat_actions_query)
                
        load_actions\
            .INTO("basestat__actions", scheme_name, *(["uuid"] + bqb.get_basestat_actions_varnames()))\
            .FROM((basestat_actions_query.get_query_name(),))\
            .SELECT_expression("uuid", "gen_random_uuid()")
        
        for varname in bqb.get_basestat_actions_varnames():
            load_actions.SELECT_field((varname,))
            
        return load_actions


    def process(self) -> None:

        dbms, db = self.get_default_dbms(), self.get_default_db()

        load_action_query = self.assemble_load_actions_query()

        runner = dbms.new_query_runner(db)
        runner.execute_query(load_action_query)
        runner.commit()
        runner.close()


def new_processor(shortcut: performer_shortcuts.PerformerShortcut) -> performers.Processor:

   return BasestatProcessor(shortcut.get_chief()).set_shortcut(shortcut)