# Pointing submissions

The Minor Planet Center (MPC) collects data on **pointings**, i.e. information describing the direction, time, duration, and geometry of each exposure.

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
   At (or near) the time of exposure

2. **Queued pointings**  
   Scheduled observations

3. **Negative observations**  
   Targeted observations where the object was *not found*

---

## Submission format

Pointings must be submitted as a **JSON file**.

> An API for querying the database will be made available separately.

---

## Documentation

For the full specification, examples, and submission methods, see:

- [Pointing submissions documentation](negative_observations.md)

---

## Minimal valid JSON

```json
{
  "action": "exposed",
  "surveyExpName": "test001",
  "mode": "survey",
  "mpcCode": "111",
  "time": "2026-01-01T00:00:00.0",
  "duration": 30,
  "center": [10.0, -10.0],
  "width": 1.0,
  "limit": 20.0
}
```

---

## Test submission

You may use the form below to test your JSON.

It performs validation and inserts the data with an `ignore=1` flag (test mode).

Do not use this form for real data.

<form action="https://www.minorplanetcenter.net/cgi-bin/pointings/submit_negativeObs" method="post">
  <div>
    <label for="json"><b>Pointing data (JSON):</b></label><br>
    <textarea id="json" name="json" rows="20" cols="80">{
  "action": "exposed",
  "surveyExpName": "test001",
  "mode": "survey",
  "mpcCode": "111",
  "time": "2026-01-01T00:00:00.0",
  "duration": 30,
  "center": [10.0, -10.0],
  "width": 1.0,
  "limit": 20.0
}</textarea>
  </div>
  <br>
  <div style="margin-top: 12px;">
    <input type="submit" value="Submit test JSON">
  </div>
</form>

---

## Notes

- The browser form submits to the standard endpoint.
- Form-based test submissions are inserted with `ignore=1`.
- Direct JSON POST submissions are treated as normal submissions.
