# Check Near-Duplicates (CND) API

The Check Near-Duplicates API can search for near-duplicates of observations published publicly in the Minor Planet Center database. A near-duplicate is an observation with similar temporal and angular positions to an existing observation.

## Endpoint

```
https://data.minorplanetcenter.net/api/cnd
```

**Method:** GET

## Parameters

| Parameter | Type | Required | Description                                                                                                                                          | Default |
|-----------|------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `obs` | List of strings | Yes | 80- or 160-character observation records in the [MPC1992 format](https://minorplanetcenter.net/iau/info/ObsFormat.html).                             | NA      |
| `time_separation_s` | Float | No | Temporal threshold (0-60 seconds). Matching observations will have been recorded within this time span with respect to the given observation.        | 60      |
| `angle_separation_arcsec` | Float | No | Spatial threshold (0-10 arcseconds). Matching observations will have been recorded within this angular radius with respect to the given observation. | 5       |
| `omit_separation` | Boolean | No | Exclude calculated separation values from results.                                                                                                   | false   |

!!! note
    160-character "two-line" observations may be concatenated, or the 80-character parts may be in sequential order.

**Limits:**

- Up to 10,000 observations per request.
- Searches against publicly published MPC observations only.

## Response Format

The original request will be included in a `request` attribute. 

An attribute for each search term is included in the `results` attribute. Note that if the search term is in our database and published, it will always be returned as one of the results. This is called an 'exact' match.

!!! note
    Exact matches may occasionally show non-zero angular separation values. This is due to the numerical difference between the RA/dec values stored in the database and those given in the obs80 string.


The value associated with each search term is a list of dictionaries, giving data about the matching observations. The fields of each match are described below.

| Field | Description |
|-------|-------------|
| `request` | Echo of the original query parameters |
| `results` | Dictionary mapping each input observation to matching near-duplicates |

Each match includes:

| Field | Type | Description |
|-------|------|-------------|
| `obs80` | String | The 80- or 160- character observation record deemed to be a near-duplicate. |
| `time_separation_s` | Float | The temporal separation in seconds between the duplicate and the search term. |
| `angle_separation_arcsec` | Float | The angular separation in arcseconds between the duplicate and the search term. |

## Examples

### Python

```python
import requests

obs = [
    '     K10CM6D  C2023 05 16.43686615 56 36.807-23 12 43.67         21.55wX~6o8oF51',
    '     K10HB1E  S2010 04 24.76254008 07 33.34 -16 07 52.4                W     C51',
    '     K10HB1E  s2010 04 24.7625401 - 3527.1820 + 5686.2015 - 1729.5218        C51'
]

request = {
    'obs': obs,
    'time_separation_s': 60,
    'angle_separation_arcsec': 5
}

response = requests.get("https://data.minorplanetcenter.net/api/cnd", json=request)
response.raise_for_status()
near_duplicates = response.json()['results']
```

### cURL

```bash
curl -X GET -H "Accept: application/json" \
  https://data.minorplanetcenter.net/api/cnd \
  -H "Content-type: application/json" \
  -d '{"obs": ["     K10CM6D  C2023 05 16.43686615 56 36.807-23 12 43.67         21.55wX~6o8oF51"]}'
```
