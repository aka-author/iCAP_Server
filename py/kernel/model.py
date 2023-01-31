# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  model.py                                  (\(\
# Func:    Processing subject area data              (^.^)
# # ## ### ##### ######## ############# #####################

import json
import utils, fields, ramtable, bureaucrat


class Model(bureaucrat.Bureaucrat):

    def __init__(self, chief, model_name):

        super().__init__(chief)

        self.model_name = model_name
        self.set_plural()

        self.fman = self.create_fields_manager()
        self.define_fields()

        self.field_values = {}
        self.clear_field_values()


    def get_model_name(self):

        return self.model_name

    
    def set_plural(self, plural=None):

        if plural is None:
            last_letter = self.model_name[len(self.model_name) - 1]
            self.plural = self.model_name + ("es" if last_letter in ["s", "z"] else "s")
        else:
            self.plural = plural

        return self


    def get_plural(self):

        return self.plural


    def create_fields_manager(self):

        return fields.Fields()


    

    
    def is_valid(self):

        return True


    


   


    # Working with DTOs

    def field_name_native2dto(self, native_name):

        return native_name


    def field_name_dto2native(self, dto_name):

        return dto_name


    def set_field_value_from_dto(self, field_name, dto_value):

        native_value = self.fields[field_name].repair_from_dto(dto_value)

        self.set_field_value(field_name, native_value)


    def get_dto_ready_field_value(self, field_name):

        native_value = self.field_values[field_name]
        
        return utils.safearg(self.fields[field_name].prepare_value_for_dto, native_value)


    def export_dto(self):

        dto = {}

        for field_name in self.fields:
            dto_field_name = self.field_name_native2dto(field_name)
            dto[dto_field_name] = self.get_dto_ready_field_value(field_name)

        return dto


    def import_dto(self, dto):

        for dto_field_name in dto:
            field_name = self.field_name_dto2native(dto_field_name)
            if self.has_field(field_name):                
                self.set_field_value_from_dto(field_name, dto[dto_field_name])

        return self


    # Serializing and parsing

    def serialize(self, custom_format=None):

        return json.dumps(self.export_dto())


    def parse(self, serialized_model, custom_format=None):

        return self.import_dto(json.load(serialized_model)) 


    # Publishing models

    def publish(self, custom_format=None):

        return self.serialize(custom_format)


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


    def get_direct_load_query(self, field_name, field_value):

        dlq = self.get_dbl().new_select("selusers", "icap").set_output_ramtable(self.get_empty_master_ramtable())
        
        dlq.WHERE.sql.add("{0} = '{1}'".format(field_name, str(field_value)))

        return dlq


    def direct_load(self, field_name, field_value):

        dlq = self.get_direct_load_query(field_name, field_value)

        self.get_dbl().execute(dlq)

        rt = dlq.get_output_ramtable()

        if rt.count_rows() == 1:
            self.import_master_ramtable_row(rt.select_by_index(0))

        return self


    def get_direct_save_query(self):

        row_m = self.export_master_ramtable().select_by_index(0)

        return self.get_dbl().new_insert("ins", "icap").import_source_ramtable_row(row_m) 


    def direct_save(self):
        
        self.get_dbl().execute(self.get_direct_save_query()).commit()

        return self


    def get_sql_conditions(self, field_name, col_name):

        return self.fields[field_name].get_sql_conditions(self.get_field_value(field_name), col_name)


    # Debugging

    def __str__(self):

        #return "\n".join([field_name + ": " + self.serialize_field_value(field_name) for field_name in self.fields])

        return "\n".join([field_name + ": " + str(self.serialize_field_value(field_name)) for field_name in self.fields])
            
            