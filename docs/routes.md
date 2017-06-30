# Resource: Routes

## Routes recommendations `/api/routes` or `/api/recommend`

| Type | Values |
|-----------|----------------|
| Methods | [`POST`] |
|Content-type|`application/json`|
|Body fields|`area`, `budget`, `travel_dist`, `activity`, `coordinates`|
|Response codes|`200`, `400`|

**Body fields encoding**

```yaml
- area:
    Mountain: 0
    Rural: 1
    Urban: 2
    Coast: 3
- budget:
    Low: 0
    Moderate: 1
    High: 2
- travel_dist:
    Short: 0
    Moderate: 1
    Long: 2
- activity:
    Familiar: 0
    Adventure: 1
    Casual: 2
- coordinates: [lat, long]
```

### Example request

**Request body**
```json
{
	"area": 0,
	"activity": 1,
	"budget": 1,
	"travel_dist": 2,
	"coordinates": [
		9.8408317,
		-83.8737972
	]
}
```

**Response**
```json
[
	{
		"origin": {
			"lat": 9.8408317,
			"lng": -83.8737972
		},
		"destination": {
			"lat": 9.683872,
			"lng": -83.896156
		},
		"stops": [
			{
				"location": {
					"lat": 9.819109774953,
					"lng": -83.85875573381782
				}
			}
		]
	},
	{
		"origin": {
			"lat": 9.8408317,
			"lng": -83.8737972
		},
		"destination": {
			"lat": 9.683872,
			"lng": -83.896156
		},
		"stops": [
			{
				"location": {
					"lat": 9.819109774953,
					"lng": -83.85875573381782
				}
			}
		]
	},
	{
		"origin": {
			"lat": 9.8408317,
			"lng": -83.8737972
		},
		"destination": {
			"lat": 9.683872,
			"lng": -83.896156
		},
		"stops": [
			{
				"location": {
					"lat": 9.819109774953,
					"lng": -83.85875573381782
				}
			}
		]
	}
]
```

If there are no available places to recommend then the response is an empty array.
