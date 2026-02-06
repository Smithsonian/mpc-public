# Observations API

The Observations API returns observational data for solar system objects from the MPC database.

## Endpoint

```
https://data.minorplanetcenter.net/api/get-obs
```

**Method:** GET

## Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `desigs` | List (single string) | Yes | Name, permanent or provisional designation | None |
| `output_format` | List of strings | No | Output format(s): `XML`, `ADES_DF`, `OBS_DF`, `OBS80` | `XML` |
| `ades_version` | String | No | ADES version: `2017` or `2022` | `2022` |

You can search for any single permanent or provisional designation. Both packed and unpacked formats are supported.

## Output Formats

| Format | Type | Description |
|--------|------|-------------|
| `XML` | String | Observations in ADES XML format |
| `OBS80` | String | Observations in MPC1992 80-column format |
| `ADES_DF` | List of dicts | Dictionary representation of ADES values |
| `OBS_DF` | List of dicts | Dictionary representation of 80-column format |

Multiple formats can be requested: `["XML", "OBS80"]`

## Examples

### Python - XML Format

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-obs",
    json={"desigs": ["2023 AB"], "output_format": ["XML"]}
)

if response.ok:
    xml_string = response.json()[0]['XML']
    print(xml_string)
else:
    print("Error:", response.status_code, response.content)
```

### Python - 80-column Format

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-obs",
    json={"desigs": ["Bennu"], "output_format": ["OBS80"]}
)

if response.ok:
    obs80_string = response.json()[0]['OBS80']
    print(obs80_string)
else:
    print("Error:", response.status_code, response.content)
```

**Output:**

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

if response.ok:
    ades_df = pd.DataFrame(response.json()[0]['ADES_DF'])
    obs_df = pd.DataFrame(response.json()[0]['OBS_DF'])
    print(ades_df)
    print(obs_df)
else:
    print("Error:", response.status_code, response.content)
```

### curl

```bash
curl -X GET -H "Content-Type: application/json" \
  -d '{"desigs": ["13270"]}' \
  https://data.minorplanetcenter.net/api/get-obs
```
