# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  model.py                                  (\(\
# Func:    Processing subject area data              (^.^)
# # ## ### ##### ######## ############# #####################

import json
import utils, fields, ramtable, bureaucrat


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

    def import_field_value_from_dto(self, varname: str, dto_value: any) -> object:

        datatype_name = self.fm.get_field(varname).get_datatype_name()

        native_value = self.get_dtoms().repair_value_from_dto(dto_value, datatype_name)

        return self.fm.set_field_value(varname, native_value)


    def import_submodels_from_dto(self, dto: object) -> object:

        return self


    def import_dto(self, dto: object) -> object:

        for varname in self.fm.get_varnames():
            self.import_field_value_from_dto(varname, dto.get(varname))

        self.import_submodels_from_dto(dto)

        return self


    def export_field_value_for_dto(self, varname: str) -> any:

        native_value = self.fm.get_field_value(varname)

        datatype_name = self.fm.get_field(varname).get_datatype_name()

        return self.get_dtoms().prapare_value_for_dto(native_value, datatype_name)


    def export_submodels_to_dto(self, dto: object) -> object:

        self


    def export_dto(self) -> object:

        dto = {}

        for varname in self.fm.get_varnames():
            dto[varname] = self.export_field_value_for_dto(varname)

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

    def get_load_query(self, key_varname, key_value):

        self.fm.set_field_value(key_varname, key_value)

        dlq = self.get_dbl().new_select("loadmodel").set_output_field_manager(self.fm)
        
        dlq.WHERE.sql.add_field_equal(self.fm, key_varname)

        return dlq


    def load_submodels(self):

        return self


    def load(self, key_varname, key_value):

        load_query = self.get_load_query(key_varname, key_value)

        self.get_dbl().execute(load_query)

        rt = load_query.get_output_ramtable()

        if rt.count_rows() == 1:
            self.import_master_ramtable_row(rt.select_by_index(0))

        self.load_submodels()

        return self


    # Saving models to a database

    def get_save_query(self):

        return self.get_dbl().new_insert().set_field_values(self.get_plural(), self.fm) 


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


    # Serializing and parsing

    def serialize(self, format: str=None) -> str:

        return json.dumps(self.export_dto())


    def parse(self, serialized_model: str, format: str=None) -> object:

        return self.import_dto(json.load(serialized_model)) 


    # Publishing models

    def publish(self, format: str=None) -> str:

        return self.serialize(format)


    # Debugging

    def __str__(self):

        return "\n".join([varname + ": " + str(self.fm.get_serialized_field_value(varname)) \
                            for varname in self.fm.get_varnames()])

            
            