# Orbits API

The Orbits API returns orbital elements and related parameters for solar system objects in the `mpc_orb` JSON format.

## Endpoint

```
https://data.minorplanetcenter.net/api/get-orb
```

**Method:** GET

## Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `desig` | String | Yes | Name, permanent or provisional designation | None |

Both packed and unpacked designation formats are supported. Currently limited to single object queries.

## Response Format

The response is in the `mpc_orb` JSON format, containing:

| Field | Type | Description |
|-------|------|-------------|
| `mpc_orb` | List of dicts | Orbital elements and orbit-related parameters for the standard epoch orbit |

The `mpc_orb` format includes:

- Cartesian state vectors (CAR)
- Orbital uncertainties and covariance matrix
- Epoch information
- Designation data

## Examples

### Python

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-orb",
    json={"desig": "123456"}
)

if response.ok:
    mpc_orb = response.json()[0]['mpc_orb'][0]
    print(mpc_orb)
else:
    print("Error:", response.status_code, response.content)
```

**Output:**

```python
{
    'CAR': {
        'coefficient_names': ['x', 'y', 'z', 'vx', 'vy', 'vz'],
        'coefficient_uncertainties': [4.1878e-08, 6.33631e-08, ...],
        'coefficient_values': [2.22157355733413, -0.248953026079381, ...],
        'covariance': {'cov00': 1.753769379695109e-15, ...},
        'eigenvalues': [5.13405e-12, 1.08044e-10, ...],
        ...
    },
    ...
}
```

### curl

```bash
curl -X GET -H "Content-Type: application/json" \
  -d '{"desig": "13270"}' \
  https://data.minorplanetcenter.net/api/get-orb
```

## Working with mpc_orb Format

The MPC maintains a public GitHub repository with a pip-installable package for reading, validating, and writing MPC_ORB JSON files:

- [mpc_orb on GitHub](https://github.com/Smithsonian/mpc-public/tree/main/mpc_orb)
- [mpc_orb on PyPI](https://pypi.org/project/mpc-orb/)

```bash
pip install mpc-orb
```

## See Also

- [MPC_ORB JSON Documentation](../orbital-elements.md)
