# Designation Identifier API

The Designation Identifier API returns information about the various designations assigned to any given object.

## Endpoint

```
https://data.minorplanetcenter.net/api/query-identifier
```

**Method:** GET

## Parameters

You can search for up to 100 designations at once. The response will be a dictionary of results, using the input IDs as keys.

Input search terms can be any of the following (you may mix and match):

1. **Unpacked Provisional Designations:** `1984 KB`, `A/2017 U1`, `S/1900 J 10`
2. **Packed Provisional Designations:** `J84K00B`, `AK17U010`, `SJ00J100`
3. **Names:** `Jason`, `ʻOumuamua`, `Lysithea`
4. **Permanent IDs:** `6063`, `1I`, `Jupiter X`
5. **Packed Permanent IDs:** `06063`, `0001I`, `J010S`

### Fuzzy Name Searching

For name searches, you can use comparison operators:

| Operator | Description |
|----------|-------------|
| `=` | Exact match |
| `ILIKE` | Case-insensitive partial match |
| `%` | Wildcard/similar to |

You can also filter by group: `Minor Planets`, `Natural Satellites`, `Comets`, `Interstellar`

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `found` | Integer | 0 if no match, 1 if found, >1 if disambiguation needed |
| `object_type` | List | [String name, Numeric index] |
| `orbfit_name` | String | Orbfit-friendly ID (IAU designation without spaces) |
| `name` | String | Object name (if assigned) |
| `citation` | String | Citation text (if assigned) |
| `iau_designation` | String | IAU designation |
| `permid` | String | Permanent ID |
| `packed_permid` | String | Packed permanent ID |
| `packed_primary_provisional_designation` | String | Packed primary provisional designation |
| `packed_secondary_provisional_designations` | List[str] | Packed secondary designations |
| `unpacked_primary_provisional_designation` | String | Unpacked primary provisional designation |
| `unpacked_secondary_provisional_designations` | List[str] | Unpacked secondary designations |
| `disambiguation_list` | List[dict] | Populated when multiple matches found |

## Examples

### Python - Basic Query

```python
import requests
import json

my_list = {"ids": ["Ceres", "2020 AB1"]}
response = requests.get("https://data.minorplanetcenter.net/api/query-identifier", json=my_list)
response.raise_for_status()
print(json.dumps(response.json(), indent=4))
```

**Output:**

```json
{
    "2020 AB1": {
        "citation": null,
        "disambiguation_list": null,
        "found": 1,
        "iau_designation": "2020 AB1",
        "name": null,
        "object_type": ["Minor Planet", 0],
        "orbfit_name": "2020AB1",
        "packed_permid": null,
        "packed_primary_provisional_designation": "K20A01B",
        "packed_secondary_provisional_designations": ["K16D00O"],
        "permid": null,
        "unpacked_primary_provisional_designation": "2020 AB1",
        "unpacked_secondary_provisional_designations": ["2016 DO"]
    },
    "Ceres": {
        "citation": null,
        "disambiguation_list": null,
        "found": 1,
        "iau_designation": "1",
        "name": "Ceres",
        "object_type": ["Minor Planet", 0],
        "orbfit_name": "1",
        "packed_permid": "00001",
        "packed_primary_provisional_designation": "I01A00A",
        "packed_secondary_provisional_designations": ["I99O00F", "J43X00B"],
        "permid": "1",
        "unpacked_primary_provisional_designation": "A801 AA",
        "unpacked_secondary_provisional_designations": ["A899 OF", "1943 XB"]
    }
}
```

### Python - Fuzzy Name Search

```python
import requests
import json

req = {"ids": ["Boriso"], "comparison": "%", "group": "Minor Planets"}
response = requests.get("https://data.minorplanetcenter.net/api/query-identifier", json=req)
response.raise_for_status()
print(json.dumps(response.json(), indent=4))
```

This returns a disambiguation list for minor planets with names similar to 'Boriso'.

## See Also

- [PostgreSQL Pattern Matching Documentation](https://www.postgresql.org/docs/current/functions-matching.html)
