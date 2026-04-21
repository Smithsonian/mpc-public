# Pointings submissions and negative observations

The Minor Planet Center (MPC) collects data on **pointings**, i.e. information describing the direction, time, duration, etc. of each exposure.

A pointing corresponds to an **individual image** (not a multi-exposure field).

We welcome submissions from:
- Large surveys
- Targeted follow-up observations
- Negative observations

---

## Purpose

Collecting pointing data enables:
1. Community coordination of NEO follow-up
2. Internal MPC data processing
3. Community precovery

---

## Types of pointings

We collect three types:

1. **Exposed pointings**  
   → At (or near) time of exposure

2. **Queued pointings**  
   → Scheduled observations

3. **Negative observations**  
   → Targeted observation where object was *not found*

---

## Submission format

Pointings must be submitted as a **JSON file**.

> An API for querying the database will be available soon.

---

## Contents

- [JSON Field Names](#json-field-names)
- [Negative Observations JSON](#negative-observations-json)
- [JSON Examples](#json-examples)
- [Submission Examples](#submission-examples)

---

## JSON Field Names

### Mandatory fields

- `action` — `"exposed"` *(string)*
- `surveyExpName` — unique exposure ID *(string, ≤64 chars, no spaces)*
- `mode` — `"survey"` or `"target"` *(string)*
- `mpcCode` — MPC site code *(string)*
- `time` — `"YYYY-MM-DDThh:mm:ss.sss"` *(string, UTC)*
- `duration` — exposure length in seconds *(number)*
- `center` — `[RA, Dec]` in decimal degrees *(list)*
- `limit` — limiting magnitude *(number)*
- `desig` — required if `mode="target"` *(string)*

---

### Field geometry (choose exactly ONE)

- `width` — square field size *(number)*
- `widths` — `[ra, dec]` rectangular field *(list)*
- `fieldDiam` — circular field diameter *(number)*
- `offsets` — list of 4 corner offsets *(list of pairs)*

---

### Optional fields

- `filter` — bandpass (use `"UNFILTERED"` if none)
- `nonsidereal` — `true` / `false`

---

### Negative Observations: Additional mandatory fields

- `found` — boolean
- `desig` — object designation or trksub
- `submitter` — name of reporter

---

### Negative Observations: Additional optional fields

- `limiting_mag_method` — 1–4
- `notes`
- `number_of_stars_fov`
- `pixel_scale`
- `seeing`
- `software`
- `stacked`
- `fill_factor`

---

### Negative Observations: Limiting magnitude methods

1. Star stack → scale to 5σ  
2. Sky noise → scale to point source  
3. Inject artificial objects (50% detection efficiency)  
4. Manual/custom  

---

## JSON Examples

### Exposed Square Field (survey)

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

### Exposed Circular Field (survey)
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
### Exposed Field (Defined by Offsets)
```json
{
  "action": "exposed",
  "surveyExpName": "Kg101_abc23112233p456",
  "mode": "survey",
  "mpcCode": "802",
  "time": "2018-01-01T11:22:33.456",
  "duration": 30,
  "center": [255.167, -29.008],
  "offsets": [[1.25,-1.25],[-1.25,-1.25],[1.25,1.25],[-1.25,1.25]],
  "limit": 22,
  "filter": "r"
}
```

### Targeted observation
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

### Negative observation
```json
{
  "action": "exposed",
  "surveyExpName": "20180101-EX0132",
  "mode": "target",
  "mpcCode": "I52",
  "time": "2024-03-03T12:20:33.46",
  "duration": 45,
  "center": [255.167, -29.008],
  "widths": [0.82, 0.64],
  "desig": "P11Uypl",
  "limit": 22.7,
  "nonsidereal": true,
  "filter": "V",
  "found": false,
  "submitter": "A. Tomatic",
  "fill_factor": 0.98
}
```

### Submission Examples

#### Command-line (using `curl`)
```bash
URL='https://www.minorplanetcenter.net/cgi-bin/pointings/submit_negativeObs'

curl -X POST \
  -H "Content-Type: application/json" \
  -d @json.txt \
  $URL

### Test form

You can test JSON submissions using the MPC test endpoint:

https://www.minorplanetcenter.net/cgi-bin/pointings/submit_negativeObs

Test submissions are flagged as ignored.