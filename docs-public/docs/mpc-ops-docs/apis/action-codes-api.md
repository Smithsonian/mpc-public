# Action Codes API

Action Codes are sent to users who submit observations with email addresses on file. Understandably, these are occasionally lost. The Action Codes API allows users to resend their action codes to the original email address the submission was made with. The codes can then be used at the [MPC action codes submission page](https://www.minorplanetcenter.net/submit_action_code).

## What Are Action Codes?

Action Codes are sent to users who submit observations with email addresses on file. They allow you to:

- Retract (delete) submitted observations
- Label objects as artificial or comets.

## Endpoint

```
https://data.minorplanetcenter.net/api/action-codes/retrieve
```

**Method:** POST

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `label` | String | Yes | Identifier for the submission |

### Label Formats

The following identifier formats are accepted:

| Format | Example | Regex | Description                 |
|--------|---------|-------|-----------------------------|
| trksub | `A10cnQO` | `^[-A-Za-z0-9_]{1,8}$` | Tracklet submission ID      |
| trkid | `00000DwbEz` | `^[-A-Za-z0-9_]{8,12}$` | Tracklet ID                 |
| submission block id | `2024-05-02T21:03:35.001_0000FzZw_01` | `^\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-6]\d\.\d{3}_\w{8}_\d{2}$` | Submission block identifier |
| submission id | `2024-05-02T21:03:35.001_0000FzZw` | `^\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-6]\d\.\d{3}_\w{8}$` | Submission identifier       |

## Response

The response will be intentionally vacuous, but you should expect that an email was sent to the original submitter's address.

!!! note
    Action codes are sent via email to the original submitter's email address. They are NOT returned in the API response to preserve privacy.

## Examples

### Python

```python
import requests
import json
import sys

terms = {'label': '[your-label]'}
response = requests.post(
    "https://data.minorplanetcenter.net/api/action-codes/retrieve",
    json=terms
)
response.raise_for_status()
json.dump(response.json(), sys.stdout, indent=4)  # Response is minimal
```

### cURL

```bash
curl -X POST -H "Accept: application/json" \
  https://data.minorplanetcenter.net/api/action-codes/retrieve \
  -H "Content-type: application/json" \
  -d '{"label": "[your-label]"}'
```
