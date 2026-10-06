# Orbit Type API

The Orbit Type API can determine an "orbit type" for given orbital parameters from [the categories maintained by the MPC](../orbits/orbit-types.md).

## Endpoint

```
https://data.minorplanetcenter.net/api/orbit-type
```

**Method:** POST

## Input Format

The API accepts a JSON object with the following fields:

| field           | description                                            | format                                                                     | required |                                                                        
|-----------------|--------------------------------------------------------|----------------------------------------------------------------------------| --- |
| `a`         | Semi-major axis                      | float                                                    | No (if `q` is provided.)                                                       |
| `q`         | Perihelion distance                      | float                                                    | No (if `a` is provided.)                                                       |
| `e`         | Eccentricity                      | float                                                    | Yes                                                       |
| `i`         | Inclination                      | float                                                    | Yes                                                       |
| `mpcID`         | MPC [unpacked primary provisional designation](../designations/provisional-designations.md)                      | string                                                    | Yes (unless `require_mpcID == False`.)                                                        |
| `require_mpcID`         | Whether a MPC designation is required.                      | boolean                                                    | No (default: `True`)                                                        |

!!! note
    `mpcID` is used to establish precise orbit types for comets and natural satellites. If `require_mpcID` is set to `False`, the API will return a best-effort orbit type based on the provided orbital parameters, even if no valid MPC designation is provided.

## Response Format

The API returns a JSON object with the following fields:

| Field     | Type| Description|
|-----------|---|---|
| `orbit_type` | integer  | Determined orbit type, or `None` if it could not be determined. |
| `orbit_type_long` | string | A human-readable 'long' name for the orbit type. |

## Examples

Note that a Python Notebook tutorial is also available [here](../../../tutorials/notebooks/mpc_tutorial_api_orbit_type/).

### Python

```python
import requests
import json
import sys

payload = {
    "a": 2.5,
    "e": 0.1,
    "i": 5.0,
    "require_mpcID": False
}
response = requests.post("https://data.minorplanetcenter.net/api/orbit-type", json=payload)
response.raise_for_status()
json.dump(response.json(), sys.stdout, indent=4)
```

**Output:**

```json
{
    "orbit_type": 11,
    "orbit_type_long": "Middle Main Belt"
}
```

### cURL

```bash
curl -X POST \
  https://data.minorplanetcenter.net/api/orbit-type \
  -H "Content-type: application/json" \
  -d '{"a": 2.5, "e": 0.1, "i": 5.0, "require_mpcID": false}'
```

## See Also

<div class="contents-grid"></div>

- [Orbit Type API Tutorial](../../../tutorials/notebooks/mpc_tutorial_api_orbit_type/)
- [Orbit Type Categories](../orbits/orbit-types.md)
