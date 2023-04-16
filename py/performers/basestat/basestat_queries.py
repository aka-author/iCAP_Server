from typing import Dict, List
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 
from kernel import status, fields, workers, sql_select


class BasestatQueryBuilder(workers.Worker):

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
            ["icap.action.message"])
        
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