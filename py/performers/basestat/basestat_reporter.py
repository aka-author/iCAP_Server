# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  basestat_reporter.py                     (\(\
# Func:    Building basic statistical reports       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 
from kernel import status, fields, dtos, performer_shortcuts, performers, perftask, \
                     sql_select, perfoutput, grq_report_query
from debug import deb_reporter


class BasestatReporter(performers.Reporter):

   def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


   # Selecting taxonomy

   def get_taxonomy_varnames(self) -> List:

      dir_desk = self.get_app().get_directory_desk()
      
      taxonomy_varnames = \
         [varname for varname in dir_desk.get_varnames() if ".taxonomy." in varname]

      return taxonomy_varnames


   def assemble_topic_taxonomy_query(self) -> sql_select.Select:

      arg_names = ["icap.cms.doc.uid", "icap.cms.doc.localCode", "icap.cms.doc.verno", 
                   "icap.cms.topic.uid", "icap.cms.topic.verno"]
      
      out_names = self.get_taxonomy_varnames()

      src_desk = self.get_app().get_source_desk()
      topic_taxonomy_query = src_desk.assemble_measurements_query(arg_names, out_names)

      return topic_taxonomy_query


   # Reporting summaries

   def assemble_summaries_report(self, report_query_dict: Dict) -> Dict:

      report_dict = {}

      rq = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))

      print("!!!", rq.granularity.dimensions[0])

      #self.get_default_dbms().new_select()


      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)

      print(rq.assemble_select_fields(sql_builder))

      report_dict = report_query_dict

      return report_dict


   # Reporting messages

   def assemble_messages_query(self) -> sql_select.Select:
        
      source_desk = self.get_app().get_source_desk()

      topic_pageread_query = source_desk.assemble_measurements_query(
         ["icap.pagereadId"],
         ["icap.cms.doc.uid", "icap.cms.doc.localCode", "icap.cms.doc.verno", 
          "icap.cms.topic.uid", "icap.cms.topic.verno"])

      reader_action_query = source_desk.assemble_measurements_query(\
         ["icap.pagereadId", "icap.action.code", "icap.action.timeOffset"],
         ["icap.action.message"])

      messages_query = self.get_default_dbms().new_select()

      messages_query.subqueries\
         .add(topic_pageread_query)\
         .add(reader_action_query)
        
      messages_query\
         .FROM((topic_pageread_query.get_query_name(),))\
         .INNER_JOIN((reader_action_query.get_query_name(),))\
         .ON("{0}={1}", ("icap.pagereadId", 0), ("icap.pagereadId", 1))\
         .SELECT_field(("accepted_at", 0))\
         .SELECT_field(("icap.pagereadId", 0))\
         .SELECT_field(("icap.cms.doc.uid", 0))\
         .SELECT_field(("icap.cms.doc.localCode", 0))\
         .SELECT_field(("icap.cms.doc.verno", 0))\
         .SELECT_field(("icap.cms.topic.uid", 0))\
         .SELECT_field(("icap.cms.topic.verno", 0))\
         .SELECT_field(("icap.action.code", 1))\
         .SELECT_field(("icap.action.message", 1))
      
      topic_taxonomy_query = self.assemble_topic_taxonomy_query()

      messages_taxonomy_query = self.get_default_dbms().new_select()

      messages_taxonomy_query.subqueries\
         .add(messages_query)\
         .add(topic_taxonomy_query)

      messages_taxonomy_query\
         .FROM((messages_query.get_query_name(),))\
         .LEFT_JOIN((topic_taxonomy_query.get_query_name(),))\
         .ON("{0}={1} AND {2}={3} AND {4}={5} AND {6}={7} AND {8}={9}", 
             ("icap.cms.doc.uid", 0), ("icap.cms.doc.uid", 1),
             ("icap.cms.doc.localCode", 0), ("icap.cms.doc.localCode", 1), 
             ("icap.cms.doc.verno", 0), ("icap.cms.doc.verno", 1),
             ("icap.cms.topic.uid", 0), ("icap.cms.topic.uid", 1),
             ("icap.cms.topic.verno", 0), ("icap.cms.topic.verno", 1))\
         .SELECT_field(("accepted_at", 0))\
         .SELECT_field(("icap.pagereadId", 0))\
         .SELECT_field(("icap.cms.doc.uid", 0))\
         .SELECT_field(("icap.cms.doc.localCode", 0))\
         .SELECT_field(("icap.cms.doc.verno", 0))\
         .SELECT_field(("icap.cms.topic.uid", 0))\
         .SELECT_field(("icap.cms.topic.verno", 0))\
         .SELECT_field(("icap.action.code", 0))\
         .SELECT_field(("icap.action.message", 0))
      
      for taxonomy_varname in self.get_taxonomy_varnames():
         messages_taxonomy_query.SELECT_field((taxonomy_varname, 1))

      return messages_taxonomy_query 


   def assemble_messages_field_manager(self) -> fields.FieldKeeper():

      messages_field_manager = fields.FieldManager()\
            .add_field(fields.TimestampField("accepted_at"))\
            .add_field(fields.StringField("icap.cms.doc.uid"))\
            .add_field(fields.StringField("icap.cms.doc.localCode"))\
            .add_field(fields.StringField("icap.cms.doc.verno"))\
            .add_field(fields.StringField("icap.cms.topic.uid"))\
            .add_field(fields.StringField("icap.cms.topic.verno"))\
            .add_field(fields.StringField("icap.action.code"))\
            .add_field(fields.StringField("icap.action.message"))
      
      return messages_field_manager
      

   def assemble_messages_report(self, report_query_dict: Dict) -> Dict:

      # print(self.assemble_topic_taxonomy_query().get_snippet())

      messages_report_dict = {}

      dbms, db = self.get_default_dbms(), self.get_default_db()
      sql_builder = dbms.new_sql_builder(None)

      report_query_model = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))
      select_messages_where = report_query_model.assemble_where_expression(sql_builder)

      messages_query = self.assemble_messages_query()

      messages_report_query = self.get_default_dbms().new_select()\
         .set_field_manager(self.assemble_messages_field_manager())

      messages_report_query.subqueries.add(messages_query)
      
      messages_report_query\
         .FROM((messages_query.get_query_name(),))\
            .WHERE(select_messages_where)\
            .SELECT_field(("accepted_at",))\
            .SELECT_field(("icap.cms.doc.uid",))\
            .SELECT_field(("icap.cms.doc.localCode",))\
            .SELECT_field(("icap.cms.doc.verno",))\
            .SELECT_field(("icap.cms.topic.uid",))\
            .SELECT_field(("icap.cms.topic.verno",))\
            .SELECT_field(("icap.action.code",))\
            .SELECT_field(("icap.action.message",))

      self.deb(messages_report_query.get_snippet())

      runner = dbms.new_query_runner(db)
      query_result = runner.execute_query(messages_report_query).get_query_result()
      messages_report_dict["messages"] = query_result.dump_list_of_dicts()
      runner.close()

      return messages_report_dict


   # Performer's main

   def perform_task(self, task: perftask.PerformerTask) -> perfoutput.PerformerOutput:

      task_body = task.get_task_body()

      status_code = status.OK
      status_message = status.MSG_SUCCESS
      out_prolog = out_body = None
      
      if task.get_task_name() == "summaries":
         out_body = self.assemble_summaries_report(task_body)      
      elif task.get_task_name() == "messages":
         out_body = self.assemble_messages_report(task_body)  
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