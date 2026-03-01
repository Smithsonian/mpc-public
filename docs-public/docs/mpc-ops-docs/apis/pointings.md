# Pointings API

The MPC Pointings Database collects details about telescope exposures — direction, timing, duration, and field geometry — relevant to the near-Earth object (NEO) community. The database facilitates:

- Community coordination of NEO follow-up activities
- Internal MPC data processing
- Community pre-recovery efforts

Two types of pointing information are collected:

- **Exposed pointings** — recorded at or near the actual time of exposure
- **Queued pointings** — scheduled observations (future capability)

## Endpoint

```
https://www.minorplanetcenter.net/cgi-bin/pointings/submit
```

**Method:** POST

**Content-Type:** `application/json`

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `action` | String | Must be `"exposed"`. Future versions will allow `"queued"`. |
| `surveyExpName` | String | Unique identifier for this exposure within the survey. Max 64 characters, no spaces. |
| `mode` | String | `"survey"` or `"target"` |
| `mpcCode` | String | MPC-assigned 3 or 4-character site code |
| `time` | String | UTC date and time of the beginning of the exposure: `YYYY-MM-DDThh:mm:ss.sss` |
| `duration` | Numeric | Length of the exposure in seconds |
| `center` | List | Right ascension and declination of the field center in decimal degrees (J2000 equinox). Use 4-8 decimal places for RA and Dec. |
| `limit` | Numeric | Faintest magnitude for which astrometric measurements can be made (typically five sigma) |
| `desig` | String | Target designation. Required when `mode` is `"target"`. |

## Field Geometry

Exactly **one** of the following fields must be provided to describe the field shape:

| Field | Type | Description |
|-------|------|-------------|
| `width` | Numeric | Side length of a square, equatorially-aligned field (degrees) |
| `widths` | List | Side lengths `[RA, Dec]` of a rectangular, equatorially-aligned field (degrees) |
| `fieldDiam` | Numeric | Diameter of a circular field (degrees) |
| `offsets` | List | Tangent plane offsets (w.r.t. field center) of field corners as four `[RA, Dec]` ordered pairs (degrees) |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `filter` | String | Short name for the bandpass. Use `"UNFILTERED"` if no filter was used. No spaces. |
| `nonsidereal` | Boolean | Set to `true` if the exposure was not tracked sidereally. Defaults to `false`. |

## Examples

### Square Survey Field

```json
{
    "action": "exposed",
    "surveyExpName": "AK101_Jxpf341-a",
    "mode": "survey",
    "mpcCode": "802",
    "time": "2018-01-01T11:22:33.4567",
    "duration": 120,
    "center": [255.1667, -29.0079],
    "width": 2.5,
    "limit": 19.5,
    "filter": "r"
}
```

### Circular Field

```json
{
    "action": "exposed",
    "mode": "survey",
    "mpcCode": "802",
    "time": "2018-01-01T11:22:33.456",
    "duration": 30,
    "center": [255.167, -29.008],
    "fieldDiam": 2.45,
    "limit": 22,
    "filter": "zp1"
}
```

### Field Corners with Tangent-Plane Offsets

```json
{
    "action": "exposed",
    "surveyExpName": "Kg101_abc23112233p456",
    "mode": "survey",
    "mpcCode": "802",
    "time": "2018-01-01T11:22:33.456",
    "duration": 30,
    "center": [255.167, -29.008],
    "offsets": [[1.25, -1.25], [-1.25, -1.25], [1.25, 1.25], [-1.25, 1.25]],
    "limit": 22,
    "filter": "r"
}
```

### Targeted Follow-Up (Rectangular Field, Non-Sidereal)

```json
{
    "action": "exposed",
    "surveyExpName": "20180101-EX0132",
    "mode": "target",
    "mpcCode": "802",
    "time": "2018-01-01T11:22:33.456",
    "duration": 300,
    "center": [255.167, -29.008],
    "widths": [0.82, 0.64],
    "desig": "K18A00A",
    "limit": 23.5,
    "nonsidereal": true,
    "filter": "VR"
}
```

### cURL

```bash
cat json.txt
{"action": "exposed", "mode": "survey", "mpcCode": "802", "time": "2018-01-01T11:22:33.234",
"center": [11.11, -22.22], "width": 2.2, "limit": 20.5}

curl -X POST -H "Content-Type: application/json" \
  -d @json.txt https://www.minorplanetcenter.net/cgi-bin/pointings/submit
```

**Response:**

```json
{"response": "Inserted new record with ID=3708893"}
```

### Python

```python
import http.client
import json

observation = {
    "action": "exposed",
    "mode": "survey",
    "mpcCode": "802",
    "time": "2017-02-06T10:00:57.2",
    "duration": 15.00,
    "center": [140.1945, 20.3632],
    "width": 2.4,
    "limit": 20.5,
    "surveyExpName": "A123xyz006",
}

jsontxt = json.dumps(observation)

headers = {"Content-type": "application/json"}
conn = http.client.HTTPSConnection("www.minorplanetcenter.net")
conn.request("POST", "/cgi-bin/pointings/submit", jsontxt, headers)
response = conn.getresponse()
print(response.status, response.reason, response.read())
```

## See Also

- [Pointing Data](../data-and-services/pointing-data.md) — accessing raw pointing files used for Sky Coverage plots
