## Resource: Places

* The endpoints marked with the `[Auth]` symbol require the `Authentication` HTTP header to be set.

### Place collection `/api/places`

| Type | Values |
|-----------|----------------|
| Methods | [`GET`] |
|Content-type|`application/json`|
|Body fields|None|
|Query arguments|`paginate`, `page` (only required if paginated is set to true)|
|Response codes|`200`|

#### Full list [Code: 200]

*Shrunk for clarity*

```
Content-Type: application/json
Content-Length: 284387
Access-Control-Allow-Origin: *
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sun, 11 Jun 2017 02:08:11 GMT

[
	{
		"area": "Montaña",
		"...": "...",
		"hours": "Lun-Dom: 8:00 am-5:00 pm"
	},
	{
		"area": "Rural",
		"...": "...",
		"hours": ""
	},
	{
		"area": "Montaña",
		"...": "...",
		"hours": "Mar-Dom: 8:30 am-3:30 pm"
	},
	{
		"area": "Rural",
		"...": "...",
		"hours": "Vie-Dom: 9:00 am-5:00 pm"
	},
	{
		"area": "Rural",
		"...": "...",
		"hours": "Mar-Dom: 8:00 am-5:00 pm"
	}
]
```

#### Paginated list [Code: 200]

Shrunk for clarity

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 11746
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sun, 11 Jun 2017 01:02:58 GMT

{
	"page": 1,
	"result": [
		{
			"address": "2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra",
			"...": "...",
			"url": "/api/places/593b67c1bf5d2e3e7895f316"
		},
		{
			"address": "2 km Sur de Santa Gertrudis Sur ó 2 km Este de Tacares",
            "...": "...",
			"url": "/api/places/593b67c1bf5d2e3e7895f317"
		}
	]
}
```


### Place creation `/api/places` `[Auth]`

| Type | Values |
|-----------|----------------|
| Methods | [`POST`] |
|Content-type|`application/json`|
|Body fields|Place|
|Response codes|`201`, `400`, `401` & `422`|

**Note**: *Response codes 401 and 422 are for when the Authentication header is missing and when the header does not
have the expected format `<JWT>`, respectively*

#### Request body

```json
{
    "name": "Parque Acuático Cascada de Fuego",
    "area": "Montaña",
    "contact": "",
    "price_range": "Barato",
    "phone_number": "2276-6080",
    "region": "Valle Central",
    "created_at": "2017-06-10T20:08:10.888086+00:00",
    "category": "Balneario",
    "location": "San José, Desamparados, Patarrá",
    "address": "2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra",
    "email": "cascadadefuegoparqueacuatico@gmail.com",
    "latitude": 9.8757875656828,
    "longitude": -84.03733452782035,
    "hours": "Lun-Dom: 8:00 am-5:00 pm"
}
```

#### Successful creation [Code: 201]

```
Content-Type: application/json
Content-Length: 702
Access-Control-Allow-Origin: *
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sun, 11 Jun 2017 02:58:17 GMT

{
	"id": "593cb1c9bf5d2e0454ae3a99",
	"name": "Parque Acuático Cascada de Fuego",
	"area": "Montaña",
    "address": "2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra",
	"created_at": "2017-06-10T20:58:17.070561+00:00",
	"price_range": "Barato",
	"hours": "Lun-Dom: 6:00 am-4:30 pm",
	"url": "/api/places/593cb1c9bf5d2e0454ae3a99",
    "email": "cascadadefuegoparqueacuatico@gmail.com",
	"category": "Balneario",
	"contact": "",
	"phone_number": "2276-6080",
    "latitude": 9.8757875656828,
    "longitude": -84.03733452782035,
	"region": "Valle Central",
    "location": "San José, Desamparados, Patarrá",
	"google_maps": "http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035"
}
```

**Note**: *Fields `name`, `area`, `price_range`, `category`, `latitude` and `longitude` are required*

#### Invalid request body [Code: 400]

```
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 156
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sun, 11 Jun 2017 02:55:50 GMT

{
	"errors": {
		"email": [
			"Not a valid email address."
		]
	},
	"message": "Invalid request body for type <Place>",
	"status_code": 400
}
```

### Place _RUD `/api/places/<string:id>` `[Auth]`

| Type | Values |
|-----------|----------------|
| Methods | [`GET`, `PUT`, `DELETE`] |
|Content-type|`application/json`|
|Body fields|Place|
|Response codes|`200`, `400`, `401`, `404`|

**Note**: *Response codes 401 and 422 are for when the Authentication header is missing and when the header does not
have the expected format `<JWT>`, respectively. 404 for when the place with the given ID does not exist in the
database*

#### Retrieve

For the url `/api/places/593cb1c9bf5d2e0454ae3a99` the result would be:

```
Content-Type: application/json
Content-Length: 702
Access-Control-Allow-Origin: *
Server: Werkzeug/0.12.2 Python/3.6.1
Date: Sun, 11 Jun 2017 02:59:54 GMT

{
	"id": "593cb1c9bf5d2e0454ae3a99",
	"name": "Parque Acuático Cascada de Fuego",
	"area": "Montaña",
    "address": "2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra",
	"created_at": "2017-06-10T20:58:17.070561+00:00",
	"price_range": "Barato",
	"hours": "Lun-Dom: 6:00 am-4:30 pm",
	"url": "/api/places/593cb1c9bf5d2e0454ae3a99",
    "email": "cascadadefuegoparqueacuatico@gmail.com",
	"category": "Balneario",
	"contact": "",
	"phone_number": "2276-6080",
    "latitude": 9.8757875656828,
    "longitude": -84.03733452782035,
	"region": "Valle Central",
    "location": "San José, Desamparados, Patarrá",
	"google_maps": "http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035"
}
```

#### Update

**Note**: *You can pass only the fields to update in the request body*

For the url `/api/places/593cb1c9bf5d2e0454ae3a99` and the request body:

```json
{
	"name": "Parque Acuático Cascada de Fuego al Rojo vivo"
}
```

The response would look like this:

```
{
	"id": "593cb1c9bf5d2e0454ae3a99",
	"name": "Parque Acuático Cascada de Fuego al Rojo vivo",
	"area": "Montaña",
    "address": "2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra",
	"created_at": "2017-06-10T20:58:17.070561+00:00",
	"price_range": "Barato",
	"hours": "Lun-Dom: 6:00 am-4:30 pm",
	"url": "/api/places/593cb1c9bf5d2e0454ae3a99",
    "email": "cascadadefuegoparqueacuatico@gmail.com",
	"category": "Balneario",
	"contact": "",
	"phone_number": "2276-6080",
    "latitude": 9.8757875656828,
    "longitude": -84.03733452782035,
	"region": "Valle Central",
    "location": "San José, Desamparados, Patarrá",
	"google_maps": "http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035"
}
```

#### Delete

For the url `/api/places/593cb1c9bf5d2e0454ae3a99` the response would be a 204 code (No content) but implicitly
stating that the resource was deleted.
