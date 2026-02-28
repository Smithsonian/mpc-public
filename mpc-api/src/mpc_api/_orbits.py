"""Orbits API mixin."""

from .exceptions import MPCValidationError


class OrbitsMixin:

    def get_orbit(self, desig):
        """Retrieve orbital elements for an object.

        Returns the ``mpc_orb`` dict directly, or ``None`` if the
        object was not found (the API returns an empty list rather
        than a 404 for unknown designations).

        Parameters
        ----------
        desig : str
            Object designation (name, number, or provisional designation).

        Returns
        -------
        dict or None
            The ``mpc_orb`` dictionary, or ``None`` if not found.
        """
        if not desig:
            raise MPCValidationError("desig must be a non-empty string")
        result = self._get("/api/get-orb", json={"desig": desig})
        if (
            isinstance(result, list)
            and result
            and "mpc_orb" in result[0]
            and result[0]["mpc_orb"]
        ):
            return result[0]["mpc_orb"][0]
        return None

    def get_orbit_raw(self, desig):
        """Retrieve the full, unprocessed API response for an orbit query.

        Parameters
        ----------
        desig : str
            Object designation.

        Returns
        -------
        list
            Raw JSON response from the API.
        """
        if not desig:
            raise MPCValidationError("desig must be a non-empty string")
        return self._get("/api/get-orb", json={"desig": desig})
