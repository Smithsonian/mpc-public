# Check Near-Duplicates (CND) API

The Check Near-Duplicates API identifies observations in the MPC database that are potential duplicates of observations you provide. This helps detect duplicate submissions before they enter the database.

## Endpoint

```
https://data.minorplanetcenter.net/api/cnd
```

**Method:** GET

## Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `obs` | List of strings | Yes | 80- or 160-character observation records in MPC format | None |
| `time_separation_s` | Float | No | Temporal threshold (0-60 seconds) | 60 |
| `angle_separation_arcsec` | Float | No | Spatial threshold (0-10 arcseconds) | 5 |
| `omit_separation` | Boolean | No | Exclude separation values from results | false |

**Limits:**

- Up to 10,000 observations per request
- Searches against publicly published MPC observations only

## Response Format

The response contains:

| Field | Description |
|-------|-------------|
| `request` | Echo of the original query parameters |
| `results` | Dictionary mapping each input observation to matching near-duplicates |

Each match includes:

| Field | Type | Description |
|-------|------|-------------|
| `obs80` | String | The near-duplicate observation record |
| `time_separation_s` | Float | Temporal gap in seconds |
| `angle_separation_arcsec` | Float | Angular distance in arcseconds |

## Examples

### Python

```python
import requests

obs_list = [
    "     K10CM6D  C2023 05 16.43686615 56 36.807-23 12 43.67         21.55wX~6o8oF51"
]

request = {
    'obs': obs_list,
    'time_separation_s': 60,
    'angle_separation_arcsec': 5
}

response = requests.get("https://data.minorplanetcenter.net/api/cnd", json=request)

if response.ok:
    result = response.json()
    for obs_query, matches in result.get('results', {}).items():
        if matches:
            print(f"Found {len(matches)} near-duplicate(s)")
            for match in matches:
                print(f"  Time: {match['time_separation_s']}s")
                print(f"  Angle: {match['angle_separation_arcsec']} arcsec")
        else:
            print("No duplicates found")
else:
    print("Error:", response.status_code)
```

### curl

```bash
curl -X GET -H "Accept: application/json" \
  https://data.minorplanetcenter.net/api/cnd \
  -H "Content-type: application/json" \
  -d '{"obs": ["     K10CM6D  C2023 05 16.43686615 56 36.807-23 12 43.67         21.55wX~6o8oF51"]}'
```

## Use Cases

- Check if observations have already been submitted to the MPC
- Identify potential duplicate observations in your data before submission
- Verify that your observations are unique

## Notes

- Exact matches appear in results even with minor numerical RA/dec differences
- The matching criteria require both time AND angle thresholds to be satisfied
