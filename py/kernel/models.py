# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  models.py                                  
# Func:    Processing subject area entities         (\(\     
# Usage:   Define your models based on Model        (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import status, dtos, workers, fields
import query_runners, sql_scripts, sql_queries, sql_insert, sql_update, query_results


class Model(workers.Worker):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.model_name = "model"
        self.plural = None

        self.fk = self.create_field_keeper()
        self.fm = self.create_field_manager()
        self.define_fields()
        self.fm.reset_field_values()


    def set_model_name(self, model_name: str) -> 'Model':

        self.model_name = model_name

        return self


    def get_model_name(self) -> str:

        return self.model_name

    
    def set_plural(self, plural: str=None) -> 'Model':

        if plural is None:
            last_letter = self.model_name[len(self.model_name) - 1]
            self.plural = self.model_name + ("es" if last_letter in ["s", "z"] else "s")
        else:
            self.plural = plural

        return self


    def get_plural(self) -> str:

        if self.plural is None:
            self.set_plural()

        return self.plural
    

    def create_field_keeper(self) -> fields.FieldKeeper:

        return fields.FieldKeeper()
    

    def define_fields(self) -> 'Model':

        return self
    

    def get_field_keeper(self) -> fields.FieldKeeper:

        return self.fk


    def create_field_manager(self) -> fields.FieldManager:

        return fields.FieldManager(self.fk)


    def get_field_manager(self) -> fields.FieldManager:

        return self.fm
    
    
    def set_field_value(self, field_name: str, field_value: any) -> 'Model':

        self.get_field_manager().set_field_value(field_name, field_value)

        return self
    

    def set_field_values_from_field_manager(self, fm: fields.FieldManager) -> 'Model':

        self.get_field_manager().set_field_values_from_field_manager(fm)

        return self


    def get_field_value(self, field_name: str) -> any:

        return self.get_field_manager().get_field_value(field_name)


    def is_valid(self) -> bool:

        return True


    # Importing and exporting a DTO

    def import_field_value_from_dto(self, varname: str, native_value: any) -> 'Model':

        self.fm.set_field_value(varname, native_value)

        return self


    def import_submodels_from_dto(self, dto: dtos.Dto) -> 'Model':

        return self


    def import_dto(self, dto: dtos.Dto) -> 'Model':

        for varname in self.fm.get_varnames():
            self.import_field_value_from_dto(varname, dto.get_prop_value(varname))

        self.import_submodels_from_dto(dto)

        return self


    def export_field_value_for_dto(self, varname: str) -> any:

        return self.fm.get_field_value(varname)


    def export_submodels_to_dto(self, dto: object) -> 'Model':

        return self


    def set_export_dto_filter(self, dto: dtos.Dto) -> 'Model':

        return self


    def export_dto(self) -> dtos.Dto:

        dto = dtos.Dto()

        self.set_export_dto_filter(dto)

        for varname in self.fm.get_varnames():
            dto.set_prop_value(varname, self.export_field_value_for_dto(varname))

        self.export_submodels_to_dto(dto)

        return dto
    

    # Loading instances of a model from a database

    def create_instances_of_query_result(self, query_result: query_results.QueryResult) -> List:

        instances = []

        fm = query_result.get_field_manager()

        while not query_result.fetch_one().eof():

            instance = type(self)(self.get_chief()) \
                        if query_result.current_row_index() < query_result.count_rows() \
                        else self
            
            instances.append(instance.set_field_values_from_field_manager(fm))

        return instances


    def get_load_query(self, target_varname: str, target_value: any) -> sql_queries.SelectiveQuery:

        instance_fm = self.get_field_manager()
        model_table_name = self.get_plural()
        db_scheme_name = self.get_default_db_scheme_name()

        load_query = self.get_default_dbms().new_select()
                        
        load_query.build_of_field_manager(\
                    instance_fm, model_table_name, db_scheme_name, \
                    "{0}={1}", (target_varname, 0), target_value)     
    
        return load_query


    def load_all_siblings(self, parent_id_varname: str, parent_id: any) -> List:

        dbms, db = self.get_default_dbms(), self.get_default_db()

        runner = dbms.new_query_runner(db)

        load_all_siblings_query = self.get_load_query(parent_id_varname, parent_id)

        query_result = runner.execute_query(load_all_siblings_query).get_query_result()

        runner.close()

        return self.create_instances_of_query_result(query_result)


    def load_submodels(self) -> 'Model':

        # my_uuid = self.get_field_value("uuid")
        # self.Cows = Cow(self).load_all_siblings("farm_uuid", my_uuid)
        # self.Hens = Hen(self).load_all_siblings("farm_uuid", my_uuid)
        
        return self


    def load(self, target_varname: str, target_value: any) -> 'Model':

        dbms, db = self.get_default_dbms(), self.get_default_db()

        runner = dbms.new_query_runner(db)

        load_query = self.get_load_query(target_varname, target_value)

        runner.execute_query(load_query).get_query_result().fetch_one()

        runner.close()
        
        self.load_submodels()

        return self


    def get_load_all_query(self) -> sql_queries.SelectiveQuery:

        load_all_query = self.get_default_dbms().new_select()

        model_fk = self.get_field_keeper()
        model_table_name = self.get_plural()
        db_scheme_name = self.get_default_db_scheme_name()
    
        load_all_query.build_dump(model_fk, model_table_name, db_scheme_name)
                        
        return load_all_query


    def load_all(self) -> List:

        dbms, db = self.get_default_dbms(), self.get_default_db()

        runner = dbms.new_query_runner(db)

        load_all_query = self.get_load_all_query()

        if runner.execute_query(load_all_query).isOK():
            query_result = runner.get_query_result()
            model_instances = self.create_instances_of_query_result(query_result)
            runner.close()
        else:
            raise Exception(status.MSG_DATABASE_ERROR)

        return model_instances
        

    # Inserting an instance of a model

    def get_insert_query(self) -> sql_insert.Insert:

        insert_query = self.get_default_dbms().new_insert()

        instance_fm = self.get_field_manager()
        model_table_name = self.get_plural()
        db_scheme_name = self.get_default_db_scheme_name()

        insert_query.build_of_field_manager(instance_fm, model_table_name, db_scheme_name)

        return insert_query


    def get_insert_submodel_queries(self) -> List:

        return []
    

    def get_insert_script(self) -> sql_scripts.Script:

        insert_script = self.get_default_dbms().new_script()
        
        insert_script.add_query(self.get_insert_query())

        for insert_submodel_query in self.get_insert_submodel_queries(): 
            insert_script.add_query(insert_submodel_query)

        return insert_script
    

    def insert(self, chief_query_runner: query_runners.QueryRunner=None) -> 'Model':

        query_runner = chief_query_runner if chief_query_runner is not None \
            else self.get_default_dbms().new_query_runner(self.get_default_db())

        query_runner.execute_script(self.get_insert_script())

        print(self.get_insert_script().get_snippet())

        if chief_query_runner is None:
            query_runner.commit().close()

        return self
    

    # Updating an instance of a model

    def get_update_query(self) -> sql_update.Update:

        update_query = self.get_default_dbms().new_update()

        instance_fm = self.get_field_manager()
        model_table_name = self.get_plural()
        db_scheme_name = self.get_default_db_scheme_name()

        update_query.build_of_field_manager(instance_fm, model_table_name, db_scheme_name)

        return update_query


    def get_update_submodel_queries(self) -> List:

        return []
    

    def get_update_script(self) -> sql_scripts.Script:

        update_script = self.get_default_dbms().new_script()
        
        update_script.add_query(self.get_update_query())

        for update_submodel_query in self.get_update_submodel_queries(): 
            update_script.add(update_submodel_query)

        return update_script


    def update(self, chief_query_runner: query_runners.QueryRunner=None) -> 'Model':

        query_runner = chief_query_runner if chief_query_runner is not None \
            else self.get_default_dbms().new_query_runner(self.get_default_db())

        query_runner.execute_script(self.get_update_script())

        if chief_query_runner is None:
            query_runner.commit().close()

        return self
    

    # Debugging

    def __str__(self):

        return "\n".join([varname + ": " + str(self.fm.get_serialized_field_value(varname)) \
                            for varname in self.fm.get_varnames()])