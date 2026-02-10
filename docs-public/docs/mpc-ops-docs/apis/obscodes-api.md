# Observatory Codes API

The Observatory Codes API returns information about observatories registered with the MPC.

## Endpoint

```
https://data.minorplanetcenter.net/api/obscodes
```

**Method:** GET

## Parameters

| Parameter | Type | Required | Description                                                                                       | Default |
|-----------|------|----------|---------------------------------------------------------------------------------------------------|---------|
| `obscode` | String | No | Three-character observatory code; e.g., `000`                                                      | None (returns all) |
| `format` | String | No | Output format: `JSON` or [`ObsCodes.html`](https://minorplanetcenter.net/iau/lists/ObsCodes.html) | `JSON` |

There are over 2,500 observatories registered with the MPC. Each is assigned a unique observatory code where the first character is a number or capital letter and the second and third characters are both numbers. If you omit `obscode`, information for all observatories is returned.

## Response Fields (JSON format)

| Field | Type           | Description                                                                                                            |
|-------|----------------|------------------------------------------------------------------------------------------------------------------------|
| `obscode` | String         | Three-character observatory code                                                                                       |
| `longitude` | String         | Longitude (East of prime meridian)                                                                                     |
| `rhocosphi` | String         | Parallax constant `ρ cos(φ')`, where `φ'` is the geocentric latitude and `ρ` is the geocentric distance in earth radii |
| `rhosinphi` | String         | Parallax constant `ρ sin(φ')`; ibid.                                                                                   |
| `name` | String         | Observatory name (ASCII)                                                                                               |
| `name_utf8` | String         | Observatory name (Unicode)                                                                                             |
| `name_latex` | String         | Observatory name (LaTeX)                                                                                               |
| `short_name` | String         | Abbreviated name (ASCII)                                                                                               |
| `firstdate` | String or Null | First observing date or commissioning (YYYYMMDD)                                                                       |
| `lastdate` | String or Null | Last observing date or decommissioning (YYYYMMDD)                                                                      |
| `web_link` | String or Null | Observatory website URL                                                                                                |
| `created_at` | String         | Timestamp at which the observatory code was created in the MPC database.                                               |
| `updated_at` | String         | Timestamp at which the observatory code was created in the MPC database.                                               |
| `uses_two_line_observations` | Boolean        | Whether observatory uses two-line observations (most do not.)                                                          |
| `old_names` | List/Null      | Previous observatory names                                                                                             |
| `observations_type` | String         | One of: `optical`, `occultation`, `satellite`, `radar`, `roving`                                                       |

## ObsCodes.html Format

If `format == 'ObsCodes.html'`, returns a string with the same format as the [old flatfile by the same name](https://minorplanetcenter.net/iau/lists/ObsCodes.html) (albeit without the header line.) If the `obscode` field is defined, just a single line is returned, otherwise a line for each observatory is returned, separated by newline characters (`\n`). The return value has the following fixed-width fields:

| Field | Index | Description           |
|-------|-------|-----------------------|
| obscode | [0:3] | Observatory code      |
| longitude | [4:13] | Longitude             |
| rhocosphi | [13:21] | ρ cos(φ'); see above. |
| rhosinphi | [21:30] | ρ sin(φ'); see above. |
| name | [30:] | Observatory name      |

## Examples

### Python - Single Observatory

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/obscodes",
    json={"obscode": "310"}
)

response.raise_for_status()
for key, value in response.json().items():
    print(f'{key:27}: {value}')
```

**Output:**

```
created_at                 : Mon, 18 Nov 2019 23:52:11 GMT
firstdate                  : None
lastdate                   : None
longitude                  : 288.87164
name                       : Minor Planet Center Test Code
...
obscode                    : 310
observations_type          : optical
rhocosphi                  : 0.739802
rhosinphi                  : 0.670574
...
```

### Python - Flatfile Format

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/obscodes",
    json={"obscode": "310", "format": "ObsCodes.html"}
)

response.raise_for_status()
print(response.text)
```

**Output:**

```
310 288.871640.739802+0.670574Minor Planet Center Test Code
```

### Python - All Observatories

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/obscodes",
    json={}
)
response.raise_for_status()
for code, data in response.json().items():
    print(f'{code:3} : {data["name"]}')
```

### cURL

```bash
# Single observatory
curl -X GET -H "Content-Type: application/json" \
  -d '{"obscode": "310"}' \
  https://data.minorplanetcenter.net/api/obscodes

# All observatories
curl -X GET -H "Content-Type: application/json" \
  -d '{}' \
  https://data.minorplanetcenter.net/api/obscodes
```

## See Also

- [Observatory Codes List](https://data.minorplanetcenter.net/explorer/?tab=Lists&list=Observatory+Codes) on the [MPC Explorer](https://data.minorplanetcenter.net/explorer/)
- [HTML Observatory Codes List](https://minorplanetcenter.net/iau/lists/ObsCodesF.html)
