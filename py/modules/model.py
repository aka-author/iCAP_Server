# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Module:  model.py                                  (\(\
# Func:    Processing subject area data              (^.^)
# # ## ### ##### ######## ############# #####################

import json
import utils, bureaucrat


class Model(bureaucrat.Bureaucrat):

    def __init__(self, chief, model_name):

        super().__init__(chief)

        self.model_name = model_name

        self.fields = {}
        self.key_names = []
        self.define_fields()

        self.field_values = {}
        self.clear_field_values()


    def get_model_name(self):

        return self.model_name


    def get_key_names(self):

        return self.key_names


    def is_key(self, field_name):

        return field_name in self.key_names


    # Defining fields

    def define_field(self, field, key_mode=None):

        field_name = field.get_field_name() 
        self.fields[field_name] = field

        if key_mode is not None:
            field.set_key_mode(key_mode)
            self.key_names.append(field_name)


    def has_field(self, field_name):

        return field_name in self.fields


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

        for field_name in self.fields:
            empty_value = self.fields[field_name].get_empty_value()
            self.set_field_value(field_name, empty_value) 


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


    # Working with SQL

    def get_sql_conditions(self, field_name, col_name):

        return self.fields[field_name].get_sql_conditions(self.get_field_value(field_name), col_name)