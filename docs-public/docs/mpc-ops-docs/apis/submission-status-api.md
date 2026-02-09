# Submission Status API

The Submission Status API allows you to check whether a submission has been accepted by the MPC, and if not, what errors occurred.

## Endpoint

```
https://data.minorplanetcenter.net/api/submission-status
```

**Method:** GET

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `submission_id` | String | Yes | The submission ID received when observations were submitted |

**Example request:**

```json
{"submission_id": "2026-01-01T00:05:07.453_0000BhCE"}
```

## Response Fields
The response will return a 404 error code if the submission ID does not exist.

If the submission does exist, the response will be a JSON object with the following structure:

| Field | Type | Description                                                              |
|-------|------|--------------------------------------------------------------------------|
| `accepted` | Boolean | Whether the submission was accepted by the ingest stage.                 |
| `pipeline_entry_time` | String (ISO8601) or null | Timestamp when data entered MPC pipeline processing, or null if pending. |
| `fault_events` | List | Log of problems encountered during ingest                                |

Each fault event is a JSON object with the following fields:

| Field | Type     | Description                |
|-------|----------|----------------------------|
| `message` | String | Human-readable event description. |
| `phase` | Integer (non-negative) | Processing stage identifier |
| `failure_code` | Integer (non-zero) | Fault classification code |

!!! note
    The `fault_events` list may be non-empty even if `accepted` is `true`. In that case, any events represent warnings that did not prevent the acceptance of the submission. Every submission where accepted is false should have at least one event log entry indicating the problem. Currently, neither `failure_code` nor `phase` values are documented, nor are they guaranteed to remain stable.

## Examples

### Python - Accepted Submission

```python
import requests

req = {"submission_id": "2026-01-01T00:05:07.453_0000BhCE"}
resp = requests.get("https://data.minorplanetcenter.net/api/submission-status", json=req)
resp.raise_for_status()
print(resp.json())
```

**Output:**

```json
{
    "accepted": true,
    "pipeline_entry_time": "2026-01-01T00:06:00.696565+00:00",
    "fault_events": []
}
```

### Python - Rejected Submission

```python
import requests

req = {"submission_id": "2025-11-12T21:11:49.579_0000Ba8V"}
resp = requests.get("https://data.minorplanetcenter.net/api/submission-status", json=req)
resp.raise_for_status()

result = resp.json()
print(f"Accepted: {result['accepted']}")
for event in result["fault_events"]:
    print(f"* fault (code {event['failure_code']}): {event['message']}")
```

**Output:**

```json
{
    "accepted": false,
    "pipeline_entry_time": null,
    "fault_events": [
        {
            "message": "exact duplicate of submission 2025-11-12T21:09:16.359_0000Ba8U",
            "phase": 2,
            "failure_code": 5
        },
        {
            "message": "ingest failed",
            "phase": 2,
            "failure_code": 7
        }
    ]
}
```

### Non-existent Submission

If you query a submission ID that doesn't exist, the API returns a 404 error.

## See Also

- [Submission API](submission-api.md) - How to submit observations
