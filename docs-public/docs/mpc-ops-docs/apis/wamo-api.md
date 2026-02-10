# WAMO API (Where Are My Observations)

The WAMO API helps investigate individual observations. It can be used to check the status of submitted observations. 

The [Original WAMO Tool][wamo] leverages this API behind the scenes.

[wamo]: https://minorplanetcenter.net/wamo/

## Endpoint

```
https://data.minorplanetcenter.net/api/wamo
```

**Method:** GET

## Input Formats

You can query the API with up to ~50k identifiers. Each identifier may return up to 100k observations. 

!!! note
    **Astrometry will be suppressed for unpublished observations.**

The following identifier formats are accepted (can be mixed):

### 1. Tracklet Submission ID (`trksub`) and Station Code (`stn`)

If you submitted with ADES, or don't have a unique observation ID, specify your `trkSub` and `stn` code, separated by a space:

```
5T0D452 703
```

### 2. Observation ID (`obsid`)

If you received an acknowledgement message with unique observation IDs:

```
L4eBVG000000CfiO010000A9a
```

### 3. MPC 1992 80- or 160-column Observation String (`obs80`)

If you submitted in the MPC 1992 80- or 160-column format, paste the observation exactly as originally submitted:

```
29149         C2005 10 10.39002 02 57 12.16 +09 01 47.3          16.5 Vro5016703
```

### 4. Submission Block ID

If you have submission block identifiers available:

```
2024-05-02T21:03:35.001_0000FzZw_01
```

## Query Payload Formats

You can query the API in two ways:

**1. List of observations (returns JSON):**

```python
['5T0D452 703', 'L4eBVG000000CfiO010000A9a']
```

**2. With a `"string"` element:**

Including this "magic" element returns the same text as the [Original WAMO Tool][wamo].

```python
['string', '5T0D452 703', 'L4eBVG000000CfiO010000A9a']
```

The `"string"` item can be in any position of the list.

## Examples

### cURL

```bash
curl -X GET -H "Accept: application/json" \
  https://data.minorplanetcenter.net/api/wamo \
  -H "Content-type: application/json" \
  -d '["5T0D452 703", "L4eBVG000000CfiO010000A9a"]'
```

### Python

```python
import requests

url = "https://data.minorplanetcenter.net/api/wamo"
obs_list = ['P11JuVG F51']
response = requests.get(url, json=obs_list)
response.raise_for_status()
wamo_response = response.json()

# To get the original WAMO string format:
response = requests.get(url, json=['string'] + obs_list)
response.raise_for_status()
wamo_response = response.text
```

## See Also

- [Original WAMO Tool][wamo]
- [WAMO Help](https://minorplanetcenter.net/wamo/help.html)
