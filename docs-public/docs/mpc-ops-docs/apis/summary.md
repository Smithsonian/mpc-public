# Summary API

The Summary API provides overall counts of the MPC's data holdings over a requested time range. These are the underlying data that supply the [MPC Summary](https://data.minorplanetcenter.net/summary/) page.

## Endpoint

```
https://data.minorplanetcenter.net/api/summary/overall 
```

**Method:** POST

!!! note
    This endpoint accepts a JSON request body.

## Request Body

| Field | Type | Required | Description                                 | Default                               |
|-------|------|----------|---------------------------------------------|---------------------------------------|
| `start_time` | String (ISO8601 datetime) | No | Earliest timestamp to include in results.   | `1647-09-29T00:00:00+00:00`           |
| `cutoff_time` | String (ISO8601 datetime) | No | Latest timestamp to include in results.     | Current UTC time at request execution |
| `limit` | Integer | No | Maximum number of summary records returned. | 1 (maximum is 1000)                   |

## Response Format

Returns a JSON array of summary objects that fall within `[start_time, cutoff_time]`.

If `limit` is provided, at most that many results are returned.

## Examples

### Python - Get the Latest Summary

```python
import requests

response = requests.post(
    "https://data.minorplanetcenter.net/api/summary/overall",
    json={},
)
response.raise_for_status()
latest_summary = response.json()[0] if response.json() else None
```

### cURL - Get Summaries Within a Time Range

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"start_time": "2026-01-01T00:00:00+00:00", "cutoff_time": "2026-01-10T00:00:00+00:00"}' \
  https://data.minorplanetcenter.net/api/summary/overall
```

## See Also

- [MPC Summary Page](https://data.minorplanetcenter.net/summary/)
- [Summary API Tutorial](../../tutorials/notebooks/mpc_tutorial_api_summary.ipynb)
