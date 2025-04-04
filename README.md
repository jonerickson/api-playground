# API Playground

A multi-language test to build simple APIs in multiple languages that meet the following specifications/features. The API should also be able to be deployed to AWS API Gateway.

## Languages

1. Python
2. Javascript
3. Go
4. Elixir
5. PHP

## Specifications/Features

1. Authentication/Authorization
2. Database Interaction (ORM)
3. Rate Limiting
4. Request Validation
5. Content Type Transformation

### Resources/Endpoints

- `GET /books`
- `GET /books/{id}`
- `POST /books`
- `PUT /books/{id}`
- `DELETE /books/{id}`

### Responses

`GET /books`

```json
// 200 OK
{
    "data": [
        {
            "id": 1,
            "title": "Book 1",
            "author": "Author 1",
        }
        ...
    ]
}
```

`GET /books/1`

```json
// 200 OK
{
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1",
    }
}
```

`POST /books`

```json
// 201 Created
{
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1",
    }
}
```

`PUT /books/1`

```json
// 200 OK
{
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1",
    }
}
```

`DELETE /books/1`

```json
// 204 No Content
""
```

### Errors

`404`

```json
{
    "error": "The book could not be found."
}
```

`422`

```json
{
    "error": "...."
}
```