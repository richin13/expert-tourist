## Authentication

Expert tourist's API protects some of the resources from public access in order to allow only registered users to create,
update and delete such resources. To do so, it exposes two endpoints: one for user registration and another for user
authentication.

The protected endpoints require the `Authentication` header to be set with the value `<JWT>`

### User registration `/api/sign_up`

| Type | Values |
|-----------|----------------|
| Methods | [`POST`] |
|Content-type|`application/json`|
|Body fields|`email`, `username` & `password`|
|Response codes|`200` & `400`|

#### Successful registration [Code: 200]

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 440
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sat, 10 Jun 2017 23:14:18 GMT

{
    "email": "richin14@gmail.com",
    "id": "593c7d4abf5d2e59894478a7",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0.Pnq9qjS6JzazGNxE",
    "username": "richin13"
}
```

#### Already registered user [Code: 400]

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 121
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sat, 10 Jun 2017 23:31:21 GMT

{
	"message": "A user with the email richin14@gmail.com already exists. Forgot your password?",
	"status_code": 400
}
```

#### Missing body fields [Code: 400]

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 90
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sat, 10 Jun 2017 23:32:33 GMT

{
	"message": "Fields <username, email, password> are required",
	"status_code": 400
}
```

**Notes on responses**: Even though the response's JSON body includes a `status_code` field, the HTTP response also
includes the correspondent status code

### User authentication `/api/sign_in`

| Type | Values |
|-----------|----------------|
| Methods | [`POST`] |
|Content-type|`application/json`|
|Body fields|`username` & `password`|
|Response codes|`200`, `400` & `401` |

#### Successful login [Code: 200]

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 440
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sat, 10 Jun 2017 23:43:06 GMT

{
	"email": "richin13@gmail.com",
	"id": "593c2cabbf5d2e0ebf38ea0a",
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0.Pnq9qjS6JzazGNxE",
	"username": "richin13"
}
```

#### Invalid request body [Code: 400]

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 84
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sat, 10 Jun 2017 23:47:01 GMT

{
	"message": "Fields <username, password> are required.",
	"status_code": 400
}
```

#### Invalid login [Code: 401]

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 68
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sat, 10 Jun 2017 23:46:03 GMT

{
	"message": "Invalid login credentials",
	"status_code": 401
}
```

