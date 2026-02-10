# NEOCP Observations API

The NEOCP Observations API returns observational data for objects currently on the [Near-Earth Object Confirmation Page (NEOCP)](https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html).

## Endpoint

```
https://data.minorplanetcenter.net/api/get-obs-neocp
```

**Method:** GET

## Parameters

| Parameter | Type                      | Required | Description                                           | Default |
|-----------|---------------------------|----------|-------------------------------------------------------|---------|
| `trksubs` | List of one single string | Yes | Tracklet identifier (`trksub`) on the NEOCP           | None    |
| `output_format` | List of strings           | No | Output format(s): `XML`, `ADES_DF`, `OBS_DF`, `OBS80` | `XML`   |
| `ades_version` | String                    | No | ADES version: `2017` or `2022`                        | `2022`  |

**Note:** Only objects currently on the NEOCP can be queried. For confirmed objects, use the [Observations API](observations-api.md).

## Output Formats

| Format | Type | Description |
|--------|------|-------------|
| `XML` | String | Observations in ADES XML format |
| `OBS80` | String | Observations in MPC1992 80-column format |
| `ADES_DF` | List of dicts | Dictionary representation of ADES values |
| `OBS_DF` | List of dicts | Dictionary representation of 80-column format |

## Examples

**Note:** Examples use tracklet IDs that may no longer be on the NEOCP. Replace with a current tracklet from the [NEOCP](https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html).

### Python - XML Format

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-obs-neocp",
    json={"trksubs": ["A118xu6"], "output_format": ["XML"]}
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
    "https://data.minorplanetcenter.net/api/get-obs-neocp",
    json={"trksubs": ["xkos423"], "output_format": ["OBS80"]}
)

if response.ok:
    obs80_string = response.json()[0]['OBS80']
    print(obs80_string)
else:
    print("Error:", response.status_code, response.content)
```

**Output:**

```
     xkos423 1B2024 07 15.81527220 06 39.103-56 39 51.72         19.2 VZ     M49
     xkos423 1B2024 07 15.82485020 06 23.639-56 39 28.20         19.5 VZ     M49
...
```

### Python - Pandas DataFrame

```python
import requests
import pandas as pd

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-obs-neocp",
    json={"trksubs": ["xkos423"], "output_format": ["ADES_DF", "OBS_DF"]}
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
  -d '{"trksubs": ["SWC0732"]}' \
  https://data.minorplanetcenter.net/api/get-obs-neocp
```

## See Also

- [NEOCP](https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html) - Current NEOCP listing
- [Observations API](observations-api.md) - For confirmed objects
