# # ## ### ##### ######## ############# #####################
# Product:  iCAP platform
# Layer:    Kernel
# Module:   measurements.py                            (\(\
# Func:     Managing measurements and variable values  (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import uuid
import utils, dtos, workers, fields, models, variables


class VarValue(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("varvalue")


    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
            .add_field(fields.UuidField("uuid"), "autoins")\
            .add_field(fields.UuidField("measurement_uuid"))\
            .add_field(fields.UuidField("variable_uuid"))\
            .add_field(fields.StringField("varname"))\
            .add_field(fields.StringField("partition"))\
            .add_field(fields.StringField("parsable_value"), "autoins")\
            .add_field(fields.StringField("serialized_value"))


    def get_varname(self):

        return self.get_field_value("varname")
 

    def get_variable(self) -> variables.Variable:

        return self.get_app().get_directory_desk().get_variable_by_name(self.get_varname())
    

    def get_parsable_value(self):

        return self.get_field_value("parsable_value")
    

    def get_serialized_value(self) -> str:

        return self.get_field_value("serialized_value")


    def rebuild(self, measurement: 'Measurement', partition: str) -> 'VarValue':

        variable_uuid = self.get_variable().get_uuid()
        serialized_value = str(self.get_field_value("parsable_value"))

        self.set_field_value("measurement_uuid", measurement.get_uuid())\
            .set_field_value("variable_uuid", variable_uuid)\
            .set_field_value("partition", partition)\
            .set_field_value("serialized_value", serialized_value)
        
        return self
    

    def is_valid(self) -> bool: 

        return self.get_app().get_directory_desk().check_varname(self.get_varname())



def assemble_argprof(shortcuts: List) -> str:

    shortcuts.sort()

    return "+".join(shortcuts)


class Measurement(models.Model):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.set_model_name("measurement")
        
        self.args = []
        self.outs = []

        self.varvals_by_names = {} 
        

    def define_fields(self) -> models.Model:
        
        self.get_field_manager()\
            .add_field(fields.StringField("id"), "autoins")\
            .add_field(fields.UuidField("uuid"))\
            .add_field(fields.TimestampTzField("accepted_at"))\
            .add_field(fields.UuidField("sensor_uuid"))\
            .add_field(fields.StringField("sensor_id"))\
            .add_field(fields.StringField("argprof"))\
            .add_field(fields.StringField("outprof"))\
            .add_field(fields.StringField("hashkey"))
            

    def get_uuid(self):

        return self.get_field_value("uuid")


    def get_accepted_at(self):

        return self.get_field_value("accepted_at")


    def get_sensor_id(self):

        return self.get_field_value("sensor_id")


    def get_sensor_uuid(self):

        dd = self.get_app().get_directory_desk()

        s = dd.get_sensor_by_id(self.get_sensor_id())

        return s.get_uuid() if s is not None else None

    
    def get_parsable_value(self, varname):

        return self.varvals_by_names[varname].get_parsable_value()
    

    def get_argprof(self) -> str:

        dd = self.get_app().get_directory_desk()

        arg_names = [arg.get_varname() for arg in self.args]
        arg_shortcuts = [dd.get_variable_by_name(arg_name).get_shortcut() for arg_name in arg_names]
        arg_shortcuts.sort()

        return assemble_argprof(arg_shortcuts)
                

    def get_outprof(self) -> str:

        dd = self.get_app().get_directory_desk()

        out_names = [out.get_varname() for out in self.outs]
        out_names.sort()

        return "+".join([dd.get_variable_by_name(out_name).get_shortcut() for out_name in out_names])                


    def get_hashkey(self):

        arg_names = [arg.get_varname() for arg in self.args]
        arg_names.sort()

        return "+".join([str(self.varvals_by_names[arg_name].get_parsable_value()).replace("+", "++") for arg_name in arg_names])


    def count_args(self):

        return len(self.args)


    def count_outs(self):

        return len(self.outs)


    def import_submodels_from_dto(self, dto: dtos.Dto) -> models.Model:

        for arg_varval_dict in dto.get_prop_value("args"):
            self.args.append(VarValue(self).import_dto(dtos.Dto(arg_varval_dict)))

        for out_varval_dict in dto.get_prop_value("outs"):
            self.outs.append(VarValue(self).import_dto(dtos.Dto(out_varval_dict)))

        for varvalue in self.args + self.outs:
            self.varvals_by_names[varvalue.get_varname()] = varvalue

        return self
    

    def rebuild(self) -> 'Measurement':

        self.set_field_value("uuid", uuid.uuid4())\
            .set_field_value("sensor_uuid", self.get_sensor_uuid())\
            .set_field_value("argprof", self.get_argprof())\
            .set_field_value("outprof", self.get_outprof())\
            .set_field_value("hashkey", self.get_hashkey())

        for varvalue in self.args:
            varvalue.rebuild(self, "ARG")

        for varvalue in self.outs:
            varvalue.rebuild(self, "OUT")

        return self


    def get_insert_submodel_queries(self) -> List:

        insert_subodel_queries = []

        for arg_varval in self.args + self.outs:
            insert_subodel_queries.append(arg_varval.get_insert_query())

        return insert_subodel_queries


    def is_valid(self): 

        valid_flag = self.get_accepted_at() is not None \
                 and self.get_sensor_id() is not None \
                 and self.count_args() > 0 

        if valid_flag:

            for v in self.args + self.outs:
                valid_flag = v.is_valid()
                if not valid_flag: break

        return valid_flag    


    def is_unique(self) -> bool:

        dbms, db = self.get_default_dbms(), self.get_default_db()        

        db_table_name = self.get_plural()
        db_scheme_name = self.get_default_db_scheme_name()

        runner = dbms.new_query_runner(db)

        count_query = dbms.new_select()\
            .FROM((db_table_name, db_scheme_name))\
            .WHERE("{0}={1} AND {2}={3} AND {4}={5}", 
                   ("argprof", 0), self.get_argprof(),
                   ("outprof", 0), self.get_outprof(),
                   ("hashkey", 0), self.get_hashkey())\
            .SELECT_expression("count_valid", "count(*)")
        
        runner.execute_query(count_query)

        if runner.isOK():
            count_result = runner.get_query_result().fetch_one()
            runner.close()
        else:
            raise Exception("Database error")
        
        return count_result.fm.get_field_value("count_valid") == 0