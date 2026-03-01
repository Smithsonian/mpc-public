# Identifications API

The Identifications API allows users to submit suggested identifications (linkages) to the MPC. An "identification" is the discovery that two or more sets of observations belong to the same underlying object. Four types of linkage are supported:

- **ITF-to-ITF** — linking isolated tracklets together to create a new designation
- **ITF-to-DES** — linking a tracklet to an existing designated object
- **DES-to-DES** — linking two or more designated objects together
- **NEOCP-to-NEOCP** — linking NEOCP candidates together

Identifications can also be submitted via the [file upload form](https://minorplanetcenter.net/mpcops/submissions/identifications/).

## Endpoint

```
https://minorplanetcenter.net/mpcops/submissions/identifications/
```

**Method:** GET with JSON body

**Content-Type:** `application/json`

## JSON Structure

The JSON payload has two top-level sections:

| Section | Description |
|---------|-------------|
| `header` | Submitter information |
| `links` | One or more linkages, each identified by a key (e.g. `link_0`, `link_1`) |

### Header Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Submitter name, consistent with how it appears in MPECs. No accented or special characters (`{}`, `[]`). |
| `email` | Yes | Submitter email address. |
| `comment` | No | Optional comment. Include `REPLY_EMAIL` to receive automated failure notifications. |

### Link Fields

| Field | Required | Description |
|-------|----------|-------------|
| `designations` | No* | List of packed designations (e.g. `K10TD3E` for unnumbered, `s2334` for numbered). |
| `trksubs` | No* | List of tracklets, each specified as `[trkSub, date, obs-code]`. |
| `orbit` | No | Optional orbital elements for the linkage. |
| `identification_type` | No | Set to `"neocp"` for NEOCP linkages. |

\* At least one of `designations` or `trksubs` must be present in each link.

### Tracklet Format

Each tracklet is a list of three elements: `[trkSub, date, obs-code]`

The `date` can be from any observation in the tracklet, in one of these formats:

- `YYYYMMDD` (e.g. `20190828`)
- `YYYY MM DD.DDDDDDDD` (e.g. `2020 07 29.47653005`)
- `YYYY-MM-DDTHH:MM:SSZ` (e.g. `2019-01-03T13:18:37Z`)

### Orbit Fields (optional)

| Field | Description |
|-------|-------------|
| `arg_pericenter` | Argument of pericenter (degrees) |
| `eccentricity` | Orbital eccentricity |
| `epoch` | Epoch (Julian Date) |
| `inclination` | Inclination (degrees) |
| `lon_asc_node` | Longitude of ascending node (degrees) |
| `pericenter_distance` | Pericenter distance (AU) |
| `pericenter_time` | Time of pericenter passage (Julian Date) |

## Important Notes

- Designations must be in **packed form** (e.g. `K10TD3E` not `2010 TD3E`). See [packed designations](../designations/packed-designations.md) for details.
- The backslash `\` is a reserved character in JSON. If a `trkSub` begins with a backslash, it must be escaped as `\\`.
- Please validate your JSON format before submission (e.g. using [jsonformatter.org](https://jsonformatter.org/)).

## Examples

### Designations + ITF Tracklets with Orbit

```json
{
    "header": {
        "name": "J.Doe",
        "email": "j.doe@email.provider.com",
        "comment": "Example identification submission with orbit. REPLY_EMAIL"
    },
    "links": {
        "link_0": {
            "designations": ["K10TD3E", "K15A53T", "K16G96F"],
            "trksubs": [
                ["P10R1G5", "20190828", "F51"],
                ["P10R1G6", "20190827", "K16"],
                ["P10R1X4", "20190829", "F52"]
            ],
            "orbit": {
                "arg_pericenter": 51.56776,
                "eccentricity": 0.0785125,
                "epoch": 2458894.5,
                "inclination": 3.33483,
                "lon_asc_node": 298.05892,
                "pericenter_distance": 2.56959638,
                "pericenter_time": 2458148.124892
            }
        }
    }
}
```

### Designations Only (DES-to-DES)

```json
{
    "header": {
        "name": "J.Doe",
        "email": "j.doe@email.provider.com",
        "comment": "Example DES-to-DES identification."
    },
    "links": {
        "link_0": {
            "designations": ["K10TD3E", "K15A53T", "K16G96F"]
        }
    }
}
```

### ITF Tracklets Only (NEOCP Type)

```json
{
    "header": {
        "name": "J.Doe",
        "email": "j.doe@email.provider.com",
        "comment": "Example NEOCP identification."
    },
    "links": {
        "link_0": {
            "trksubs": [
                ["P10R1G5", "20190828", "F51"],
                ["P10R1G6", "20190827", "K16"],
                ["P10R1X4", "20190829", "F52"]
            ],
            "identification_type": "neocp",
            "orbit": {
                "arg_pericenter": 51.56776,
                "eccentricity": 0.0785125,
                "epoch": 2458894.5,
                "inclination": 3.33483,
                "lon_asc_node": 298.05892,
                "pericenter_distance": 2.56959638,
                "pericenter_time": 2458148.124892
            }
        }
    }
}
```

### Single Designation + ITF Tracklets (ITF-to-DES)

```json
{
    "header": {
        "name": "J.Doe",
        "email": "j.doe@email.provider.com",
        "comment": "Example ITF-to-DES identification."
    },
    "links": {
        "link_0": {
            "designations": ["K10TD3E"],
            "trksubs": [
                ["P10R1G5", "20190828", "F51"],
                ["P10R1G6", "20190827", "K16"],
                ["P10R1X4", "20190829", "F52"]
            ]
        }
    }
}
```

### Python

```python
import requests
import json

url = "https://minorplanetcenter.net/mpcops/submissions/identifications/"

params = {
    "header": {
        "name": "J.Doe",
        "email": "j.doe@email.provider.com",
        "comment": "REPLY_EMAIL"
    },
    "links": {
        "link_0": {
            "designations": ["K10TD3E", "K15A53T"]
        }
    }
}

response = requests.get(url, json=params)
print(response.status_code)
print(response.reason)
print(response.text)
```

## See Also

- [Identifications overview](../identifications/index.md) — linkage types, pipeline behavior, processing timelines
- [Acceptance criteria](../identifications/acceptance-criteria.md) — what the pipeline accepts or rejects
- [Identifications API tutorial](https://docs.minorplanetcenter.net/tutorials/notebooks/mpc_tutorial_api_identifications) — interactive notebook with worked examples
- [Submit identifications (upload form)](https://minorplanetcenter.net/mpcops/submissions/identifications/)
