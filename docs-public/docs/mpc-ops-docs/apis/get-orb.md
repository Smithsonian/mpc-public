# Orbits API

The Orbits API returns orbital elements and related parameters for solar system objects in the `mpc_orb` JSON format.

## Endpoint

```
https://data.minorplanetcenter.net/api/get-orb
```

**Method:** GET

## Parameters

| Parameter       | Type            | Required | Description                                                                                    | Default     |
|-----------------|-----------------|----------|------------------------------------------------------------------------------------------------|-------------|
| `desig`         | String          | Yes      | Name, permanent or provisional designation                                                     | NA          |

!!! note
    You may use any designation format supported by the [Designation Identifier API](./query-identifier.md). Currently, the Orbits API is limited to single object queries.

## Response Format

At a high level, the Orbits API returns a list containing:

| List Item   | Type       | Description                                |
|-------------|------------|--------------------------------------------|
| Orbit       | Dictionary | Dictionary containing an `mpc_orb` object. |
| Status Code | Integer    | 200                                        |

## Examples

### Python

```python
import requests

response = requests.get(
    "https://data.minorplanetcenter.net/api/get-orb",
    json={"desig": "123456"}
)
response.raise_for_status()
mpc_orb = response.json()[0]['mpc_orb'][0]
```

**Output `mpc_orb` Dictionary**

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

### cURL

```bash
curl -X GET -H "Content-Type: application/json" \
  -d '{"desig": "13270"}' \
  https://data.minorplanetcenter.net/api/get-orb
```

## Working with the `mpc_orb` Format

The MPC maintains a public GitHub repository with a pip-installable package for reading, validating, and writing `MPC_ORB` JSON files:

- [`mpc_orb` on GitHub](https://github.com/Smithsonian/mpc-public/tree/main/mpc_orb)
- [`mpc-orb` on PyPI](https://pypi.org/project/mpc-orb/)
- [`MPC_ORB` JSON Documentation](https://minorplanetcenter.net/mpcops/documentation/mpc-orb-json/)

```bash
pip install mpc-orb
```

## See Also

- [Orbital Elements Documentation](../orbits.md)
