# Catalog Codes API

The Catalog Codes API can provide the complete set of "catalog codes" for a given astrometric catalog. 
It can also provide a list of all codes recognized by the MPC. 

These codes are also available [here](../observations/valid-ades-values.md#astcat-photcat-star-catalogs).

## Endpoint

```
https://data.minorplanetcenter.net/api/catalog-codes
```

**Method:** POST

## Input Format

The API accepts a JSON object with the following fields:

| field           | description                                            | format                                                                     | required | default |                                                                        
|-----------------|--------------------------------------------------------|----------------------------------------------------------------------------| --- | --- |
| `catalog_code`         | Catalog code                      | string                                                    | No | None |
| `catalog_code_type`         | Catalog code type                      | string in `['catalog', 'ades_code', 'obs80_code']`                                                    | No | `ades_code` |

!!! note
    If no `catalog_code` is provided, the API will return all catalog codes recognized by the MPC. 
    If a `catalog_code` is provided, the API will return only that code if it is recognized by the MPC.

## Response Format

The API returns a JSON object with the following fields:

| Field     | Type| Description|
|-----------|---|---|
| `request` | `dict`  | The input parameters supplied to the API. |
| `response` | `list[dict]` | The API response containing the catalog codes (see below). |

A catalog code is represented as a JSON object with the following fields:

| Field     | Type| Description|
|-----------|---|---|
| `catalog` | string  | The catalog code's 'longname'. E.g., 'Gaia DR 3'. |
| `ades_code` | string | The catalog code's ADES code. E.g., 'Gaia3'. |
| `obs80_code` | string | The catalog code's MPC1992 code. E.g., 'W'. |
| `deprecated` | boolean | Whether the catalog code is deprecated. |

## Examples

Note that a Python Notebook tutorial is also available [here](../../../tutorials/notebooks/mpc_tutorial_api_catalog_codes/).

### Python

#### To get all catalog codes recognized by the MPC:
```python
import requests
import json
import sys

# An empty payload will return all catalog codes recognized by the MPC.
response = requests.post("https://data.minorplanetcenter.net/api/catalog-codes", json={})
response.raise_for_status()
json.dump(response.json(), sys.stdout, indent=4)
```

#### To get a specific catalog code, e.g., 'NOMAD':
```python
# The API assumes that the `catalog_code_type` is `ades_code` if not specified.
payload = {"catalog_code": "NOMAD"}
response = requests.post("https://data.minorplanetcenter.net/api/catalog-codes", json=payload)
response.raise_for_status()
json.dump(response.json(), sys.stdout, indent=4)
```

#### To get a specific catalog code by its obs80_code, e.g., 'v':
```python
payload = {"catalog_code": "v", "catalog_code_type": "obs80_code"}
response = requests.post("https://data.minorplanetcenter.net/api/catalog-codes", json=payload)
response.raise_for_status()
json.dump(response.json(), sys.stdout, indent=4)
```

##### Example output for the above request:
```json
{
  'request': {
    'catalog_code': 'v', 
    'catalog_code_type': 'obs80_code'
  }, 
  'response': [
    {
      'catalog': 'NOMAD',
      'ades_code': 'NOMAD',
      'obs80_code': 'v',
      'deprecated': False,
    },
  ]
}
```

### cURL

```bash
curl -X POST \
  https://data.minorplanetcenter.net/api/catalog-codes \
  -H "Content-type: application/json" \
  -d '{"catalog_code": "NOMAD"}'
```

## See Also

<div class="contents-grid"></div>

- [Catalog Codes API Tutorial](../../../tutorials/notebooks/mpc_tutorial_api_catalog_codes/)
- [Valid catalog codes](../observations/valid-ades-values.md#astcat-photcat-star-catalogs)
