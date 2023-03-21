# Data Types

## Atomic Data Types

The listed atomic data types are allowed in the platform.

Concept           | Inner name     | Database      | JSON      | Python
------------------|----------------|---------------|-----------|----------
Null              | `null`         | `null`        | `Null`    | `NoneType`
UUID              | `uuid`         | `uuid`        | `String`  | `uuid.UUID`
Boolean           | `boolean`      | `boolean`     | `Boolean` | `bool`
Integer           | `bigint`       | `bigint`      | `Number`  | `int`
Float             | `double`       | `double`      | `Number`  | `float`
String            | `string`       | `varchar`     | `String`  | `str`
Timestamp         | `timestamp`    | `timestamp`   | `String`  | `datetime.datetime`
Timestamp with TZ | `timestamp_tz` | `timestamptz` | `String`  | `datetime.datetime`
Date              | `date`         | `timestamp`   | `String`  | `datetime.datetime`
Time              | `time`         | `timestamp`   | `String`  | `datetime.datetime`
   
The abbreviation _TZ_ stands for a time zone here and in other contexts. 

> **TBD**
>
> We are going to have a data type for a timeslot duration some time.

For the sake of JSON, some data types require values to be serialized into a string as listed below.

Concept           | Python format string      | Example
------------------|---------------------------|---------------------------------------
UUID              | N/A                       | `fccc704c-33b1-49e6-a1f9-02f2f8c4756f`
Timestamp         | `%Y-%m-%d %H:%M:%S.%f`    | `2023-12-03 10:10:10.123456`
Timestamp with TZ | `%Y-%m-%d %H:%M:%S.%f %z` | `2023-12-03 10:10:10.123456 +0200` 
Date              | `%Y-%m-%d`                | `2023-12-03`
Time              | `%H:%M:%S`                | `10:10:10.123456`

Omitting a time part is allowed for serialized timestamps but not for timestamps with a time zone. 

Omitting microseconds is allowed for timestamps and time values. 


## Array Data Types

Platform software components can treat arrays as atomic values in certain contexts. The array types are listed below.


Concept    | Inner name | Database | JSON     | Python  
-----------|------------|----------|----------|--------
List       | `list`     | N/A      | `Array`  | `List`
Dictionary | `dict`     | N/A      | `Object` | `Dict` 

Unlike programming languages like Pascal, the platform does not recognize arrays by data types of their elements, say, an array of integers or an array of strings. 


## Ranges

### Understanding Ranges

A _range_ is a structure that describes constraints a value should match. Being nested into query conditions, a range works as a boolean function of a variable value. 

Each range is applicable to values of a certain data type. 

Each range belongs to one of _range types_ the platform supprots. The type of a range denotates a rule for checking values. The platform provides a fixed set of rules implemented in the code.


### Range Types

The range types available in the platform are listed below.

Range type | Matching values      
-----------|--------------------------------------------------------------
`named`    | Each value matching an individual named rule 
`set`      | Each value that belongs to an explicit set of values 
`segment`  | Each value between the minimum and the maximum

The platform provides a fixed set of named rules. 

Segment bounds belong to a segment. 

> **TBD**
>
> We parhaps need to support a `set_of_segments` as well.


### Structure of a Range

Each range consists of the porperties listed below.

Property         | Type     | Valid values                
-----------------|----------|--------------------------------------------------------
`datatype_name`  | `string` | Atomic data type names      
`range_type_name`| `string` | Range type names            
`constraints`    | `dict`   | A dictionary relevant for the range type


A generic JSON representation of a range as shown below.

```json
{
    "datatype_name":   /* A data type name goes here" */,
    "range_type_name": /* A range type name goes here" */,
    "constraints":     /* Constraints go here */ 
}
```


### Named Ranges

A _named range_ invokes a specific rule for checking a given value. The rule is implemented in the code of the platform.

The format of constraints for named ranges is shown below.

```json
"constraints": {"name": "<the name of a rule>"}
```

A property `name` contains the name of a rule.

Names and rules available in the platform are listed below.

Name  | Matching values                                
------|-----------------------------------------------
`any` | Any value is being checked againt a range


**Sample**

```json
{
    "datatype_name": "string",
    "range_type_name": "named",
    "constraints": {"name": "any"}
}
```


### Set Ranges

A value matches a _set range_ if it belongs to a set. Otherwise, a value does not match a range. 

A property `constraint` provides an explicit set of values that match a range. The format of constraints for set ranges is shown below.

```json
"constraints": {
    "members": "[<A list of values matching a range>]"
}
```

**Sample**

```json
{
    "datatype_name": "string",
    "range_type_name": "set",
    "constraints": {"members": ["de", "en", "es", "fr"]}
}
```

> **TBD**
>
> Rules for matching values are coming soon: case sensetivity, etc.


### Segment Ranges

A value matches a _segment range_ if it not less than minimum and not greater than the maximum _bound_. Segment ranges make sense for sortable values only.

A property `constraint` provides the bounds of a range. The format of constraints for segment ranges is shown below.

```json
"constraints": {
    "min": "<the minimim value matching a range>", 
    "max": "<the maximum value matching a range>"
}
```

A bound is infinite if it is set to `null`.

**Sample 1. A limited segment**

```json
{
    "datatype_name": "timestamp",
    "range_type_name": "segment",
    "constraints": { 
        "min": "2022-01-01", 
        "max": "2022-06-30"
    }
} 
```

**Sample 2. A ray**

```json
{
    "datatype_name": "timestamp",
    "range_type_name": "segment",
    "constraints": { 
        "min": "2022-01-01", 
        "max": null
    }
}
```


## Conditions

A _condition_ is a rule for checking a variable value against a range. In other words, it is a place where a variable and a range meed each other.

The properties of a condition are listed below.

Property    | Type     | Mandatory | Valid values | Meaning
------------|----------|-----------|--------------|---------------------------------
`cond_name` | `string` | No        | A name       | A name for referring a condition
`varname`   | `string` | Yes       | A name       | A variable we are going to check
`range`     | `dict`   | Yes       | A range      | A range for checking variable values

**Sample**
```json
{
    "cond_name": "target_langs",
    "varname": "icap.cms.doc.localCode",
    "range": {
        "datatype_name": "string",
        "range_type_name": "set",
        "values": {
            "members": ["de", "en", "es", "fr"]
        }
    }
}
```


## Scopes

A _scope_ is a set of conditions joined with boolead functions. While a condition is applicable to a singular variable value, a scope is applicable a set of variable values.

The properties of a scope are listed below.

Property     | Type     | Mandatory | Valid values 
-------------|----------|-----------|----------------------
`conditions` | `list`   | Yes       | A list of conditions 
`expression` | `string` | No        | A boolean expression 

If an expression is omitted, then the conditions are treated as joined with `and`.

**Sample**

```json
{
    "conditions": [
        {
            "cond_name": "target_langs",
            "varname": "icap.cms.doc.localCode",
            "range": {
                "datatype_name": "string",
                "range_type_name": "set",
                "constraints": {
                    "members": ["de", "en", "es", "fr"]
                }
            }
        },
        {
            "cond_name": "target_timeslot",
            "varname": "accepted_at", 
            "range": {
                "datatype_name": "timestamp",
                "range_type_name": "segment",
                "constraints": { 
                    "min": "2022-01-01", 
                    "max": "2022-12-31"
                }
            }
        }
    ],
    "expression": "target_langs and target_timeslot"
}
```


