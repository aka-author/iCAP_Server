# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  models.py                                  
# Func:    Processing subject area entities         (\(\     
# Usage:   The class is abstract                    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List
import dtos, workers, fields
import db_instances, sql_scripts, sql_queries


class Model(workers.Worker):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.model_name = "model"

        self.fk = self.create_field_keeper().set_recordset_name("models")
        self.fm = self.create_field_manager(self.fk)
        self.define_fields()
        self.fm.reset_field_values()


    def set_model_name(self, model_name: str) -> 'Model':

        self.model_name = model_name

        self.get_field_keeper().set_recordset_name(self.get_plural())

        return self


    def get_model_name(self) -> str:

        return self.model_name

    
    def set_plural(self, plural: str=None) -> 'Model':

        if plural is None:
            last_letter = self.model_name[len(self.model_name) - 1]
            self.plural = self.model_name + ("es" if last_letter in ["s", "z"] else "s")
        else:
            self.plural = plural

        self.fm.set_recordset_name(self.plural)

        return self


    def get_plural(self) -> str:

        return self.plural
    

    def create_field_keeper(self) -> fields.FieldKeeper:

        return fields.FieldKeeper()
    

    def get_field_keeper(self) -> fields.FieldKeeper:

        return self.get_field_manager().get_field_keeper()


    def create_field_manager(self) -> fields.FieldManager:

        return fields.FieldManager(self)


    def get_field_manager(self) -> fields.FieldManager:

        return self.fm
    

    def set_field_values_from_field_manager(self, fm: fields.FieldManager) -> 'Model':

        self.get_field_manager().set_field_values_from_field_manager(fm)

        return self


    def is_valid(self) -> bool:

        return True


    # Working with a DTO

    def import_field_value_from_dto(self, varname: str, native_value: any) -> 'Model':

        self.fm.set_field_value(varname, native_value)

        return self


    def import_submodels_from_dto(self, dto: object) -> 'Model':

        return self


    def import_dto(self, dto: dtos.Dto) -> 'Model'

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


    # Loading models from a database

    def get_load_query(self, db: db_instances.Db, target_varname: str, target_value: any) -> sql_queries.SelectiveQuery:

        recordset_name = self.get_field_keeper().get_recordset_name()

        load_query = db.get_dbms().new_select().build_of_field_manager(self.get_field_manager())

        load_query.WHERE("{0}={1}", 
                   {"recordset_name": recordset_name, "varname": target_varname}, 
                   {"value": target_value})

        return load_query


    def load_siblings_and_self(self, db: db_instances.Db) -> List:

        siblings_and_self = []

        query_runner = db.get_dbms().new_query_runner()

        query_result = query_runner.execute_query(self.get_load_query(db)).get_query_result()
        fm = query_result.get_field_manager()

        while not query_result.fetch().eof():
            sibling = type(self)(self.get_chief()) \
                        if query_result.rownumber() < query_result.rowcount() - 1 \
                        else self
            siblings_and_self.append(sibling.set_field_values_from_field_manager(fm))

        return siblings_and_self


    def load_submodels(self, db: db_instances.Db) -> 'Model':

        # my_uuid = self.get_field_value("uuid")
        # self.Cows = Cow(self).set_field_value("farm_uuid", my_uuid).load_siblings_and_self(db)
        # self.Hens = Hen(self).set_field_value("farm_uuid", my_uuid).load_siblings_and_self(db)
        
        return self


    def load(self, db: db_instances.Db, target_varname: str, target_value: any) -> 'Model':

        query_runner = db.get_dbms().new_query_runner()

        query_runner.execute(self.get_load_query(db, target_varname, target_value)).fetch_one()

        self.load_submodels(db)

        return self


    # Inserting models to a database

    def get_insert_query(self, db: db_instances.Db) -> sql_queries.Insert:

        return db.get_dbms().new_insert().build_of_field_manager(self.get_field_manager())


    def get_update_query(self, db: db_instances.Db) -> sql_queries.Insert:

        return db.get_dbms().new_update().build_of_field_manager(self.get_field_manager()) 


    def get_save_query(self, db: db_instances.Db, options: Dict) -> sql_queries.Insert: 

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

            
            