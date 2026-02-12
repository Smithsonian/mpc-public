# MPECs API

The MPECs API searches for Minor Planet Electronic Circulars (MPECs) associated with specific objects or search terms. It utilizes the same underlying code as the [MPEC Search Tool](https://minorplanetcenter.net/mpcops/mpecs/).

## Endpoint

```
https://data.minorplanetcenter.net/api/mpecs
```

**Method:** GET

## Input Format

The API accepts a JSON array of search terms:

- Up to 100 search terms
- Up to 1,000 MPECs per term
- Search terms are case-insensitive

!!! note
    The search term is always checked against the "title" and "full name" fields of an MPEC.
    For example, the MPEC titled [1992 BB](https://www.minorplanetcenter.net/mpec/J93/J93S13.html) has a "full name" called `1993-S13`, which is compressed into a mixed [Base62](https://en.wikipedia.org/wiki/Base62) character string and base 10 numeral system as `J93S13`.

### Search Term Types

1. **Object Designations** - Any designation resolvable by the [Designation Identifier API](query-identifier.md). For now, this is only resolved into the "Unpacked Primary Provisional Designation", which is the most common title format of MPECs. That is, searching by any identifier below will only return the MPEC titled [1992 BB](https://www.minorplanetcenter.net/mpec/J93/J93S13.html). Future versions of this search tool will be able to identify MPECs where a given object is mentioned in the title or within the MPEC text itself. For instance, in Daily Orbit Updates or identifications MPECs ([example](https://www.minorplanetcenter.net/mpec/K14/K14A37.html)). 
   ```
   1992 BB, J92B00B, 6564, Asher
   ```

2. **MPEC Names**
   ```
   1993-S13  (unpacked) 
   J93S13    (packed)
   ```

3. **Wildcards** - Use `%` for pattern matching. This approach uses no disambiguation as above. For instance, `1992%` will locate all MPECs beginning with `1992` in _either_ their titles or "full names". And `%=%` will locate MPECs used to announce 'identifications' of objects. 
   ```
   1992%     (all MPECs starting with "1992")
   %=%       (most identification MPECs)
   ```

## Response Format

Returns a JSON object where each search term is a key, with values containing lists of matching MPECs.

### MPEC Fields

Note that if the MPEC lacks one of these values, it will be null.

| Field | Type | Description                                                                                         |
|-------|------|-----------------------------------------------------------------------------------------------------|
| `fullname` | String | Unique MPEC identifier (e.g., [`2022-A05`](https://www.minorplanetcenter.net/mpec/K22/K22A05.html)) |
| `title` | String | MPEC title (e.g., [`2022 AA`](https://www.minorplanetcenter.net/mpec/K22/K22A05.html))              |
| `pubdate` | String | Publication date (UTC)                                                                              |
| `link` | String | URL to the MPEC                                                                                     |

## Examples

### Python

```python
import requests
import json
import sys

terms = ['2025-A18', '2025 aa', 'fancy stone', '202% BU5']
response = requests.get("https://data.minorplanetcenter.net/api/mpecs", json=terms)
response.raise_for_status()
json.dump(response.json(), sys.stdout, indent=4)
```

**Output:**

```json
{
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
```

### cURL

```bash
curl -X GET -H "Accept: application/json" \
  https://data.minorplanetcenter.net/api/mpecs \
  -H "Content-type: application/json" \
  -d '["K14A00A", "`Oumuamua"]'
```

## See Also

- [Recent MPECs](https://minorplanetcenter.net/mpec/RecentMPECs.html)
- [MPEC Search Tool](https://minorplanetcenter.net/mpcops/mpecs/)
