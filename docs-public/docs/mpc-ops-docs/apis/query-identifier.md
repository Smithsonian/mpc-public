# Designation Identifier API

The Designation Identifier API returns information about the various designations assigned to small solar system objects.

## Endpoint

```
https://data.minorplanetcenter.net/api/query-identifier
```

**Method:** GET

## Parameters

You can search for up to 100 designations at once. The response will be a dictionary of results, using the input IDs as keys.

Input search terms can be any of the following. You may mix and match input types:

1. **Unpacked Primary (or Secondary) Provisional Designations**, e.g., 
  [`1984 KB`][Jason],
  [`A/2017 U1`][Oumuamua], 
  [`S/1900 J 10`][Lysithea]
2. **Packed Provisional Designations**, e.g., 
  [`J84K00B`][Jason], 
  [`AK17U010`][Oumuamua], 
  [`SJ00J100`][Lysithea]
3. **Names**, e.g., 
  [`Jason`][Jason], 
  [`ʻOumuamua`][Oumuamua], 
  [`Lysithea`][Lysithea]
4. **Permanent IDs**, e.g.,
  [`6063`][Jason], 
  [`1I`][Oumuamua], 
  [`Jupiter X`][Lysithea]
5. **Packed Permanent IDs**, e.g., 
  [`06063`][Jason],
  [`0001I`][Oumuamua], 
  [`J010S`][Lysithea]

[Jason]: https://data.minorplanetcenter.net/explorer/?tab=Designated&search=1984+KB
[Oumuamua]: https://data.minorplanetcenter.net/explorer/?tab=Designated&search=A%2F2017+U1
[Lysithea]: https://data.minorplanetcenter.net/explorer/?tab=Designated&search=S%2F1900+J+10

### JSON Input Format

The following fields are accepted by the API:

| Field        | Type            | Required | Default | Description                                                                                                                                                         |
|--------------|-----------------|----------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ids`        | List of strings | Yes      | NA      | List of designations to search for                                                                                                                                  |
| `comparison` | String          | No       | None    | [PSQL comparison operator](https://www.postgresql.org/docs/current/functions-matching.html#FUNCTIONS-MATCHING) for fuzzy name searches; one of `['=', 'ILIKE', '%']` |
| `group`      | String          | No       | None    | One of `['Minor Planets', 'Natural Satellites', 'Comets', 'Interstellar']`; constrains the name search to a category of objects.                                    |

!!! note
    The `comparison` and `group` fields are only applicable in name searches.

## Response Fields

The following fields are always returned by the API. If the object lacks one of these ID types, the value will be null. 

| Field | Type                 | Description                                                                                                                   |
|-------|----------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `found` | Integer              | 0 if no match, 1 if found, >1 if disambiguation needed                                                                        |
| `object_type` | List of two values   | An [object type](https://minorplanetcenter.net/mpcops/documentation/object-types/) identifier: `[String name, Numeric index]` |
| `name` | String               | Object name (if assigned)                                                                                                     |
| `citation` | String               | Citation text (if assigned)                                                                                                   |
| `permid` | String               | Permanent ID                                                                                                                  |
| `packed_permid` | String               | Packed permanent ID                                                                                                           |
| `iau_designation` | String               | IAU designation                                                                                                               |
| `orbfit_name` | String               | Orbfit-friendly ID (IAU designation without spaces)                                                                           |
| `packed_primary_provisional_designation` | String               | Packed primary provisional designation                                                                                        |
| `packed_secondary_provisional_designations` | List of strings      | Packed secondary designations                                                                                                 |
| `unpacked_primary_provisional_designation` | String               | Unpacked primary provisional designation                                                                                      |
| `unpacked_secondary_provisional_designations` | List of strings      | Unpacked secondary designations                                                                                               |
| `disambiguation_list` | List of dictionaries | Populated _only_ when multiple matches found                                                                                  |

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

This returns a disambiguation list for minor planets with names similar to `'Boriso'`.

## See Also

- [PostgreSQL Pattern Matching Documentation](https://www.postgresql.org/docs/current/functions-matching.html)
