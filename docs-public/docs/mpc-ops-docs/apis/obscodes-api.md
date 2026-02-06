# Observatory Codes API

The Observatory Codes API returns information about observatories registered with the MPC.

## Endpoint

```
https://data.minorplanetcenter.net/api/obscodes
```

**Method:** GET

## Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `obscode` | String | No | Three-character observatory code | None (returns all) |
| `format` | String | No | Output format: `JSON` or `ObsCodes.html` | `JSON` |

## Response Fields (JSON format)

| Field | Type | Description |
|-------|------|-------------|
| `obscode` | String | Three-character observatory code |
| `longitude` | String | Longitude (East of prime meridian) |
| `rhocosphi` | String | Parallax constant ρ cos(φ') |
| `rhosinphi` | String | Parallax constant ρ sin(φ') |
| `name` | String | Observatory name (ASCII) |
| `name_utf8` | String | Observatory name (Unicode) |
| `name_latex` | String | Observatory name (LaTeX) |
| `short_name` | String | Abbreviated name |
| `firstdate` | String/Null | First observing date (YYYYMMDD) |
| `lastdate` | String/Null | Last observing date (YYYYMMDD) |
| `web_link` | String/Null | Observatory website URL |
| `created_at` | String | Database creation timestamp |
| `updated_at` | String | Database update timestamp |
| `uses_two_line_observations` | Boolean | Whether observatory uses two-line observations |
| `old_names` | List/Null | Previous observatory names |
| `observations_type` | String | One of: `optical`, `occultation`, `satellite`, `radar`, `roving` |

## ObsCodes.html Format

If `format`=`ObsCodes.html`, returns a string with these fixed-width fields:

| Field | Index | Description |
|-------|-------|-------------|
| obscode | [0:3] | Observatory code |
| longitude | [4:13] | Longitude |
| rhocosphi | [13:21] | ρ cos(φ') |
| rhosinphi | [21:30] | ρ sin(φ') |
| name | [30:] | Observatory name |

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

if response.ok:
    for code, data in response.json().items():
        print(f'{code:3} : {data["name"]}')
else:
    print("Error:", response.status_code, response.content)
```

### curl

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

- [Observatory Codes List](https://minorplanetcenter.net/iau/lists/ObsCodesF.html)
