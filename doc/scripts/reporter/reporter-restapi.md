# Reporter. REST API Description

## REST API Version

The version number of the REST API is 2.


## Tasks

The following tasks are available:

- Requesting an Analytical Report


## Requesting an Analytical Report

### Result

Possible results are:

- A report is sent back to a client

- A receipt is sent back to a client

A receipt is required during the two-phase report generation. In the first phase, a reporter launches a process that performs calculations and then assembles a report. A reporter sends a receipt back to a client. In the second phase, the client trades receipt for a report.  


### URL

`POST /v2/reporter`


### Authorization

HTTP header | Format          | Meaning
------------|-----------------|---------------------- 
`Cookie`    | Serialized UUID | The UUID of a session


### Input

The input format is JSON.

**Application Request**

Property                | Type    | Mandatory | Meaning
------------------------|---------|-----------|-----------------------------------------------
`app_request_type_name` | String  | Yes       | Always `performer_task` for requesting reports
`ver`                   | Integer | Yes       | Always `2` for this version of the API
`app_request_body`      | Object  | Yes       | A task for an analytical performer
`output_template`       | Object  | No        | Directions for formatting an output

**Task for an Analytical Performer**

Property         | Type    | Mandatory | Meaning
-----------------|---------|-----------|-----------------------------------------------
`performer_name` | String  | Yes       | The name of a performer we are going to use
`task_name`      | Integer | Yes       | The name of a task we are going to perform 
`prolog`         | Object  | No        | A block of task metadata
`task_body`      | Object  | Yes       | A task definition, say, a block of query conditions 

For analytical reports, a `task name` is the name of a report.


> **Tip**
> 
> Nest a mocked report to `output_template` for debugging purposes. 
> The **Reporter** will send it back as the output.


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
    },
    "output_template": {
        /* Formatting data for the output goes here */
    }
}
```


### Output

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
`performer_name` | String  | Yes       | The name of a performer that performed the task
`task_name`      | String  | Yes       | The name of a performed task
`status_code`    | Integer | Yes       | `0` on success; an error code otherwise
`status_message` | String  | Yes       | A positive phrase on success; an error message otherwise
`prolog`         | Object  | No        | Report metadata
`output_body`    | Object  | Yes       | A report or another useful output itself

**Sample of a Report**

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
        "prolog": {
            /* Metadata goes here */
        },
        "output_body": {
            /* Useful data goes here */
        }
    }
}
```

**Sample of a Receipt**

```json
{
    "app_response_type_name": "receipt_for_output",
    "ver": 2,
    "started_at": "2023-03-19 21:26:00.869551",
    "finished_at": "2023-03-19 22:25:00.000000",
    "duration": 1234,
    "app_response_body": {
        "performer_name": "basestat",
        "task_name": "summaries",
        "status_code": 0,
        "status_message": "Please take the output later",
        "receipt_uuid": "fccc704c-33b1-49e6-a1f9-02f2f8c4756f",
        "eta": "2023-03-19 22:30:00.000000",
        "estimated_duration": "5min"
    }
}
```


### Possible Negative Responses

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
        "status_message": "Unknown request type",
        "app_request_type_name": "dance_on_your_ears"
    }
}
```

**Unknown Performer**

```json
{
    "app_response_type_name": "request_error", 
    "ver": 2, 
    "started_at": "2023-03-20 05:19:09.026175", 
    "finished_at": "2023-03-20 05:19:09.026175", 
    "duration": 0, 
    "app_response_body": {
        "status_code": 9, 
        "status_message": "Unknown performer",
        "app_request_type_name": "karabas-barabas"
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