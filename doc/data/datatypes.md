# Data Types

## Introduction

This document describes data types and structures platform components and add-ons can use for a wide set of purposes. Technical documentation on performers is supposed to describe specific data structures.


## Atomic Data Types

Platform components operate in the three environments:

- Database
- JSON data transfer objects (DTOs)
- Python code

Since datatypes in these environments do not match exectly, a uniform method for passing data from one environment to another is required. This method should not imply writing intividual code snippets for each convertion. The solution is to select a limited subset of atomic data types for each platform and then map each subset to each of other two subsets. 

An internal binary format the Python run-time engine uses for representing values in RAM is a _native_ value format. The most common conversion is JSON -> native -> database or vice versa. The platform kernel foftware provides automated "duck" recognition of data types of values and convertion values between the environments. 

For the purpose of mapping, the platform suggests a _native name_ for each line of data types that mean the same. The listed atomic data types are available in the platform.

Concept           | Native name    | Database      | JSON      | Python
------------------|----------------|---------------|-----------|--------------------
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

For being represented in JSON, some data types require serialization of values as listed below. 

Concept           | Python format string      | Example
------------------|---------------------------|---------------------------------------
UUID              | N/A                       | `fccc704c-33b1-49e6-a1f9-02f2f8c4756f`
Timestamp         | `%Y-%m-%d %H:%M:%S.%f`    | `2023-12-03 10:10:10.123456`
Timestamp with TZ | `%Y-%m-%d %H:%M:%S.%f %z` | `2023-12-03 10:10:10.123456 +0200` 
Date              | `%Y-%m-%d`                | `2023-12-03`
Time              | `%H:%M:%S`                | `10:10:10.123456`

Omitting a time part is allowed for serialized timestamps but not for timestamps with a time zone. Omitting microseconds is allowed for timestamps and time values. 


## Array Data Types

Platform software components can treat arrays as atomic values in certain contexts. The array types are listed below.

Concept    | Inner name | Database | JSON     | Python  
-----------|------------|----------|----------|--------
List       | `list`     | N/A      | `Array`  | `List`
Dictionary | `dict`     | N/A      | `Object` | `Dict` 

Unlike strongly typed programming languages, the platform does not recognize arrays with different data types of their elements, say, an array of integers or an array of strings. 


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

The bounds belong to a segment. 


### Structure of a Range

The properties of a range are listed below.

Property         | Type     | Valid values                
-----------------|----------|--------------------------------------------------------
`datatype_name`  | `string` | Atomic data type names      
`range_type_name`| `string` | Range type names            
`constraints`    | `dict`   | A dictionary relevant for the range type


The generic JSON representation of a range as shown below.

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
"constraints": {"range_name": "<the name of a rule>"}
```

A property `range_name` contains the name of a rule.

Names and rules available in the platform are listed below.

Name  | Matching values                                
------|-----------------------------------------------
`any` | Any value is being checked againt a range


**Sample**

```json
{
    "datatype_name": "string",
    "range_type_name": "named",
    "constraints": {"range_name": "any"}
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

**Sample 1: A limited segment**

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

**Sample 2: A ray**

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
    "condition_name": "target_langs",
    "varname": "icap.cms.doc.localCode",
    "range": {
        "datatype_name": "string",
        "range_type_name": "set",
        "constraints": {
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
            "condition_name": "target_langs",
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
            "condition_name": "target_timeslot",
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

## Groups

A _group_ provides a rule for grouping source data before calculating aggregated values over each group.

The properties of a group are listed below.

Property   | Type   | Valid values            | Meaning
-----------|--------|-------------------------|----------------------
`group_by` | `dict` | A definition, see below | A variable for aggregating data
`range`    | `dict` | A range                 | Conditions for grouping data 

From the logical perspective, when processing a query, a server selects records from a database first. Then the server arranges the selected records into groups. A server uses _indicator values_ for making the groups. To do this, the server calculates a indicator value for each group. Records that give the same indicator value go into the same group. 

The properties of a deputy value definition are listed below.

Property        | Type     | Valid values                 | Meaning
----------------|----------|------------------------------|------------------------------
`datetype_name` | `string` | A data type name             | The data type of an indicator
`group_value`   | Any      | A value of the declared type | An indicator value of a group

**Sample**

```json
{
    "group_by_value": "Q1",
    "range": {
        "datatype_name": "timestamp",
        "range_type_Name": "segment",
        "constraints": { 
            "min": "2022-01-01", 
            "max": "2022-03-31"
        }
    }
}
```


## Dimensions

A _dimension_ describes how to group source data for calculating aggregated values. Technically, a dimension provides a field name that appears in a `GROUP BY` clause of an SQL query, but not only this. A dimension additionally can provide a set of values by which source data is getting grouped. 

The properties of a dimension are listed below. 

Property  | Type     | Mandatory | Valid values     | Meaning
----------|----------|-----------|------------------|---------------------------------
`varname` | `string` | Yes       | Variable name    | A variable for aggregating data
`groups`  | `list`   | No        | A list of groups | Conditions for grouping data 

Without groups, source data is grouped by each variable value that appears there. If groups are present, then source data is grouped by each group name. 

**Sample 1: A simple dimension**

```json
{
    "varname": "icap.cms.doc.uid"
}
```

**Sample 2: A dimension with explicit groups**

```json
{
    "varname": "accepted_at",
    "group_by_value_datatype_name": "string",
    "groups": [
        {
            "group_by_value": "Q1",
            "range": {
                "datatype_name": "timestamp",
                "range_type_name": "segment",
                "constraints": { 
                    "min": "2022-01-01", 
                    "max": "2022-03-31"
                }
            }
        },
        {
            "group_by_value": "Q2",
            "range": {
                "datatype_name": "timestamp",
                "range_type_Name": "segment",
                "constraints": { 
                    "min": "2022-04-01", 
                    "max": "2022-06-30"
                }
            }
        }
        /* The other two quarters go here */
    ]
}
```


## Granularity

A _granularity_ describes how source data is grouped. 

The properties of a granularity are listed below.

Property     | Type   | Valid values         | Meaning
-------------|--------|----------------------|-----------------------
`dimensions` | `list` | A list of dimensions | The dimensions for grouping source data

At least one dimension must exist in `dimensions`. If n dimensions are provided, and each dimension splits source data on m[1], m[2],..., m[n] groups, then m[1]\*m[2]\*...\*m[n] combined groups appear in the aggregated data. Each combined group is an intersection of n groups where each group comes from one of unique dimensions.

**Sample**

```json
{
    "dimensions": [
        {"varname": "icap.cms.doc.uid"},
        {"varname": "icap.cms.doc.localCode"}
    ]
}
```


## Generic Analytical Query

The query structure described below works fine for some analytical reports. An analytical shop can apply a query discribed like this to source data it assembles. In this case, the structure of the source data depends on the analytical shop.  

The properties of a generic analytical query are listed below. 

Property      | Type   | Valid values  | Meaning
--------------|--------|---------------|---------------------------------
`scope`       | `dict` | A scope       | The conditions for selecting source data records
`granularity` | `dict` | A granularity | The directions for aggregating the selected data

**Sample**

```json
{
    "scope": {
        "conditions": [
            {
                "condition_name": "langScope",
                "varname": "icap.cms.doc.localCode",
                "range": {
                    "datatype_name": "string",
                    "range_type_name": "set",
                    "constraints": {
                        "items": ["en", "es"]
                    }
                }
            },
            {
                "condition_name": "timeScope",
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
        "expression": "langScope and timeScope"
    },
    "granularity": {
        "dimensions": [
            {
                "varname": "accepted_at",
                "group_by_value_datatype_name": "string",
                "groups": [
                    {
                        "group_by_value": "Q1",
                        "range": {
                            "datatype_name": "timestamp",
                            "range_type_name": "segment",
                            "constraints": { 
                                "min": "2022-01-01", 
                                "max": "2022-03-31"
                            }
                        }
                    },
                    {
                        "group_by_value": "Q2",
                        "range": {
                            "datatype_name": "timestamp",
                            "range_type_name": "segment",
                            "constraints": { 
                                "min": "2022-04-01", 
                                "max": "2022-06-30"
                            }
                        }
                    },
                    {
                        "group_by_value": "Q3",
                        "range": {
                            "datatype_name": "timestamp",
                            "range_type_name": "segment",
                            "constraints": { 
                                "min": "2022-07-01", 
                                "max": "2022-09-30"
                            }
                        }
                    },
                    {
                        "group_by_value": "Q4",
                        "range": {
                            "datatype_name": "timestamp",
                            "range_type_name": "segment",
                            "constraints": { 
                                "min": "2022-10-01", 
                                "max": "2022-12-31"
                            }
                        }
                    }
                ]
            }    
        ]
    } 
}
```
