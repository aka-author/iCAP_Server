
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import ramtable, fields


rt = ramtable.Table("animals")
#print(rt.get_table_name())

rt.fm.add_field(fields.UuidField("uuid"))\
     .add_field(fields.StringField("name"))\
     .add_field(fields.StringField("species"))\
     .add_field(fields.BigintField("weight"))\
     .add_field(fields.DateField("date_of_birth"), "mandatory")

print(rt.fm.count_fields())

rt.insert({"name": "Tuzik", "species": "dog", "weight": 12})
print(rt.count_rows())
print(rt.select_by_index(0))



