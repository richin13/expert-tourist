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