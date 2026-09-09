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

Note that summary records are timestamped at the time of their creation, which is typically once per hour. Therefore, the `start_time` and `cutoff_time` parameters are inclusive of the summary records that fall within that range.

| Field | Type | Required | Description                                 | Default                               |
|-------|------|----------|---------------------------------------------|---------------------------------------|
| `start_time` | String (ISO8601 datetime) | No | Earliest timestamp to include in results.   | `1647-09-29T00:00:00+00:00`           |
| `cutoff_time` | String (ISO8601 datetime) | No | Latest timestamp to include in results.     | Current UTC time at request execution |
| `limit` | Integer | No | Maximum number of summary records returned. | 1 (maximum is 1000)                   |

## Response Format

Returns a JSON array of summary objects that fall within `[start_time, cutoff_time]`.

If `limit` is provided, at most that many results are returned.

A summary object has the values given in the table below. All of which are relative to `cutoff_time`; this timestamp marks the end of the summary's "field of regard". For example, `designated_objects` is a count of provisional designations as recorded in the MPC's database, of all entries with `created_at` prior to the `cutoff_time`.

| Field | Type | Description |
|-------|------|-------------|
| `cutoff_time` | String (ISO8601 datetime) | Timestamp marking the end of the summary. |
| `designated_objects` | Integer | Count of [provisionally designated](../designations/provisional-designations.md) objects. |
| `numbered_objects` | Integer | Count of [numbered objects](../data-and-services/schema/numbered-identifications.md). |
| `neocp_objects` | Integer | Count of [NEOCP objects](../data-and-services/neocp-notes.md). |
| `pccp_objects` | Integer | Count of PCCP objects. |
| `identifications` | Integer | Count of [identifications](../identifications/index.md). |
| `obscodes` | Integer | Count of [observatory codes](../observatory-and-program-codes/index.md). |
| `program_codes` | Integer | Count of [program codes](../observatory-and-program-codes/index.md). |
| `obs_published` | Integer | Count of published observations. |
| `obs_itf` | Integer | Count of ITF observations. |
| `obs_duplicated` | Integer | Count of duplicated observations. |
| `obs_deleted` | Integer | Count of deleted observations. |
| `designated_this_year` | Integer | Count of objects [designated](../designations/provisional-designations.md) this year. |
| `designated_this_month` | Integer | Count of objects [designated](../designations/provisional-designations.md) this month. |
| `designated_this_half_month` | Integer | Count of objects [designated](../designations/provisional-designations.md) in the last half month. |
| `orbit_type_counts` | Object | Counts of observations by numbered/unnumbered status, per [orbit type](../orbits/orbit-types.md). |
| `object_type_counts` | Object | Counts of observations by numbered/unnumbered status, per [object type](../orbits/object-types.md). |
| `mpec_counts` | Object | Counts of MPECs, subset by MPEC type. |
| `named_minor_planets` | Integer | Count of named minor planets. |
| `named_natural_satellites` | Integer | Count of named natural satellites. |
| `named_comets` | Integer | Count of named comets. |
| `named_interstellar` | Integer | Count of named interstellar objects. |
| `updated_at` | String (ISO8601 datetime) | Timestamp when the summary record was last updated. |

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
