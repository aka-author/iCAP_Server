# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  basestat_reporter.py                     (\(\
# Func:    Building basic statistical reports       (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict
import sys, os, pathlib
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.parent.absolute()))) 
from kernel import status, dtos, performer_shortcuts, performers, perftask, \
                     sql_select, perfoutput, grq_report_query
from debug import deb_reporter


class BasestatReporter(performers.Reporter):

   def __init__(self, chief):

      super().__init__(chief)

      self.report_ver = 2


   def assemble_summaries_report(self, report_query_dict: Dict) -> Dict:

      report_dict = {}

      rq = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))

      print("!!!", rq.granularity.dimensions[0])

      #self.get_default_dbms().new_select()


      sql_builder = self.get_app().get_default_dbms().new_sql_builder(None)

      print(rq.assemble_select_fields(sql_builder))

      report_dict = report_query_dict

      return report_dict


   def assemble_messages_query(self) -> sql_select.Select:
        
        sd = self.get_app().get_source_desk()

        topic_pageread_query = sd.assemble_measurements_query(
            ["icap.pagereadId"],
            ["icap.cms.doc.uid", 
             "icap.cms.doc.verno", 
             "icap.cms.topic.uid", 
             "icap.cms.topic.verno"])

        reader_action_query = sd.assemble_measurements_query(\
            ["icap.pagereadId", 
             "icap.action.code", 
             "icap.action.timeOffset"],
            ["icap.action.message"])

        combo_query = self.get_default_dbms().new_select()

        combo_query.subqueries\
            .add(topic_pageread_query)\
            .add(reader_action_query)
        
        combo_query\
            .FROM((topic_pageread_query.get_query_name(),))\
            .INNER_JOIN((reader_action_query.get_query_name(),))\
            .ON("{0}={1}", ("icap.pagereadId", 0), ("icap.pagereadId", 1))\
            .SELECT_field(("accepted_at", 0))\
            .SELECT_field(("icap.pagereadId", 0))\
            .SELECT_field(("icap.cms.doc.uid", 0))\
            .SELECT_field(("icap.cms.doc.verno", 0))\
            .SELECT_field(("icap.cms.topic.uid", 0))\
            .SELECT_field(("icap.cms.topic.verno", 0))\
            .SELECT_field(("icap.action.code", 1))\
            .SELECT_field(("icap__action__message", 1))

        return combo_query 


   def assemble_messages_report(self, report_query_dict: Dict) -> Dict:

      report_dict = {}

      dbms, db = self.get_default_dbms(), self.get_default_db()
      sql_builder = dbms.new_sql_builder(None)

      report_query_model = grq_report_query.ReportQuery(self).import_dto(dtos.Dto(report_query_dict))
      select_messages_where = report_query_model.assemble_where_expression(sql_builder)

      
      runner = dbms.new_query_runner(db)

      messages_measurements_query = self.assemble_messages_query()

      messages_query = self.get_default_dbms().new_select()

      messages_query.subqueries.add(messages_measurements_query)
      
      messages_query\
         .FROM((messages_measurements_query.get_query_name(),))\
            .WHERE(select_messages_where)\
            .SELECT_field(("accepted_at",))\
            .SELECT_field(("icap.cms.doc.uid",))\
            .SELECT_field(("icap.cms.doc.verno",))\
            .SELECT_field(("icap.cms.topic.uid",))\
            .SELECT_field(("icap.cms.topic.verno",))\
            .SELECT_field(("icap__action__code",))\
            .SELECT_field(("icap__action__message",))

      print(messages_query.get_snippet())

      # query_result = runner.execute_query(messages_query).get_query_result()

      # runner.close()

      return report_dict


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