
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\modules")
import dbl, ramtable, fields

rt = ramtable.Table("animals")
rt.add_field(fields.UuidField("uuid"))
rt.add_field(fields.StringField("name"))
rt.add_field(fields.StringField("species"))
rt.add_field(fields.IntField("weight"))
rt.add_field(fields.TimestampField("date_of_birth"), "mandatory")

rt.insert({"name": "Tuzik",  "species": "dog", "weight": 12})
rt.insert({"name": "Barsik", "species": "cat", "weight": 5})
rt.insert({"name": "Shustrik", "species": "rabbit", "weight": 3})

rt_res = ramtable.Table("stats")
rt_res.add_field(fields.StringField("country"))
rt_res.add_field(fields.StringField("avg_weight").set_sql_agg_expr("avg(weight)"))



db = dbl.Dbl(None)

#q_pets = db.new_select("pets")
#q_pets.DISTINCT.turn_on()
#q_pets.COLUMNS.sql.join_list_items(("pet_name", "species", "weight", "date_of_birth", "city"))
#q_pets.COLUMNS.sql.take_ramtable_fields(rt)
#q_pets.FROM.sql.join("pets")

q_pets = db.new_union("pets")
for idx in range(0, rt.count_rows()):
    subq = db.new_select("auto" + str(idx))
    subq.import_ramtable_row(rt.select_by_index(idx))
    print(subq.get_snippet())
    q_pets.subqueries.add(subq)

q_cities = db.new_select("cities")
q_cities.COLUMNS.sql.add_list_items(("city", "country"))
q_cities.FROM.sql.add("cities")

q = db.new_select("q_stats").set_output_ramtable(rt_res)
q.subqueries.add(q_pets)
q.subqueries.add(q_cities)

#q.COLUMNS.sql.join_list_items(["country", "avg(weight)"])
#q.COLUMNS.sql.take_ramtable_fields(rt_res)
q.FROM.sql.add_list_items(["pets", "cities"])
q.WHERE.sql.add("q_pets.city=cities.city and date_of_birth > '2020-01-01'")
q.GROUP_BY.sql.add("country")

#print(q.get_snippet())

# qi = db.new_insert("pets").import_source_ramtable(rt)

# print(qi.get_snippet())

qu = db.new_union("pets").import_source_ramtable(rt)
print(qu.get_snippet())