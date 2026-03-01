# Mag Bands API

The Mag Bands API returns information about photometric magnitude bands recognized by the MPC.

## Endpoint

```
https://data.minorplanetcenter.net/api/mag-band
```

**Method:** GET

**Content-Type:** `application/json`

## Request

The JSON body contains a single `band` field:

```json
{
    "band": "V"
}
```

To retrieve all currently defined bands, use `"band": "all"`:

```json
{
    "band": "all"
}
```

## Response

The API returns the original request context and an array of results:

```json
{
    "request": {
        "band": "V"
    },
    "response": [
        {
            "allowed": true,
            "band": "V",
            "notes": "Visual",
            "v_conversion": 0.0
        }
    ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `band` | String | The band code |
| `notes` | String | Human-readable description of the band |
| `allowed` | Boolean | Whether this band is currently accepted for submissions |
| `v_conversion` | Numeric or null | Offset to convert from this band to V magnitude (null if not defined) |

If the requested band code is not recognized, the `response` array will be empty.

## Python Example

```python
import json
import sys
import requests

url = "https://data.minorplanetcenter.net/api/mag-band"
payload = {
    "band": "V"
}

response = requests.get(url, json=payload)
response.raise_for_status()  # raise an exception if the HTTP result is an error
json.dump(response.json(), sys.stdout, indent=4)
```
