# Observations API

The Observations API returns observational data for solar system objects from the MPC database.

## Endpoint

```
https://data.minorplanetcenter.net/api/get-obs
```

**Method:** GET

## Parameters

| Parameter | Type                      | Required | Description | Default |
|-----------|---------------------------|----------|-------------|---------|
| `desigs` | List of one single string | Yes | Name, permanent or provisional designation | None |
| `output_format` | List of strings           | No | Output format(s): `XML`, `ADES_DF`, `OBS_DF`, `OBS80` | `XML` |
| `ades_version` | String                    | No | ADES version: `2017` or `2022` | `2022` |

!!! note
    You may use any designation format supported by the [Designation Identifier API](./designation-identifier-api.md). Currently, the Orbits API is limited to single object queries.

### Valid `output_format` specifications

| Format | Type | Description                                                                                      |
|--------|------|--------------------------------------------------------------------------------------------------|
| `XML` | String | Observations in [ADES XML](https://minorplanetcenter.net/iau/info/ADES.html) format              |
| `OBS80` | String | Observations in [MPC1992 80-column](https://minorplanetcenter.net/iau/info/ObsFormat.html) format |
| `ADES_DF` | List of dicts | Dictionary representation of ADES values                                                         |
| `OBS_DF` | List of dicts | Dictionary representation of 80-column format                                                    |

Multiple formats can be requested. E.g., `["XML", "OBS80"]`

## Examples

### Python - XML Format

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-obs",
    json={"desigs": ["2023 AB"], "output_format": ["XML"]}
)
response.raise_for_status()
xml_string = response.json()[0]['XML']
```

### Python - 80-column Format

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-obs",
    json={"desigs": ["Bennu"], "output_format": ["OBS80"]}
)
response.raise_for_status()
obs80_string = response.json()[0]['OBS80']
```

**Output `obs80` string:**

```
A1955J99R36Q* C1999 09 11.40624 01 37 54.90 -27 04 27.5          15.1  aa6197704
A1955J99R36Q  C1999 09 11.42149 01 38 00.18 -27 03 59.6          15.1  aa6197704
...
```

### Python - Pandas DataFrame

```python
import requests
import pandas as pd

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-obs",
    json={"desigs": ["Bennu"], "output_format": ["ADES_DF", "OBS_DF"]}
)
response.raise_for_status()
ades_df = pd.DataFrame(response.json()[0]['ADES_DF'])
obs_df = pd.DataFrame(response.json()[0]['OBS_DF'])
```

### cURL

```bash
curl -X GET -H "Content-Type: application/json" \
  -d '{"desigs": ["13270"]}' \
  https://data.minorplanetcenter.net/api/get-obs
```
