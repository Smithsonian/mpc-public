# MPECs API

The MPECs API searches for Minor Planet Electronic Circulars (MPECs) associated with specific objects or search terms. It utilizes the same underlying code as the [MPEC Search Tool](https://minorplanetcenter.net/mpcops/mpecs/).

## Endpoint

```
https://data.minorplanetcenter.net/api/mpecs
```

**Method:** GET

## Input Format

The API accepts a JSON object with the following fields:

| field           | description                                            | format                                                                     | required |                                                                        
|-----------------|--------------------------------------------------------|----------------------------------------------------------------------------| --- |
| `terms`         | Array of (up to 100) search terms                      | see specification below                                                    | Yes                                                       |
| `issued_before` | Return only those MPECs published _before_ a given date | date string with optional time (e.g., `2000-01-01`, `2000-01-01 00:00:00`) | No                        |
| `issued_after` | Return only those MPECs published _after_ a given date | id.                                                                        | No                                                                         |

!!! note
    The search term is always checked against both the "title" and "full name" fields of an MPEC. This is to cast a wide net in the search results.
    For example, the MPEC titled [1992 BB](https://www.minorplanetcenter.net/mpec/J93/J93S13.html) has a "full name" called `1993-S13`, which is compressed into a mixed [Base62](https://en.wikipedia.org/wiki/Base62) character string and base 10 numeral system as `J93S13`.

### Search Term Specification

Up to 1,000 MPECs may be returned for each search term, depending on the number of matching MPECs. Search terms are case-insensitive, and may be any of the following:

1. **Object Designations** - Any designation resolvable by the [Designation Identifier API](query-identifier.md). For example, the following search terms will each return the MPEC titled [1992 BB](https://www.minorplanetcenter.net/mpec/J93/J93S13.html), as these aliases all resolve to the same object:
   ```
   1992 BB, J92B00B, 6564, Asher
   ```

2. **MPEC Names** - The "full name" of an MPEC. For example:
   ```
   1993-S13  (unpacked) 
   J93S13    (packed)
   ```

3. **Wildcards** - Use `%` for pattern matching. This approach uses no disambiguation as above. For instance, `1992%` will locate all MPECs beginning with `1992` in _either_ their titles or "full names". And `%=%` will locate MPECs used to announce 'identifications' of objects. 
   ```
   1992%     (all MPECs starting with "1992")
   %=%       (most identification MPECs)
   ```

!!! note
    Currently, object designations are resolved into the "Unpacked Primary" and "Secondary" "Provisional Designations". See the documentation on [designations](../designations/provisional-designations.md) and [identifications](../identifications/index.md) for more information. Unpacked designations are the most common title format of MPECs that refer to specific objects. Future versions of this search tool will be able to identify MPECs where a given object is mentioned among others, in the title or within the MPEC text itself. For instance, in Daily Orbit Updates or identifications MPECs. For example, [MPEC 2014-A37](https://www.minorplanetcenter.net/mpec/K14/K14A37.html). 

## Response Format

The API returns a JSON object with the following fields:

| Field     | Type| Description|
|-----------|---|---|
| `request` | Dictionary | An echo of the given request |
| `results` | Dictionary | Each search term is a key, with values containing lists of matching MPECs. See below.|

### MPEC Fields

Each MPEC result is enumerated with the following values. Note that if the MPEC lacks one of these values, it will be null.

| Field | Type | Description                                                                                         |
|-------|------|-----------------------------------------------------------------------------------------------------|
| `fullname` | String | Unique MPEC identifier (e.g., [`2022-A05`](https://www.minorplanetcenter.net/mpec/K22/K22A05.html)) |
| `title` | String | MPEC title (e.g., [`2022 AA`](https://www.minorplanetcenter.net/mpec/K22/K22A05.html))              |
| `pubdate` | String | Publication date (UTC)                                                                              |
| `link` | String | URL to the MPEC                                                                                     |

## Examples

Note that a Python Notebook tutorial is also available [here](../../../tutorials/notebooks/mpc_tutorial_api_mpecs/).

### Python

```python
import requests
import json
import sys

payload = {'terms': [
    # These two terms will match the same MPECs
    '2025-A18', 
    '2025 aa',
    # Here, 2019 UG7 = 2019 WP, but the latter's MPEC was issued before this linkage.
    '2019 UG7',
    # No matches expected
    'fancy stone', 
    # Wildcard usage
    '202% BU5'
]}
response = requests.get("https://data.minorplanetcenter.net/api/mpecs", json=payload)
response.raise_for_status()
json.dump(response.json(), sys.stdout, indent=4)
```

**Output:**

```json
{
    "request": {
        "terms": [
            "2025-A18",
            "2025 aa",
            "2019 UG7",
            "fancy stone",
            "202% BU5"
        ]
    },
    "results": {
        "2019 UG7": [
            {
                "fullname": "2019-U185",
                "link": "https://www.minorplanetcenter.net/mpec/K19/K19UI5.html",
                "pubdate": "Sat, 26 Oct 2019 12:59:23 GMT",
                "title": "2019 UG7"
            },
            {
                "fullname": "2021-C152",
                "link": "https://www.minorplanetcenter.net/mpec/K21/K21CF2.html",
                "pubdate": "Tue, 09 Feb 2021 17:09:41 GMT",
                "title": "2019 UG7"
            },
            {
                "fullname": "2019-W89",
                "link": "https://www.minorplanetcenter.net/mpec/K19/K19W89.html",
                "pubdate": "Thu, 21 Nov 2019 06:44:50 GMT",
                "title": "2019 WP"
            }
        ],
        "202% BU5": [
            {
                "fullname": "2020-B124",
                "link": "https://www.minorplanetcenter.net/mpec/K20/K20BC4.html",
                "pubdate": "Fri, 24 Jan 2020 04:05:33 GMT",
                "title": "2020 BU5"
            },
            {
                "fullname": "2023-B174",
                "link": "https://www.minorplanetcenter.net/mpec/K23/K23BH4.html",
                "pubdate": "Sun, 29 Jan 2023 01:11:37 GMT",
                "title": "2023 BU5"
            }
        ],
        "2025 aa": [
            {
                "fullname": "2025-A18",
                "link": "https://www.minorplanetcenter.net/mpec/K25/K25A18.html",
                "pubdate": "Thu, 02 Jan 2025 09:25:27 GMT",
                "title": "2025 AA"
            }
        ],
        "2025-A18": [
            {
                "fullname": "2025-A18",
                "link": "https://www.minorplanetcenter.net/mpec/K25/K25A18.html",
                "pubdate": "Thu, 02 Jan 2025 09:25:27 GMT",
                "title": "2025 AA"
            }
        ],
        "fancy stone": []
    }
}
```

### cURL

```bash
curl -X GET -H "Accept: application/json" \
  https://data.minorplanetcenter.net/api/mpecs \
  -H "Content-type: application/json" \
  -d '{"terms": ["K14A00A", "`Oumuamua"]}'
```

## See Also

<div class="contents-grid"></div>

- [MPEC API Tutorial](../../../tutorials/notebooks/mpc_tutorial_api_mpecs/)
- [MPEC Search Tool](https://minorplanetcenter.net/mpcops/mpecs/)
- [Recent MPECs](https://minorplanetcenter.net/mpec/RecentMPECs.html)
