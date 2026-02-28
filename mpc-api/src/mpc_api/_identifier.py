"""Designation Identifier API mixin."""

from .exceptions import MPCValidationError


class IdentifierMixin:

    def identify(self, ids):
        """Look up designation information for one or more objects.

        Parameters
        ----------
        ids : str or list of str
            Object identifier(s) — names, numbers, or provisional designations.

        Returns
        -------
        dict
            Mapping of each queried identifier to its designation data.
        """
        if isinstance(ids, str):
            if not ids:
                raise MPCValidationError("ids must be a non-empty string or list")
            ids = [ids]
        if not ids:
            raise MPCValidationError("ids must be a non-empty string or list")
        return self._get("/api/query-identifier", json={"ids": ids})
