# MPECs API

The MPECs API searches for Minor Planet Electronic Circulars (MPECs) associated with specific objects or search terms.

## Endpoint

```
https://data.minorplanetcenter.net/api/mpecs
```

**Method:** GET

## Input Format

The API accepts a JSON array of search terms:

- **Up to 100 search terms**
- **Up to 1,000 results per term**
- Search terms are case-insensitive

### Search Term Types

1. **Object Designations** - Any designation resolvable by the [Designation Identifier API](designation-identifier-api.md):
   ```
   1992 BB, J92B00B, 6564, Asher
   ```

2. **MPEC Names** - Packed or unpacked:
   ```
   1993-S13, J93S13
   ```

3. **Wildcards** - Use `%` for pattern matching:
   ```
   1992%     (all MPECs starting with "1992")
   %=%       (identification MPECs)
   ```

## Response Format

Returns a JSON object where each search term is a key, with values containing lists of matching MPECs.

### MPEC Fields

| Field | Type | Description |
|-------|------|-------------|
| `fullname` | String | Unique MPEC identifier (e.g., "2022-A05") |
| `title` | String | MPEC title (e.g., "2022 AA") |
| `pubdate` | String | Publication date (UTC) |
| `link` | String | URL to the MPEC document |

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

## Notes

- Currently searches against MPEC titles and full names only
- Future versions may search within MPEC text content
- The search uses the same code as the [MPEC Search Tool](https://minorplanetcenter.net/mpcops/mpecs/)

## See Also

- [Recent MPECs](https://minorplanetcenter.net/mpec/RecentMPECs.html)
- [MPEC Search Tool](https://minorplanetcenter.net/mpcops/mpecs/)
