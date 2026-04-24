# Pointing submissions documentation

This page contains the field definitions, rules, examples, and submission methods for MPC pointings and negative observations.

---

## Contents

- [JSON Field Names](#json-field-names)
- [JSON Examples](#json-examples)
- [Submission Examples](#submission-examples)
- [Common mistakes](#common-mistakes)

---

## JSON Field Names

### Mandatory fields (All Pointing Types)

- `action` — `"exposed"` *(string)*
- `surveyExpName` — unique exposure ID *(string, up to 64 characters, no spaces)*
- `mode` — `"survey"` or `"target"` *(string)*
- `mpcCode` — MPC-assigned 3- or 4-character site code *(string)*
- `time` — UTC time in the format `"YYYY-MM-DDThh:mm:ss.sss"` *(string)*
- `duration` — exposure length in seconds *(number)*
- `center` — `[RA, Dec]` in decimal degrees *(list)*
- `limit` — limiting magnitude *(number)*
- `desig` — required if `mode="target"` *(string)*

---

### Field geometry (choose exactly ONE)

Exactly ONE of the following must be provided:

- `width` — side length of a square field *(number)*
- `widths` — `[ra, dec]` side lengths of a rectangular field *(list)*
- `fieldDiam` — diameter of a circular field *(number)*
- `offsets` — tangent-plane offsets of the four field corners *(list of pairs)*

---

### Optional fields

- `filter` — short name of the bandpass; use `"UNFILTERED"` if no filter
- `nonsidereal` — `true` or `false`

---


### Negative Observations: Additional mandatory fields

- `found` — boolean
- `desig` — object designation in packed format, or a trksub for NEOCP
- `submitter` — name of the submitter

### Negative Observations: Additional optional fields

- `limiting_mag_method` — integer in `{1,2,3,4}`
- `notes`
- `number_of_stars_fov`
- `pixel_scale`
- `seeing`
- `software`
- `stacked`
- `fill_factor`

---

### Negative Observations: Limiting magnitude methods

1. On star stack, measure faint objects at the limit and scale to 5-sigma.
2. On stack, measure sky noise, scale for a point-source area, and then to 5-sigma.
3. Insert artificial objects into frames and measure 50% detection efficiency.
4. Manual/custom method.

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
  "offsets": [[1.25, -1.25], [-1.25, -1.25], [1.25, 1.25], [-1.25, 1.25]],
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

---

#### Command-line (using `curl`)
```bash
URL='https://www.minorplanetcenter.net/cgi-bin/pointings/submit_negativeObs'

curl -X POST \
  -H "Content-Type: application/json" \
  -d @json.txt \
  $URL
```

### Test form

## Common mistakes

- Providing multiple geometry fields
- Missing `surveyExpName`
- Wrong time format
- Using spaces in `surveyExpName`
- Forgetting `desig` for target mode
