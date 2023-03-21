# Logout. REST API Description

## REST API Version

The version number of the REST API is 2.


## Tasks

The following tasks are available:

- Logging out of a system


## Logging Out of a System

## Result

A user session is closed now. In other words, it is not valid anymore. Each REST server in a system will reject REST requests that provide the UUID of this user session.


### URL

`POST /v2/logout`


### Authorization

HTTP header | Format          | Meaning
------------|-----------------|-------------------------------- 
`Cookie`    | Serialized UUID | The UUID of a user session


### Input

Input is not required.


### Positive Output

Status code: `200`.


### Negative Output

Status code: `401`.
