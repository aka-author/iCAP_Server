
import sys
sys.path.append("C:\privat\misha\webhelp\iCAP_Server\py\kernel")
import datatypes


assert datatypes.detect_native_value_datatype(True) == datatypes.DTN_BOOLEAN
assert datatypes.detect_native_value_datatype(False) == datatypes.DTN_BOOLEAN

assert datatypes.detect_native_value_datatype(12345) == datatypes.DTN_BIGINT
assert datatypes.detect_native_value_datatype(12345.678) == datatypes.DTN_DOUBLE

assert datatypes.detect_native_value_datatype("Тарарабумбия сижу на тумбе я") == datatypes.DTN_STRING

assert datatypes.detect_native_value_datatype([1,2,3]) == datatypes.DTN_LIST
assert datatypes.detect_native_value_datatype({"foo": "bar"}) == datatypes.DTN_DICT



assert datatypes.detect_serialized_value_datatype("null") == datatypes.DTN_NULL

assert datatypes.detect_serialized_value_datatype("85769e12-8277-4673-85cc-237dd8f24112") == datatypes.DTN_UUID

assert datatypes.detect_serialized_value_datatype("true") == datatypes.DTN_BOOLEAN
assert datatypes.detect_serialized_value_datatype("false") == datatypes.DTN_BOOLEAN

assert datatypes.detect_serialized_value_datatype("123456") == datatypes.DTN_BIGINT
assert datatypes.detect_serialized_value_datatype("+123456") == datatypes.DTN_BIGINT
assert datatypes.detect_serialized_value_datatype("-123456") == datatypes.DTN_BIGINT

assert datatypes.detect_serialized_value_datatype("123456.78") == datatypes.DTN_DOUBLE
assert datatypes.detect_serialized_value_datatype("+123456.78") == datatypes.DTN_DOUBLE
assert datatypes.detect_serialized_value_datatype("-123456.78") == datatypes.DTN_DOUBLE
assert datatypes.detect_serialized_value_datatype("123456.") == datatypes.DTN_DOUBLE
assert datatypes.detect_serialized_value_datatype(".78") == datatypes.DTN_DOUBLE

assert datatypes.detect_serialized_value_datatype("2022-02-04 10:11:12.123456") == datatypes.DTN_TIMESTAMP
assert datatypes.detect_serialized_value_datatype("2022-02-04 10:11:12.123456 +02:00") == datatypes.DTN_TIMESTAMP_TZ
assert datatypes.detect_serialized_value_datatype("2022-02-04") == datatypes.DTN_DATE
assert datatypes.detect_serialized_value_datatype("10:11:12") == datatypes.DTN_TIME

assert datatypes.detect_serialized_value_datatype("Тарарабумбия сижу на тумбе я") == datatypes.DTN_STRING