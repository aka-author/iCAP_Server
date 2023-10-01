# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Performer (Webstat)
# Module:  webstat_reporter.py                         (\(\
# Func:    Building statistical reports for webhelps   (^.^)
# # ## ### ##### ######## ############# #####################

import sys
import os
import pathlib

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 

from kernel import (
   status, fields, dtos, performer_shortcuts, performers, 
   perftask, sql_select, perfoutput, grq_report_query
)

from debug import deb_reporter


class WebstatReporter(performers.Reporter):

   def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


   # Common queries

   def get_source_data_age_sec(self) -> int:
      return 5*60

   def get_action_varnames(self) -> list:

      varnames = [
         "accepted_at", 
         "icap.cms.doc.uid", "icap.cms.doc.localCode", "icap.cms.doc.verno",
         "icap.cms.topic.uid", "icap.cms.topic.verno",
         "icap.page.title", "icap.page.url",
         "icap.action.code", "icap.action.timeOffset", "icap.action.message",
         "icap.countryCode", "userLangCode", "userOs", "userBrowser"
      ]
      
      return varnames

   def get_taxonomy_varnames(self) -> list:

      dir_desk = self.get_app().get_directory_desk()

      taxonomy_varnames = [
         varname for varname in dir_desk.get_varnames() if ".taxonomy." in varname
      ]

      return taxonomy_varnames
   
   def assemble_webstat_topics_query(self) -> sql_select.Select:

      arg_names = [
         "icap.cms.doc.uid", 
         "icap.cms.doc.localCode", 
         "icap.cms.doc.verno", 
         "icap.cms.topic.uid", 
         "icap.cms.topic.verno"
      ]
      
      out_names = self.get_taxonomy_varnames()

      src_desk = self.get_app().get_source_desk()
      webstat_topics_query = src_desk.assemble_measurements_query(arg_names, out_names)\
                              .set_query_name("topicmeta")

      return webstat_topics_query


   def assemble_webstat_actions_query(self) -> sql_select.Select:

      webstat_actions_query = self.get_default_dbms().new_select()

      webstat_actions_query\
         .FROM(("webstat__actions", self.get_default_db_scheme_name()))
      
      for varname in self.get_action_varnames():
         webstat_actions_query.SELECT_field((varname,))
         
      return webstat_actions_query
   

   # Detecting available directory codes

   def grab_directory(self, directory_field_name: str) -> list:

      dircodes = []

      dbms, db = self.get_default_dbms(), self.get_default_db()

      dircodes_field_manager = fields.FieldManager()\
         .add_field(fields.StringField(directory_field_name))
      
      dircodes_query = dbms.new_select()\
         .set_field_manager(dircodes_field_manager)
      
      dircodes_query\
         .FROM(("webstat__actions", self.get_default_db_scheme_name()))\
         .DISTINCT()\
         .SELECT_field((directory_field_name,))
      
      runner = dbms.new_query_runner(db)
      query_result = runner.execute_query(dircodes_query).get_query_result()
      
      if query_result is not None:
         for country_dict in query_result.dump_list_of_dicts():
            dircodes.append(country_dict[directory_field_name])

      runner.close()

      return dircodes


   def grab_countries(self) -> list:

      return self.grab_directory("icap__countrycode")

   
   def grab_browsers(self) -> list: 

      return self.grab_directory("userbrowser")


   def grab_oss(self) -> list: 

      return self.grab_directory("useros")
   

   def grab_user_langs(self) -> list: 

      return self.grab_directory("userlangcode")
   

   def grab_locals(self) -> list: 

      return self.grab_directory("icap__cms__doc__localcode")


   def assemble_directories_report(self, report_query_dict: dict) -> dict:

      directories_report_dict = {
         "source_data_age_sec": self.get_source_data_age_sec(),
         "countries": self.grab_countries(),
         "browsers": self.grab_browsers(),
         "oss": self.grab_oss(),
         "user_langs": self.grab_user_langs(),
         "locals": self.grab_locals()
      }

      return directories_report_dict


   # Selecting messages within a specified scope

   def assemble_actions_topics_query(self) -> sql_select.Select:
        
      actions_query = self.assemble_webstat_actions_query().set_query_name("actions") 
      topics_query = self.assemble_webstat_topics_query().set_query_name("topics")

      actions_topics_query = self.get_default_dbms().new_select()\
         .set_query_name("actions_topics") 

      actions_topics_query.subqueries\
         .add(actions_query)\
         .add(topics_query)
        
      actions_topics_query\
         .FROM((actions_query.get_query_name(),))\
         .LEFT_JOIN((topics_query.get_query_name(),))\
         .ON("{0}={1} AND {2}={3} AND {4}={5} AND {6}={7} AND {8}={9}", 
             ("icap.cms.doc.uid", 0), ("icap.cms.doc.uid", 1),
             ("icap.cms.doc.localCode", 0), ("icap.cms.doc.localCode", 1), 
             ("icap.cms.doc.verno", 0), ("icap.cms.doc.verno", 1),
             ("icap.cms.topic.uid", 0), ("icap.cms.topic.uid", 1),
             ("icap.cms.topic.verno", 0), ("icap.cms.topic.verno", 1))
      
      for action_varname in self.get_action_varnames():
         actions_topics_query.SELECT_field((action_varname, 0))
      
      for taxonomy_varname in self.get_taxonomy_varnames():
         actions_topics_query.SELECT_field((taxonomy_varname, 1))
         
      return actions_topics_query 

   def assemble_messages_field_manager(self) -> fields.FieldKeeper():

      messages_field_manager = fields.FieldManager()\
         .add_field(fields.TimestampField("accepted_at"))\
         .add_field(fields.StringField("icap.cms.doc.uid"))\
         .add_field(fields.StringField("icap.cms.doc.localCode"))\
         .add_field(fields.StringField("icap.cms.doc.verno"))\
         .add_field(fields.StringField("icap.cms.topic.uid"))\
         .add_field(fields.StringField("icap.cms.topic.verno"))\
         .add_field(fields.StringField("icap.page.title"))\
         .add_field(fields.StringField("icap.page.url"))\
         .add_field(fields.StringField("icap.action.code"))\
         .add_field(fields.BigintField("icap.action.timeOffset"))\
         .add_field(fields.StringField("icap.action.message"))\
         .add_field(fields.StringField("icap.countryCode"))\
         .add_field(fields.StringField("userLangCode"))\
         .add_field(fields.StringField("userOs"))\
         .add_field(fields.StringField("userBrowser"))
            
      return messages_field_manager
      
   def assemble_messages_report(self, report_query_dict: dict) -> dict:

      messages_report_dict = {}

      dbms, db = self.get_default_dbms(), self.get_default_db()
      sql_builder = dbms.new_sql_builder(None)

      report_query_model = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))
      select_messages_where = report_query_model.assemble_where_expression(sql_builder)

      actions_topics_query = self.assemble_actions_topics_query()

      messages_report_query = self.get_default_dbms().new_select()\
         .set_field_manager(self.assemble_messages_field_manager())

      messages_report_query.subqueries.add(actions_topics_query)
      
      messages_report_query\
         .FROM((actions_topics_query.get_query_name(),))\
         .WHERE("(icap__action__message is not null) AND " + select_messages_where)
      
      for action_varname in self.get_action_varnames():
         messages_report_query.SELECT_field((action_varname,))
                  
      self.deb(messages_report_query.get_snippet())

      runner = dbms.new_query_runner(db)
      query_result = runner.execute_query(messages_report_query).get_query_result()
      if query_result is not None:
         messages_report_dict = {   
            "source_data_age_sec": self.get_source_data_age_sec(),
            "messages": query_result.dump_list_of_dicts()
         }
      runner.close()

      return messages_report_dict
   

   # Calculating quality summaries for specified groups whithin a specified scope

   def assemble_coeff_set_query(self) -> sql_select.Select:

      coeff_sets_query = self.get_default_dbms().new_select() \
         .FROM(("webstat__coeff_sets", self.get_default_db_scheme_name())) \
         .WHERE("is_active") \
         .SELECT_field(("*",))
      
      return coeff_sets_query
   
   def get_pagereads_expression(self) -> str:

      pagereads_expression = """
         CASE 
            WHEN icap__action__code='LOAD' THEN 1
            ELSE 0
         END
      """

      return pagereads_expression

   def get_joy_expression(self) -> str:

      joy_expression = """
         CASE 
            WHEN icap__action__code='LIKE' THEN
               CASE
                  WHEN icap__action__message is not null THEN dislike_with_message_score
                  ELSE dislike_score
               END
            ELSE 0
         END
      """

      return joy_expression

   def get_pain_expression(self) -> str:

      pain_expression = """
         CASE 
            WHEN icap__action__code='UNLOAD' THEN 
               CASE
                  WHEN icap__action__timeoffset < bounce_max_sec*1000 THEN bounce_score
                  WHEN icap__action__timeoffset > stuck_min_sec*1000 THEN stuck_score
                  ELSE 0
               END
            WHEN icap__action__code='DISLIKE' THEN
               CASE
                  WHEN icap__action__message is not null THEN dislike_with_message_score
                  ELSE dislike_score
               END
            ELSE 0
         END
      """

      return pain_expression

   def get_happy_readers_count(self) -> str:

      happy_readers_count = """
         CASE 
            WHEN icap__action__code='LIKE' THEN 1
            ELSE 0
         END
      """

      return happy_readers_count

   def get_unhappy_readers_count(self) -> str:

      unhappy_readers_count = """
         CASE 
            WHEN icap__action__code='UNLOAD' THEN 
               CASE
                  WHEN icap__action__timeoffset < bounce_max_sec*1000 THEN 1
                  WHEN icap__action__timeoffset > stuck_min_sec*1000 THEN 1
                  ELSE 0
               END
            WHEN icap__action__code='DISLIKE' THEN 1
            ELSE 0
         END
      """

      return unhappy_readers_count
   
   def assemble_scores_query(self, report_query_model, actions_topics_query, coeff_set_query) -> sql_select.Select:

      scores_query = self.get_default_dbms().new_select() 

      scores_query.subqueries \
         .add(actions_topics_query) \
         .add(coeff_set_query)
      
      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)

      select_scores_where = report_query_model.assemble_where_expression(sql_builder)

      scores_query \
         .FROM((actions_topics_query.get_query_name(),)) \
         .INNER_JOIN((coeff_set_query.get_query_name(),)) \
         .ON("true") \
         .WHERE(select_scores_where) \
         .SELECT_field(("*",)) \
         .SELECT_expression("pagereads", self.get_pagereads_expression()) \
         .SELECT_expression("happy_readers", self.get_happy_readers_count()) \
         .SELECT_expression("unhappy_readers", self.get_unhappy_readers_count()) \
         .SELECT_expression("joy", self.get_joy_expression()) \
         .SELECT_expression("pain", self.get_pain_expression())
      
      return scores_query

   def assemble_subtotals_query(self, report_query_model, scores_query) -> sql_select.Select:

      subtotals_query = self.get_default_dbms().new_select() 

      subtotals_query \
         .subqueries.add(scores_query)
      
      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)

      granularity = report_query_model.get_granularity()
      group_by_fields = granularity.assemble_group_by_list(sql_builder)
      group_by = granularity.assemble_group_by_list(sql_builder)

      subtotals = """, 
         sum(pagereads) AS group_pagereads, 
         sum(happy_readers) AS group_happy_readers, 
         sum(unhappy_readers) AS group_unhappy_readers, 
         sum(joy) AS group_joy, 
         sum(pain) AS group_pain
      """

      subtotals_query \
         .FROM((scores_query.get_query_name(),)) \
         .get_SELECT().set_snippet(group_by_fields + subtotals) 
         
      subtotals_query.GROUP_BY_expression(group_by)

      return subtotals_query
   
   def assemble_totals_query(self, pain_query) -> sql_select.Select:

      totals_query = self.get_default_dbms().new_select() 

      totals_query \
         .subqueries.add(pain_query)
      
      totals_query \
         .FROM((pain_query.get_query_name(),)) \
         .SELECT_expression("total_pagereads", "sum(pagereads)") \
         .SELECT_expression("total_joy", "sum(joy)") \
         .SELECT_expression("total_pain", "sum(pain)")
      
      return totals_query

   def assemble_summaries_field_manager(self, report_query_model) -> fields.FieldManager: 

      fm = fields.FieldManager()

      dimensions = report_query_model.get_granularity().get_dimensions()

      for dimension in dimensions:
         fm.add_field(fields.StringField(dimension.get_varname()))

      fm .add_field(fields.BigintField("pagereads")) \
         .add_field(fields.BigintField("group_happy_readers")) \
         .add_field(fields.BigintField("group_unhappy_readers")) \
         .add_field(fields.BigintField("group_joy")) \
         .add_field(fields.BigintField("group_pain")) \
         .add_field(fields.BigintField("total_pagereads")) \
         .add_field(fields.BigintField("total_joy")) \
         .add_field(fields.BigintField("total_pain")) \
         .add_field(fields.DoubleField("goodness")) \
         .add_field(fields.DoubleField("badness")) \
         .add_field(fields.DoubleField("joy_factor")) \
         .add_field(fields.DoubleField("pain_factor"))

      return fm
   
   def assemble_indicators_query(self, report_query_model, subtotals_query, totals_query) -> sql_select.Select:

      dbms = self.get_default_dbms()

      indicators_query = dbms.new_select()

      indicators_query.subqueries \
         .add(subtotals_query) \
         .add(totals_query) 
         
      sql_builder = dbms.new_sql_builder(None)

      indicators_query \
         .FROM((subtotals_query.get_query_name(),)) \
         .INNER_JOIN((totals_query.get_query_name(),)) \
         .ON("true") \
         .SELECT_field(("*",)) \
         .SELECT_expression("goodness", sql_builder.safediv("group_happy_readers", "group_pagereads")) \
         .SELECT_expression("badness", sql_builder.safediv("group_unhappy_readers", "group_pagereads")) \
         .SELECT_expression("joy_factor", sql_builder.safediv("group_joy", "total_joy")) \
         .SELECT_expression("pain_factor", sql_builder.safediv("group_pain", "total_pain"))
      
      indicators_query.set_field_manager(self.assemble_summaries_field_manager(report_query_model))
      
      return indicators_query

   def clean_summary(self, summary: dict) -> dict:

      summary.pop("group_happy_readers")
      summary.pop("group_unhappy_readers")
      summary.pop("group_joy")
      summary.pop("group_pain")
      summary.pop("total_pagereads")
      summary.pop("total_joy")
      summary.pop("total_pain")

      return summary

   def assemble_summaries_report(self, report_query_dict: dict) -> dict:

      summaries_report_dict = {}
      
      report_query_model = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))

      actions_topics_query = self.assemble_actions_topics_query()
      coeff_sets_query = self.assemble_coeff_set_query()  
      scores_query = self.assemble_scores_query(report_query_model, actions_topics_query, coeff_sets_query) 
      subtotals_query = self.assemble_subtotals_query(report_query_model, scores_query)    
      totals_query = self.assemble_totals_query(scores_query)
      indicators_query = self.assemble_indicators_query(report_query_model, subtotals_query, totals_query)

      dbms, db = self.get_default_dbms(), self.get_default_db()

      runner = dbms.new_query_runner(db)
      query_result = runner.execute_query(indicators_query).get_query_result()
      if query_result is not None:
         summaries_report_dict = {
            "source_data_age_sec": self.get_source_data_age_sec(),
            "summaries": [self.clean_summary(summary) for summary in query_result.dump_list_of_dicts()]
         }
      runner.close()
      
      return summaries_report_dict


   # Creating a breakdown based on audience characteristics within a specified scope. 

   def assemble_pagereads_query(self, report_query_model, actions_topics_query, field_name) -> sql_select.Select:

      pagereads_query = self.get_default_dbms().new_select() 

      pagereads_query.subqueries \
         .add(actions_topics_query) 
      
      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)

      select_where = report_query_model.assemble_where_expression(sql_builder)

      pagereads_query \
         .FROM((actions_topics_query.get_query_name(),)) \
         .WHERE(select_where) \
         .SELECT_expression("code", field_name) \
         .SELECT_expression("pagereads", self.get_pagereads_expression()) 
      
      return pagereads_query
   

   def assemble_total_pagereads_query(self, pagereads_query) -> sql_select.Select:

      total_pagereads_query = self.get_default_dbms().new_select() 

      total_pagereads_query \
         .subqueries.add(pagereads_query)
      
      total_pagereads_query \
         .FROM((pagereads_query.get_query_name(),)) \
         .SELECT_expression("total_pagereads", "sum(pagereads)::double precision")
      
      return total_pagereads_query
   
   def assemble_group_pagereads_query(self, report_query_model, pagereads_query, field_name) -> sql_select.Select:

      group_pagereads_query = self.get_default_dbms().new_select()

      group_pagereads_query.subqueries \
         .add(pagereads_query) 
      
      group_pagereads_query \
         .FROM((pagereads_query.get_query_name(),)) \
         .SELECT_field(("code", )) \
         .SELECT_expression("group_pagereads", "sum(pagereads)::double precision") \
         .GROUP_BY_expression("code")

      return group_pagereads_query

   def assemble_breakdown_field_manager(self) -> fields.FieldManager: 

      fm = fields.FieldManager() \
         .add_field(fields.StringField("code")) \
         .add_field(fields.DoubleField("share")) 

      return fm
   
   def assemble_partial_brakedown_query(self, report_query_model, field_name) -> sql_select.Select:

      breakdown_query = self.get_default_dbms().new_select()

      actions_topics_query = self.assemble_actions_topics_query()
      pagereads_query = self.assemble_pagereads_query(report_query_model, actions_topics_query, field_name)
      total_pagereads_query = self.assemble_total_pagereads_query(pagereads_query)
      group_pagereads_query = self.assemble_group_pagereads_query(report_query_model, pagereads_query, field_name)

      breakdown_query.subqueries \
         .add(total_pagereads_query) \
         .add(group_pagereads_query)
      
      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)
      
      breakdown_query \
         .FROM((total_pagereads_query.get_query_name(),)) \
         .INNER_JOIN((group_pagereads_query.get_query_name(),)) \
         .ON("true") \
         .SELECT_field(("code",)) \
         .SELECT_expression("share", sql_builder.safediv("group_pagereads", "total_pagereads"))
      
      breakdown_query.set_field_manager(self.assemble_breakdown_field_manager())

      return breakdown_query

   def run_partial_breakdown_query(self, report_query_model, field_name) -> list:

      brakedown_entries = []

      dbms, db = self.get_default_dbms(), self.get_default_db()

      partial_brakedown_query = self.assemble_partial_brakedown_query(report_query_model, field_name)

      runner = dbms.new_query_runner(db)
      query_result = runner.execute_query(partial_brakedown_query).get_query_result()
      if query_result is not None:
         brakedown_entries = [{"code": row["code"], "share": row["share"]} for row in query_result.dump_list_of_dicts()]

      runner.close()

      return brakedown_entries

   def assemble_breakdown_report(self, report_query_dict: dict) -> dict:

      report_query_model = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))

      breakdown_report_dict = {
         "source_data_age_sec": self.get_source_data_age_sec(),
         "countries": self.run_partial_breakdown_query(report_query_model, "icap__countrycode"),
         "userLangs": self.run_partial_breakdown_query(report_query_model, "userlangcode"),
         "oss": self.run_partial_breakdown_query(report_query_model, "useros"),
         "browsers": self.run_partial_breakdown_query(report_query_model, "userbrowser"),
         "locals": self.run_partial_breakdown_query(report_query_model, "icap__cms__doc__localcode")
      }
      
      return breakdown_report_dict
   

   # Performer's main

   def perform_task(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

      task_body = task.get_task_body()

      status_code = status.OK
      status_message = status.MSG_SUCCESS
      out_prolog = out_body = None

      if task.get_task_name() == "get_directories":
         out_body = self.assemble_directories_report(task_body)
      elif task.get_task_name() == "get_messages":
         out_body = self.assemble_messages_report(task_body)  
      elif task.get_task_name() == "get_quality_summaries":
         out_body = self.assemble_summaries_report(task_body)
      elif task.get_task_name() == "get_audience_breakdown":
         out_body = self.assemble_breakdown_report(task_body)
      else:
         status_code = status.ERR_UNKNOWN_TASK 
         status_message = status.MSG_UNKNOWN_TASK

      perf_out = perfoutput.PerformerOutput(self)\
         .set_performer_name(task.get_performer_name())\
         .set_task_name(task.get_task_name())\
         .set_status_code(status_code)\
         .set_status_message(status_message)\
         .set_prolog(out_prolog)\
         .set_body(out_body)
      
      return perf_out 

def new_reporter(shortcut: performer_shortcuts.PerformerShortcut) -> performers.Reporter:

   return WebstatReporter(shortcut.get_chief()).set_shortcut(shortcut)
