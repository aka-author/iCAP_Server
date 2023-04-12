# Basic Statistics

## Tasks

### A List of Tasks

The performer provides an access to the following tasks:

- Assembling Statistical Summaries
- Reporting Readers' Messages


### Assembling Statistical Summaries

TBD


### Reporting Readers' Messages

#### Result

The task returns messages readers have posted.


### URL

`POST /v2/reporter`


### Authorization

HTTP header | Format          | Meaning
------------|-----------------|-------------------------------- 
`Cookie`    | Serialized UUID | The UUID of a user session


#### Input

- Generic Analytical Query

A generic analitical query must contain the following properties:

- `scope`


#### Output

- A messages report

**Sample**

```json
{
    "app_response_type_name": "performer_output",
    "ver": 2,
    "started_at": "2023-04-12 09:34:17.644384",
    "finished_at": "2023-04-12 09:34:17.644384",
    "duration": 740026,
    "app_response_body": {
        "performer_name": "basestat",
        "task_name": "messages",
        "status_code": 0,
        "status_message": "OK",
        "prolog": null,
        "output_body": {
            "messages": [
                {
                    "accepted_at": "2023-04-09 13:53:34.186000 +0000",
                    "icap.cms.doc.uid": "74679",
                    "icap.cms.doc.localCode": "en",
                    "icap.cms.doc.verno": "2",
                    "icap.cms.topic.uid": "74691",
                    "icap.cms.topic.verno": "2",
                    "icap.page.title": "Turtle Soup",
                    "icap.page.url": "http://localhost/cookbook/cookbook_turtle-soup.html",
                    "icap.action.code": "DISLIKE",
                    "icap.action.message": "I am so confused!"
                }
            ]
        }
    }
}
```

## Data Structures

### Variables

The variables associated with a reader's action are listed below.

Variable                 | Type        | Valid values  | Meaning
-------------------------|-------------|---------------|---------------
`accepted_at`            | `timestamp` | Any timestamp | Date and time when an action happened
`icap.cms.doc.uid`       | `string`    | Any string    | Unique id of a document
`icap.cms.doc.localCode` | `string`    | A local code  | Local code of a viewed page
`icap.cms.doc.verno`     | `string`    | Any string    | Document version number
`icap.cms.topic.uid`     | `string`    | Any string    | Unique id of a topic
`icap.cms.topic.verno`   | `string`    | Any string    | Topic version number
`icap.page.title`        | `string`    | Any string    | Title of a viewed page
`icap.page.url`          | `string`    | Any string    | URL of a viewed page
`icap.action.code`       | `string`    | Action code   | Code of an action a reader performed
`icap.action.message`    | `string`    | Any string    | Message a reader posted


## Local Codes

A _local code_ is a standard string value denoting a primary language and a language version specific for a certain country. A document, topic, or another content slice has a local code. 

A local code consists of the following parts:

- Language code
- Country code

The format of a country code is `ll-CC`.

A language code is mandatory. A country code may be omitted. 

**Samples**

`en-US`, `ru-RU`, `he`


### Action Codes

An _action code_ is a string value that denotes an event or an action a reader performed while reading a page. 

The action codes the performer recognizes are listed below.

Action code | Meaning                  | Corresponding variables
------------|--------------------------|--------------------------
`DISLIKE`   | A reader disliked a page | `icap.action.message`
`LOAD`      | A reader loaded a page   |
`LIKE`      | A reader liked a page    |
`UNLOAD`    | A reader left a page     | `icap.action.message`