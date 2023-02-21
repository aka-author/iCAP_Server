# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  model.py                                  (\(\
# Func:    Processing subject area data              (^.^)
# # ## ### ##### ######## ############# #####################

from typing import List
import utils, dtos, dbms, fields, ramtable, bureaucrat


class Model(bureaucrat.Bureaucrat):

    def __init__(self, chief: bureaucrat.Bureaucrat, model_name: str):

        super().__init__(chief)

        self.model_name = model_name
        self.set_plural()

        self.fm = self.create_field_manager().set_recordset_name(self.get_plural())
        self.define_fields()

        self.fm.reset_field_values()


    def get_model_name(self) -> str:

        return self.model_name

    
    def set_plural(self, plural: str=None) -> object:

        if plural is None:
            last_letter = self.model_name[len(self.model_name) - 1]
            self.plural = self.model_name + ("es" if last_letter in ["s", "z"] else "s")
        else:
            self.plural = plural

        return self


    def get_plural(self) -> str:

        return self.plural


    def create_field_manager(self) -> fields.FieldManager:

        return fields.FieldManager(self)


    def is_valid(self) -> bool:

        return True


    # Working with a DTO

    def import_field_value_from_dto(self, varname: str, native_value: any) -> object:

        self.fm.set_field_value(varname, native_value)

        return self


    def import_submodels_from_dto(self, dto: object) -> object:

        return self


    def import_dto(self, dto: dtos.Dto) -> object:

        for varname in self.fm.get_varnames():
            self.import_field_value_from_dto(varname, dto.get(varname))

        self.import_submodels_from_dto(dto)

        return self


    def export_field_value_for_dto(self, varname: str) -> any:

        return self.fm.get_field_value(varname)


    def export_submodels_to_dto(self, dto: object) -> object:

        return self


    def export_dto(self) -> object:

        dto = dtos.Dto()

        for varname in self.fm.get_varnames():
            dto.set_prop_value(self.export_field_value_for_dto(varname))

        self.export_submodels_to_dto(dto)

        return dto


    # Working with a database and ramtables

    def import_master_ramtable_row(self, row):

        for field_name in row.get_table().get_field_names():
            if self.has_field(field_name):
                self.set_field_value(field_name, row.get_field_value(field_name))

        return self


    def get_empty_master_ramtable(self):

        rt = ramtable.Table(self.get_plural().lower())

        for field_name in self.fields:
            rt.add_field(self.get_field(field_name))

        return rt


    def export_master_ramtable(self):

        rt = self.get_empty_master_ramtable()

        field_values_dic = {}
        for field_name in self.fields:
            if self.fields[field_name].is_atomic():
                field_values_dic[field_name] = self.get_field_value(field_name)

        rt.insert(field_values_dic)

        return rt    


    # Loading models from a database

    def get_load_query(self, dbl: dbms.DbLayer, key_varname: str, key_value: any) -> sqlqueries.Query:

        self.fm.set_field_value(key_varname, key_value)

        dlq = self.get_dbl().new_select("loadmodel").set_output_field_manager(self.fm)
        
        dlq.WHERE.sql.add_field_equal(self.fm, key_varname)

        return dlq


    def load_siblings_and_self(self, dbl: dbms.DbLayer) -> List:

        siblings_and_self = []

        r_load = dbl.execute_query(self.get_load_query(dbl)).get_query_result()

        while not r_load.fetch().eof():
            sibling = type(self)(self.get_chief()) if r_load.rownumber() < r_load.rowcount() - 1 else self
            siblings_and_self.append(sibling.set_field_values(r_load.fm))

        return siblings_and_self


    def load_submodels(self, dbl: dbms.DbLayer) -> object:

        # my_uuid = self.get_field_value("uuid")
        # self.Cows = Cow(self).set_field_value("farm_uuid", my_uuid).load_siblings_and_self(dbl)
        # self.Hens = Hen(self).set_field_value("farm_uuid", my_uuid).load_siblings_and_self(dbl)
        
        return self


    def load(self, dbl: dbms.DbLayer, key_varname: str, key_value: any) -> object:

        dbl.execute(self.get_load_query(dbl, key_varname, key_value))

        self.load_submodels(dbl)

        return self


    # Saving models to a database

    def get_save_query(self):

        return self.get_dbl().new_insert().set_field_manager(self.fm)  


    def get_submodel_save_queries(self):

        return []


    def get_save_script(self):

        save_script = self.get_dbl().new_script().add(self.get_save_query())

        for save_query in self.get_submodel_save_queries(): save_script.add(save_query)

        return save_script


    def save(self):
        
        self.get_dbl().execute(self.get_save_script()).commit()

        return self


    def get_sql_conditions(self, field_name, col_name):

        return self.fields[field_name].get_sql_conditions(self.get_field_value(field_name), col_name)


    # Debugging

    def __str__(self):

        return "\n".join([varname + ": " + str(self.fm.get_serialized_field_value(varname)) \
                            for varname in self.fm.get_varnames()])

            
            