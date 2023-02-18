
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import dtos


random_payload = {
    "uuid": "fd3034bd-565b-4823-81f4-19cc2f47915f",
    "name": "Tuzik",
    "weight": 12,
    "date_of_birth": "2020-03-12",
    "arnocles": ["2020-03-12", "2020-03-13", "2020-03-14"],
    "arnocles2": [{"foo": ["a", "b", "c"]}, "2020-03-12 10:10:10.123456 +02:00", "2020-03-13 10:10:10.123456", "2020-03-14 10:10:10.123456"],
    "arnocles3": {"pivo": "raki"}
}

dto = dtos.Dto(random_payload).repair_datatypes()

print(dto.get_payload())

print(dto.export_payload())

dto1 = dtos.Dto(dto.export_payload()).repair_datatypes()

print(dto1.get_payload())