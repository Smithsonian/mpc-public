# Magnitude Band API

The Magnitude Band API returns information about magnitude bands used in observations on record at the MPC.

## Endpoint

```
https://data.minorplanetcenter.net/api/mag-band
```

**Method:** GET 

## JSON Input Format

The API accepts one key/value pair:

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `band` | String | Yes | Abbreviated name of band, or `\"all\"` for all bands | N/A |

## Response Format

| Field | Description |
|-------|-------------|
| `request` | Echo of query parameters |
| `response` | List of records matching the query |

Each item in `response` contains:

| Field | Type | Description |
|-------|------|-------------|
| `allowed` | Boolean | True if currently allowed in submissions |
| `band` | String | Abbreviated name of band |
| `notes` | String / Null | Brief description of band |
| `v_conversion` | Float / Null | V-conversion parameter |

## Example

### Python

```python
import requests
import json

req = {
    'band': 'R'
}
response = requests.get('https://data.minorplanetcenter.net/api/mag-band', json=req)
response.raise_for_status()
print(json.dumps(response.json(), indent=4))
```

**Output:**

```json
{
    "request": {
        "band": "R"
    },
    "response": [
        {
            "allowed": true,
            "band": "R",
            "notes": "Red",
            "v_conversion": 0.4
        }
    ]
}
```

## See Also

- [Magnitude Band API Tutorial](../../../tutorials/notebooks/mpc_tutorial_api_mag_band/)

