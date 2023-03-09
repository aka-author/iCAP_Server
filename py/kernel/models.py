# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  models.py                                  
# Func:    Processing subject area entities         (\(\     
# Usage:   Define your models based on Model        (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import dtos, workers, fields
import db_instances, sql_scripts, sql_queries, sql_insert, sql_update, query_results


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


    # Working with a DTO

    def import_field_value_from_dto(self, varname: str, native_value: any) -> 'Model':

        self.fm.set_field_value(varname, native_value)

        return self


    def import_submodels_from_dto(self, dto: object) -> 'Model':

        return self


    def import_dto(self, dto: dtos.Dto) -> 'Model':

        for varname in self.fm.get_varnames():
            self.import_field_value_from_dto(varname, dto.get(varname))

        self.import_submodels_from_dto(dto)

        return self


    def export_field_value_for_dto(self, varname: str) -> any:

        return self.fm.get_field_value(varname)


    def export_submodels_to_dto(self, dto: object) -> 'Model':

        return self


    def export_dto(self) -> dtos.Dto:

        dto = dtos.Dto()

        for varname in self.fm.get_varnames():
            dto.set_prop_value(self.export_field_value_for_dto(varname))

        self.export_submodels_to_dto(dto)

        return dto


    # Working with a database

    def get_db_scheme_name(self) -> str:

        return self.get_cfg().get_default_db_scheme_name()
    

    # Loading models from a database

    def create_instances_of_query_result(self, query_result: query_results.QueryResult) -> List:

        instances = []

        fm = query_result.get_field_manager()

        while not query_result.fetch_one().eof():

            instance = type(self)(self.get_chief()) \
                        if query_result.current_row_index() < query_result.count_rows() \
                        else self
            
            instances.append(instance.set_field_values_from_field_manager(fm))

        return instances


    def get_load_query(self, db: db_instances.Db, target_varname: str=None, target_value: any=None) -> sql_queries.SelectiveQuery:

        load_query = db.get_dbms().new_select()\
            .build_of_field_manager(\
                self.get_field_manager(), self.get_plural(), self.get_db_scheme_name(), \
                "{0}={1}", (target_varname, 0), target_value)     
    
        return load_query


    def load_all_siblings(self, db: db_instances.Db, parent_id_varname: str=None, parent_id: any=None) -> List:

        runner = db.get_dbms().new_query_runner()

        load_all_siblings_query = self.get_load_query(db, parent_id_varname, parent_id)

        query_result = runner.execute_query(load_all_siblings_query).get_query_result()

        runner.close()

        return self.create_instances_of_query_result(query_result)


    def load_submodels(self, db: db_instances.Db) -> 'Model':

        # my_uuid = self.get_field_value("uuid")
        # self.Cows = Cow(self).load_all_siblings(db, "farm_uuid", my_uuid)
        # self.Hens = Hen(self).load_all_siblings(db, "farm_uuid", my_uuid)
        
        return self


    def load(self, db: db_instances.Db, target_varname: str, target_value: any) -> 'Model':

        runner = db.get_dbms().new_query_runner()

        load_query = self.get_load_query(db, target_varname, target_value)

        runner.execute_query(load_query).fetch_one().close()

        self.load_submodels(db)

        return self


    def get_load_all_query(self, db: db_instances.Db) -> sql_queries.SelectiveQuery:
    
        load_all_query = db.get_dbms().new_select()\
            .build_dump(self.get_field_keeper(), \
                        self.get_plural(), \
                        self.get_db_scheme_name())
    
        return load_all_query


    def load_all(self, db: db_instances.Db) -> List:

        runner = db.get_dbms().new_query_runner(db)

        load_all_query = self.get_load_all_query(db)

        query_result = runner.execute_query(load_all_query).get_query_result()

        instances = self.create_instances_of_query_result(query_result)

        runner.close()

        return instances
        

    # Inserting/updating models to/in a database

    def get_insert_query(self, db: db_instances.Db) -> sql_insert.Insert:

        return db.get_dbms().new_insert().build_of_field_manager(self.get_field_manager())


    def get_update_query(self, db: db_instances.Db) -> sql_update.Update:

        return db.get_dbms().new_update().build_of_field_manager(self.get_field_manager()) 


    def get_save_query(self, db: db_instances.Db, options: Dict) -> sql_queries.Query: 

        if options["mode"] == "insert":
            save_query = self.get_insert_query(self, db)
        elif options["mode"] == "update":
            return self.get_update_query(self, db)
        
        return save_query


    def get_submodel_save_queries(self, options: Dict) -> List:

        return []


    def get_save_script(self, db: db_instances.Db, options: Dict) -> sql_scripts.Script:

        save_script = db.get_dbms().new_script().add(self.get_save_query(db, options))

        for save_query in self.get_submodel_save_queries(db, options): 
            save_script.add(save_query)

        return save_script


    def save(self, db: db_instances.Db, options: Dict) -> 'Model':
        
        query_runner = db.get_dbms().new_query_runner()

        save_script = self.get_save_script(db, options)

        query_runner.execute_script(save_script).commit().close()

        return self
    

    def insert(self, db):

        return self.save(db, {"mode": "insert"})
    

    def update(self, db):

        return self.save(db, {"mode": "update"})


    # Debugging

    def __str__(self):

        return "\n".join([varname + ": " + str(self.fm.get_serialized_field_value(varname)) \
                            for varname in self.fm.get_varnames()])

            
            