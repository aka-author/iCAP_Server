# Login. REST API Description

## REST API Version

The version number of the REST API is 2.


## Tasks

The following tasks are available:

- Logging into a system


## Logging into a System

### Result

A new user session has been created. A user session UUID is issued. Client components may use the user session UUID now for sending requests to REST servers via the REST API. 

The user session is staying valid for calling each REST server while this session is not closed or expired. An ability to fulfill a certain request depends on permissions of a user who is sending this request.  


### URL

`POST /v2/login`


### Input

The input format is URL-encoded form. All the input parameters are mandatory.

Parameter  | Type   | Meaning
-----------|--------|-------------------------
`username` | String | A user name
`password` | String | A password of a user


### Positive Output

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

### Negative Output

Status code: `401`.
