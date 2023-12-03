# Notification Service

## General info
This project is a web application for manage newsletters and get statistics.

## Setup
Change .env-example to .env and use docker-compose.
```
docker-compose build
```
```
docker-compose up
```
Than you need to create migrations:
```
docker-compose exec backend python manage.py makemigrations
```
And apply the migration:
```
docker-compose exec backend python manage.py migrate
```
## Endpoints

### Newsletters
___
Get list of newsletters.
```
'GET' /api/newsletters/
```
Response body example:
`[
  {
    "id": 0,
    "start_time": "2023-12-03T15:40:26.309Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:40:26.309Z"
  }
]`
___
Create a new newsletter.
```
'POST' /api/newsletters/
```
Request body example:
`{
    "start_time": "2023-12-03T15:54:33.658Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:54:33.658Z"
}`

Response body example:
`{
    "id": 0,
    "start_time": "2023-12-03T15:40:26.309Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:40:26.309Z"
}`
___
Receive the newsletter at id.
```
'GET' /api/newsletters/{id:int}/
```
Response body example:
`{
    "id": 0,
    "start_time": "2023-12-03T15:40:26.309Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:40:26.309Z"
}`
___
Update the newsletter at id.
```
'PUT' /api/newsletters/{id:int}/
```
Request body example:
`{
    "start_time": "2023-12-03T15:54:33.658Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:54:33.658Z"
}`

Response body example:
`{
    "id": 0,
    "start_time": "2023-12-03T15:40:26.309Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:40:26.309Z"
}`
___
Partial update the newsletter at id.
```
'PATCH' /api/newsletters/{id:int}/
```
Request body example (you may not pass all fields):
`{
    "start_time": "2023-12-03T15:54:33.658Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:54:33.658Z"
}`

Response body example:
`{
    "id": 0,
    "start_time": "2023-12-03T15:40:26.309Z",
    "messages_text": "string",
    "user_filter": "string",
    "finish_time": "2023-12-03T15:40:26.309Z"
}
`
___
Delete the newsletter at id.
```
'DELETE' /api/newsletters/{id:int}/
```
___
### Users
___
Get list of users.
```
'GET' /api/users/
```
Response body example:
`[
    {
        "id": 0,
        "phone_number": "73828753118",
        "tag": "string",
        "timezone": "string"
    }
]`
___
Create a new user.
```
'POST' /api/users/
```
Request body example:
`{
    "phone_number": "76877633935",
    "tag": "string",
    "timezone": "string"
}`

Response body example:
`{
    "id": 0,
    "phone_number": "76877633935",
    "tag": "string",
    "timezone": "string"
}`
___
Receive the user at id.
```
'GET' /api/users/{id:int}/
```
Response body example:
`{
    "id": 0,
    "phone_number": "76877633935",
    "tag": "string",
    "timezone": "string"
}`
___
Update the user at id.
```
'PUT' /api/users/{id:int}/
```
Request body example:
`{
    "phone_number": "76877633935",
    "tag": "string",
    "timezone": "string"
}`

Response body example:
`{
    "id": 0,
    "phone_number": "76877633935",
    "tag": "string",
    "timezone": "string"
}`
___
Partial update the user at id.
```
'PATCH' /api/users/{id:int}/
```
Request body example (you may not pass all fields):
`{
    "phone_number": "76877633935",
    "tag": "string",
    "timezone": "string"
}`

Response body example:
`{
    "id": 0,
    "phone_number": "76877633935",
    "tag": "string",
    "timezone": "string"
}`
___
Delete the user at id.
```
'DELETE' /api/users/{id:int}/
```
___
### Statistics
___
Get detailed statistics of messages sent for a specific newsletter.
```
'GET' /api/statistics/
```
Response body example:
`[
  {
    "newsletter_id": 0,
    "in_progress": 0,
    "delivered": 0,
    "is_not_delivered": 0
  }
]`
___
Get general statistics on created newsletters at id.
```
'GET' /api/statistics/{id:int}/
```
Response body example:
`[
  {
    "id": 0,
    "status": "delivered",
    "user_phone_number": "71251234595",
    "created_at": "2023-11-28T22:52:00.967055+03:00"
  },
  {
    "id": 1,
    "status": "delivered",
    "user_phone_number": "71234567895",
    "created_at": "2023-11-28T22:52:01.268079+03:00"
  }
]`
___