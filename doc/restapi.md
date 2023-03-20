# iCAP Rest API v2

## Logging into and out of a Syste,

### Logging into a System

#### URL

`POST /v2/login`


#### Input

The input format is URL-encoded form. All the input parameters are mandatory.

Parameter  | Type   | Meaning
-----------|--------|-------------------------
`username` | String | A user name
`password` | String | A password of a user


#### Positive Output

Status code: `200`.

The output format is JSON. 

Property    | Type                 | Meaning
------------|----------------------|------------------------------------
`uuid`      | Serialized UUID      | An UUID of a session
`host`      | String               | A host detected as a request sender
`opened_at` | Serialized timestamp | A moment when the session started
`expire_at` | Serialized timestamp | A moment when the session expiees
`duration`  | Integer              | The duration of the session (sec)

The property `uuid` is crucial. The other properties are auxiliary. 

**Sample**

```json
{
    "uuid": "902a980a-c53b-4562-af62-4aa33ed42f49",
    "host": "itsurim.com",
    "opened_at": "2023-03-19 21:02:06.464613",
    "expire_at": "2023-03-19 22:42:06.464613",
    "duration": 6000
}
```

#### Negative Output

Status code: `401`.


### Logging Out of a System

#### URL

`POST /v2/logout`


#### Authorization and Input

HTTP header | Format          | Meaning
------------|-----------------|-------------------------------- 
Cookie      | Serialized UUID | The UUID of a current session


#### Positive Output

Status code: `200`.


#### Negative Output

Status code: `401`.


## Requesting Reports

### Generic Report Request

#### URL

`POST /v2/reporter`


#### Authorization

HTTP header | Format          | Meaning
------------|-----------------|-------------------------------- 
Cookie      | Serialized UUID | The UUID of a current session


#### Generic Request Structure

The input format is JSON.

**Application Request**

Property                | Type    | Mandatory | Meaning
------------------------|---------|-----------|-----------------------------------------------
`app_request_type_name` | String  | Yes       | Always `performer_task` for requesting reports
`ver`                   | Integer | Yes       | Always `2` for this version of the API
`app_request_body`      | Object  | Yes       | A task for an analytical performer
`output_template`       | Object  | No        | Directions for formatting the output

**A Task for an Analytical Performer**

Property         | Type    | Mandatory | Meaning
-----------------|---------|-----------|-----------------------------------------------
`performer_name` | String  | Yes       | The name of a performer we are going to use
`task_name`      | Integer | Yes       | The name of a task we are going to perform. A task name is the name of a report in the case of analytical reports
`prolog`         | Object  | No        | A block of task metadata
`task_body`      | Object  | Yes       | A task definition, say, a block of query conditions 



> **Tip**
> 
> Nest a report to `output_template` for debugging purpose. The **Reporter** 
> will send it back to you as the output.


**Sample**

```json
{
    "app_request_type_name": "performer_task",
    "ver": 2,
    "app_request_body": {
        "performer_name": "basestat",
        "task_name": "summaries",
        "prolog": {
            /* A query prolog goes here */
        },
        "task_body": {
            /* A query conditions go here*/
        }
    }
    "output_template": {
        /* Formatting data for the output goes here */
    }
}
```


#### Generic Output Structure

Status code: `200`.

**Application Response**

Property                 | Type                 | Meaning
-------------------------|----------------------|-----------------------------------------------
`app_response_type_name` | String               | Always `performer_output` for performer tasks
`ver`                    | Integer              | Always 2 for this version of the API
`started_at`             | Serialized timestamp | The moment when the task started
`finished_at`            | Serialized timestamp | The moment when the task finished
`duration`               | Integer              | Time of performing the task (mks)
`app_response_body`      | Object               | An output of the performer

**Performer Output**

Property         | Type    | Mandatory | Meaning
-----------------|---------|-----------|----------------------------------------------------
`performer_name` | String  | Yes       | The name of the performer which performed the task
`task_name`      | String  | Yes       | The task name
`status_code`    | Integer | Yes       | `0` for a successful attempt or an error code for a failure
`status_message` | String  | Yes       | `OK` or an error message
`prolog`         | Object  | No        | Report metadata
`output_body`    | Object  | Yes       | A report

**Sample**

```json
{
    "app_response_type_name": "performer_output",
    "ver": 2,
    "started_at": "2023-03-19 21:26:00.869551",
    "finished_at": "2023-03-19 21:26:00.869649",
    "duration": 3466,
    "app_response_body": {
        "performer_name": "basestat",
        "task_name": "summaries",
        "status_code": 0,
        "status_message": "Success",
        "prolog": {},
        "output_body": {
        }
    }
}
```

#### Possible Negative Responses

Status code: `200`.

**Unknown Request Type**

```json
{
    "app_response_type_name": "request_error", 
    "ver": 2, 
    "started_at": "2023-03-20 05:19:09.026175", 
    "finished_at": "2023-03-20 05:19:09.026175", 
    "duration": 0, 
    "app_response_body": {
        "status_code": 8, 
        "status_message": "Unknown request type"
    }
}
```

**Unknown Performer**

```json
{
    "app_response_type_name": "performer_output", 
    "ver": 2, 
    "started_at": "2023-03-20 05:22:18.691382", 
    "finished_at": "2023-03-20 05:22:18.691382", 
    "duration": 0, 
    "app_response_body": {
        "performer_name": "karabas-barabas", 
        "task_name": "summaries", 
        "status_code": 9, 
        "status_message": "Unknown performer", 
        "prolog": null, 
        "output_body": null
    }
}
```

**Unknown Report**

```json
{
    "app_response_type_name": "performer_output", 
    "ver": 2, 
    "started_at": "2023-03-20 05:34:29.861053", 
    "finished_at": "2023-03-20 05:34:29.861053", 
    "duration": 12006, "app_response_body": {
        "performer_name": "basestat", 
        "task_name": "count-crows", 
        "status_code": 10, 
        "status_message": "Unknown task", 
        "prolog": null, 
        "output_body": null
    }
}
```

**Incorrect Performer Output**

```json
{
    "app_response_type_name": "performer_output", 
    "ver": 2, 
    "started_at": "2023-03-20 05:55:17.440248", 
    "finished_at": "2023-03-20 05:55:17.440248", 
    "duration": 15000, 
    "app_response_body": {
        "performer_name": "basestat", 
        "task_name": "messages", 
        "status_code": 11, 
        "status_message": "Incorrect performer output", 
        "prolog": null, 
        "output_body": {
            "incorrect_output": "Тыквенное латте"
        }
    }
}
```
