# Action Codes API

Action codes are automatically generated and sent to the submitters of new NEO and new comet candidates as well as to the NEO/NEOPC follow-up reporters. Action codes are used to retract or replace submitted observations. The Action Codes API allows you to request that your action codes be resent to your original email address. The codes can then be used at the [MPC action codes submission page](https://www.minorplanetcenter.net/submit_action_code).

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

| Format | Example | Regex | Description |
|--------|---------|-------|-------------|
| trksub | `A10cnQO` | `^[-A-Za-z0-9_]{1,8}$` | Tracklet submission ID (1-8 alphanumeric characters) |
| trkid | `00000DwbEz` | `^[-A-Za-z0-9_]{8,12}$` | Track ID (8-12 alphanumeric characters) |
| submission block id | `2024-05-02T21:03:35.001_0000FzZw_01` | `^\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-6]\d\.\d{3}_\w{8}_\d{2}$` | Full submission block identifier |
| submission id | `2024-05-02T21:03:35.001_0000FzZw` | `^\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-6]\d\.\d{3}_\w{8}$` | Submission identifier |

## Response

The response will be intentionally minimal (vacuous), but you should expect that an email was sent to the original submitter's address.

**Important:** Action codes are sent via email to the original submitter's email address. They are NOT returned in the API response.

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

### curl

```bash
curl -X POST -H "Accept: application/json" \
  https://data.minorplanetcenter.net/api/action-codes/retrieve \
  -H "Content-type: application/json" \
  -d '{"label": "[your-label]"}'
```

## What Are Action Codes?

Action Codes are sent to users who submit observations with email addresses on file. They allow you to:

- Retract (delete) submitted observations
- Replace observations with corrected versions
- Prove ownership of submissions

If you've lost your action code, this API allows you to have it resent to your original email address.

## Using Action Codes

After receiving your action code, you can use it at the [MPC Action Codes Submission Page](https://www.minorplanetcenter.net/submit_action_code).

## See Also

- [MPC Action Codes Submission Page](https://www.minorplanetcenter.net/submit_action_code)
