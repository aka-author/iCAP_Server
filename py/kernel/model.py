# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  model.py                                  (\(\
# Func:    Processing subject area data              (^.^)
# # ## ### ##### ######## ############# #####################

import json
import utils, ramtable, bureaucrat


class Model(bureaucrat.Bureaucrat):

    def __init__(self, chief, model_name):

        super().__init__(chief)

        self.model_name = model_name
        self.set_plural()

        self.fields = {}
        self.field_names = []
        self.key_names = []
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


    def get_key_names(self):

        return self.key_names


    def is_key(self, field_name):

        return field_name in self.key_names


    def get_field_names(self):

        return self.field_names


    def get_field(self, field_name):

        return self.fields[field_name]


    # Defining fields

    def add_field(self, field, options=""):

        field_name = field.get_varname() 
        self.fields[field_name] = field
        self.field_names.append(field_name)

        if "key" in options:
            self.key_names.append(field_name)

        return self


    def has_field(self, field_name):

        return field_name in self.field_names


    def define_fields(self):

        pass


    # Setting, getting, checking field values

    def set_field_value(self, field_name, native_value):

        self.field_values[field_name] = native_value
            

    def get_field_value(self, field_name):

        return self.field_values[field_name]

    
    def is_valid(self):

        return True


    def serialize_field_value(self, field_name, custom_format=None):

        native_value = self.get_field_value(field_name)

        return self.fields[field_name].serialize(native_value, custom_format)


    def parse_field_value(self, field_name, serialized_value, custom_format=None):

        native_value = self.fields[field_name].parse(serialized_value, custom_format)

        return self.set_field_value(field_name, native_value)


    def publish_field_value(self, field_name, custom_format=None):

        native_value = self.get_field_value(field_name)

        return self.fields[field_name].publish(native_value, custom_format)


    def clear_field_values(self):

        for field_name in self.field_names:
            null_value = self.fields[field_name].get_null_value()
            self.set_field_value(field_name, null_value) 


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
        
        return utils.govnone(self.fields[field_name].prepare_for_dto, native_value)


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


    # Working with SQL and ramtables

    def import_master_ramtable_row(self, row):

        for field_name in row.get_table().get_field_names():
            if self.has_field(field_name):
                self.set_field_value(field_name, row.get_field_value(field_name))

        return self


    def get_master_ramtable(self):

        rt = ramtable.Table(self.get_plural().lower())

        for field_name in self.fields:
            rt.add_field(self.get_field(field_name))

        return rt


    def export_master_ramtable(self):

        rt = self.get_master_ramtable()

        src_dic = {}
        for field in self.fields:
            if field.is_atomic():
                field_name = self.get_field_name()
                src_dic[field_name] = self.get_field_value(field_name)

        rt.insert(src_dic)

        return rt    


    def get_quick_load_query(self, field_name, field_value):

        q = self.get_dbl().new_select("selusers", "icap").set_output_ramtable(self.get_master_ramtable())
        
        q.WHERE.sql.add("{0} = '{1}'".format(field_name, str(field_value)))

        return q


    def quick_load(self, field_name, field_value):

        q = self.get_quick_load_query(field_name, field_value)

        self.get_dbl().execute(q)

        rt = q.get_output_ramtable()

        if rt.count_rows() == 1:
            self.import_master_ramtable_row(rt.select_by_index(0))

        return self


    def get_sql_conditions(self, field_name, col_name):

        return self.fields[field_name].get_sql_conditions(self.get_field_value(field_name), col_name)