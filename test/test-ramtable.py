
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\modules")
import ramtable, fields


rt = ramtable.Table("animals")
#print(rt.get_table_name())

rt.add_field(fields.UuidField("uuid"))
rt.add_field(fields.StringField("name"))
rt.add_field(fields.StringField("species"))
rt.add_field(fields.IntField("weight"))
rt.add_field(fields.TimestampField("date_of_birth"), "out", "mandatory")

print(rt.count_fields())

rt.insert_from_dic({"name": "Tuzik", "species": "dog", "weight": 12})
print(rt.count_rows())
print(rt.select_by_index(0).field_values)



