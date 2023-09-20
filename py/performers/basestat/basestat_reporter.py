# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  basestat_reporter.py                     (\(\
# Func:    Building basic statistical reports       (^.^)
# # ## ### ##### ######## ############# #####################

import sys
import os
import pathlib

sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 

from kernel import (
   utils, status, fields, dtos, performer_shortcuts, performers, 
   perftask, sql_select, perfoutput, grq_report_query
)

from debug import deb_reporter


class BasestatReporter(performers.Reporter):

   def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


   # Common queries

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
   

   def assemble_basestat_topics_query(self) -> sql_select.Select:

      arg_names = [
         "icap.cms.doc.uid", 
         "icap.cms.doc.localCode", 
         "icap.cms.doc.verno", 
         "icap.cms.topic.uid", 
         "icap.cms.topic.verno"
      ]
      
      out_names = self.get_taxonomy_varnames()

      src_desk = self.get_app().get_source_desk()
      basestat_topics_query = src_desk.assemble_measurements_query(arg_names, out_names)\
                              .set_query_name("topicmeta")

      return basestat_topics_query


   def assemble_basestat_actions_query(self) -> sql_select.Select:

      basestat_actions_query = self.get_default_dbms().new_select()

      basestat_actions_query\
         .FROM(("basestat__actions", self.get_default_db_scheme_name()))
      
      for varname in self.get_action_varnames():
         basestat_actions_query.SELECT_field((varname,))
         
      return basestat_actions_query
   

   # Grabbing directories

   def grab_directory(self, directory_field_name: str) -> list:

      dircodes = []

      dbms, db = self.get_default_dbms(), self.get_default_db()

      dircodes_field_manager = fields.FieldManager()\
         .add_field(fields.StringField(directory_field_name))
      
      dircodes_query = dbms.new_select()\
         .set_field_manager(dircodes_field_manager)
      
      dircodes_query\
         .FROM(("basestat__actions", self.get_default_db_scheme_name()))\
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
         "countries": self.grab_countries(),
         "browsers": self.grab_browsers(),
         "oss": self.grab_oss(),
         "user_langs": self.grab_user_langs(),
         "locals": self.grab_locals()
      }

      return directories_report_dict


   # Reporting messages

   def assemble_actions_topics_query(self) -> sql_select.Select:
        
      actions_query = self.assemble_basestat_actions_query().set_query_name("actions") 
      topics_query = self.assemble_basestat_topics_query().set_query_name("topics")

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
         messages_report_dict["messages"] = query_result.dump_list_of_dicts()
      runner.close()

      return messages_report_dict
   

   # Reporting summaries

   def assemble_coeff_set_query(self) -> sql_select.Select:

      coeff_sets_query = self.get_default_dbms().new_select() \
         .FROM(("basestat__coeff_sets", self.get_default_db_scheme_name())) \
         .WHERE("is_active") \
         .SELECT_field(("*",))
      
      return coeff_sets_query
   
   def assemble_pain_query(self, report_query_model, actions_topics_query, coeff_set_query) -> sql_select.Select:

      pain_query = self.get_default_dbms().new_select() 

      pain_query.subqueries \
         .add(actions_topics_query) \
         .add(coeff_set_query)
      
      calcpain = """
         CASE 
         WHEN icap__action__code='UNLOAD' THEN 
            CASE
            WHEN icap__action__timeoffset < bounce_max_sec*1000 THEN bounce_score
            WHEN icap__action__timeoffset > stuck_min_sec*1000 THEN stuck_score
            ELSE 0
            END
         WHEN icap__action__code='LIKE' THEN 0
         WHEN icap__action__code='DISLIKE' THEN
            CASE
            WHEN icap__action__message is not null THEN dislike_with_message_score
            ELSE dislike_score
            END
         ELSE 0
         END
      """

      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)

      select_pain_where = report_query_model.assemble_where_expression(sql_builder)

      pain_query \
         .FROM((actions_topics_query.get_query_name(),)) \
         .INNER_JOIN((coeff_set_query.get_query_name(),)) \
         .ON("true") \
         .WHERE(select_pain_where) \
         .SELECT_field(("*",)) \
         .SELECT_expression("pain", calcpain)
      
      return pain_query

   def assemble_group_pain_query(self, report_query_model, pain_query) -> sql_select.Select:

      group_pain_query = self.get_default_dbms().new_select() 

      group_pain_query \
         .subqueries.add(pain_query)
      
      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)

      granularity = report_query_model.get_granularity()
      group_by_fields = granularity.assemble_group_by_list(sql_builder)
      group_by = granularity.assemble_group_by_list(sql_builder)

      group_pain_query \
         .FROM((pain_query.get_query_name(),)) \
         .get_SELECT().set_snippet(group_by_fields + ", sum(pain) AS group_pain") 
         
      group_pain_query.GROUP_BY_expression(group_by)

      return group_pain_query
   
   def assemble_total_pain_query(self, pain_query) -> sql_select.Select:

      total_pain_query = self.get_default_dbms().new_select() 

      total_pain_query \
            .subqueries.add(pain_query)
      
      total_pain_query \
         .FROM((pain_query.get_query_name(),)) \
         .SELECT_expression("total_pain", "sum(pain)")
      
      return total_pain_query

   def assemble_pain_factor_query(self, group_pain_query, total_pain_query) -> sql_select.Select:

      pain_factor_query = self.get_default_dbms().new_select()

      pain_factor_query.subqueries \
         .add(group_pain_query) \
         .add(total_pain_query) 
         
      pain_factor_query \
         .FROM((group_pain_query.get_query_name(),)) \
         .INNER_JOIN((total_pain_query.get_query_name(),)) \
         .ON("true") \
         .SELECT_field(("*",)) \
         .SELECT_expression("pain_factor", "group_pain/total_pain")
      
      return pain_factor_query

   def assemble_summaries_report(self, report_query_dict: dict) -> dict:

      report_dict = {}
      
      report_query_model = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))

      actions_topics_query = self.assemble_actions_topics_query()
      coeff_sets_query = self.assemble_coeff_set_query()      
      pain_query = self.assemble_pain_query(report_query_model, actions_topics_query, coeff_sets_query)  
      group_pain_query = self.assemble_group_pain_query(report_query_model, pain_query)    
      total_pain_query = self.assemble_total_pain_query(pain_query)
      pain_factor_query = self.assemble_pain_factor_query(group_pain_query, total_pain_query)
      
      print(pain_factor_query.get_snippet())

      
      report_dict = report_query_dict

      return report_dict


   # Performer's main

   def perform_task(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

      task_body = task.get_task_body()

      status_code = status.OK
      status_message = status.MSG_SUCCESS
      out_prolog = out_body = None

      if task.get_task_name() == "directories":
         out_body = self.assemble_directories_report(task_body)
      elif task.get_task_name() == "messages":
         out_body = self.assemble_messages_report(task_body)  
      elif task.get_task_name() == "summaries":
         out_body = self.assemble_summaries_report(task_body)
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

   return BasestatReporter(shortcut.get_chief()).set_shortcut(shortcut)
