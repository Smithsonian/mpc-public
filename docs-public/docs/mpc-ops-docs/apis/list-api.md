# List API

The List API returns lists of objects belonging to various groups, ordered alphanumerically by designation. This includes lists of NEOs, comets, TNOs, and other categories.

## Endpoint

```
https://data.minorplanetcenter.net/api/list
```

**Method:** GET 

## JSON Input Format

The following key/value pairs are accepted by the API. Where applicable, default values are used when omitted by the user. 

| Parameter | Type | Required | Description                                                                                                            | Default |
|-----------|------|----------|------------------------------------------------------------------------------------------------------------------------|---------|
| `list` | String | Yes | Object group to query; see below for valid categories                                                                  | NA       |
| `order` | String | No | Sort order: `ASC` or `DESC`                                                                                            | `ASC`   |
| `limit` | Integer | No | Maximum results (1-50,000)                                                                                             | 50,000  |
| `offset` | Integer | No | This offset may be used to start from a given index in the result set, which is ordered alphanumerically by designation | 0       |
| `like` | String | No | Pattern for filtering designations (PostgreSQL [LIKE syntax][PSQLLIKE])                                                | None    |

[PSQLLIKE]: https://www.postgresql.org/docs/current/functions-matching.html#FUNCTIONS-LIKE

### Available Lists

| List Name | Description |
|-----------|-------------|
| `minor-planets` | All minor planets |
| `neos` | Near-Earth Objects |
| `inners` | Inner solar system objects |
| `middles` | Middle solar system objects |
| `outers` | Outer solar system objects |
| `binaries` | Binary asteroids |
| `comets` | All comets |
| `fragments` | Comet fragments |
| `atiras` | Atira-class asteroids |
| `atens` | Aten-class asteroids |
| `apollos` | Apollo-class asteroids |
| `amors` | Amor-class asteroids |
| `inner-others` | Other inner solar system objects |
| `mars-crossers` | Mars-crossing asteroids |
| `main-belters` | Main belt asteroids |
| `jovian-trojans` | Jupiter Trojans |
| `tnos` | Trans-Neptunian Objects |
| `hyperbolics` | Hyperbolic objects |
| `parabolics` | Parabolic objects |
| `unbounded` | Unbound objects |
| `planet-nat-sats` | Planetary natural satellites |
| `mp-nat-sats` | Minor planet natural satellites |
| `impacted` | Impacted objects |
| `retired` | Retired designations |
| `dual-status` | Dual-status objects (comet/asteroid) |
| `minor-planet-names` | Named minor planets |
| `nat-sat-names` | Named natural satellites |
| `comet-names` | Named comets |
| `interstellar-names` | Named interstellar objects |

### Pattern Filtering

The `like` parameter accepts PostgreSQL [LIKE patterns][PSQLLIKE] for filtering unpacked primary provisional designations:

- `%` matches any sequence of characters
- `_` matches any single character

## Response Format

| Field | Description |
|-------|-------------|
| `items` | List of objects matching the query |
| `request` | Echo of query parameters |

Each item contains:

| Field | Type | Description |
|-------|------|-------------|
| `name` | String/Null | Object name (if assigned) |
| `permid` | String/Null | Permanent ID (if numbered) |
| `unpacked_primary_provisional_designation` | String | Primary provisional designation |

## Examples

### Python

```python
import requests
import json

req = {
    'list': 'neos',
    'limit': 5,
    'like': '2010%'
}
response = requests.get('https://data.minorplanetcenter.net/api/list', json=req)
response.raise_for_status()
print(json.dumps(response.json(), indent=4))
```

**Output:**

```json
{
    "items": [
        {
            "name": null,
            "permid": null,
            "unpacked_primary_provisional_designation": "2010 AA93"
        },
        {
            "name": null,
            "permid": null,
            "unpacked_primary_provisional_designation": "2010 AB103"
        },
        {
            "name": null,
            "permid": null,
            "unpacked_primary_provisional_designation": "2010 AB3"
        },
        {
            "name": null,
            "permid": "614599",
            "unpacked_primary_provisional_designation": "2010 AB78"
        },
        {
            "name": null,
            "permid": null,
            "unpacked_primary_provisional_designation": "2010 AC3"
        }
    ],
    "request": {
        "like": "2010%",
        "limit": 5,
        "list": "neos",
        "offset": 0,
        "order": "ASC"
    }
}
```

### Pagination Example

```python
import requests

# Get 'first page'
req = {'list': 'neos', 'limit': 100, 'offset': 0}
response = requests.get('https://data.minorplanetcenter.net/api/list', json=req)
first_page = response.json()['items']

# Get 'second page'
req['offset'] = 100
response = requests.get('https://data.minorplanetcenter.net/api/list', json=req)
second_page = response.json()['items']
```

## See Also

- [PostgreSQL Pattern Matching](PSQLLIKE)
