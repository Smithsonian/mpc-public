"""MPECs (Minor Planet Electronic Circulars) API mixin."""

from .exceptions import MPCValidationError


class MPECsMixin:

    def get_mpecs(self, search_terms):
        """Search for Minor Planet Electronic Circulars.

        Parameters
        ----------
        search_terms : str or list of str
            Object designation(s), MPEC name(s), or wildcard pattern(s)
            (using ``%`` for wildcards).

        Returns
        -------
        dict
            Mapping of each search term to a list of MPEC dicts
            (keys: ``fullname``, ``title``, ``pubdate``, ``link``).
        """
        if isinstance(search_terms, str):
            search_terms = [search_terms]
        if not search_terms:
            raise MPCValidationError("search_terms must be a non-empty string or list")
        return self._get("/api/mpecs", json=search_terms)

    def get_discovery_mpec(self, designation):
        """Get the discovery MPEC for an object (the earliest by publication date).

        Parameters
        ----------
        designation : str
            Object designation.

        Returns
        -------
        dict or None
            The earliest MPEC dict, or ``None`` if none found.
        """
        result = self.get_mpecs(designation)
        mpecs = result.get(designation, [])
        if not mpecs:
            return None
        return sorted(mpecs, key=lambda m: m.get("pubdate", ""))[0]
