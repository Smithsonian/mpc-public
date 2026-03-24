"""MPECs (Minor Planet Electronic Circulars) API mixin."""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, field_validator

from ._base import _MixinBase
from ._requests import _validate

# ---------- Request model ----------


class MPECsRequest(BaseModel):
    search_terms: List[str]

    @field_validator("search_terms", mode="before")
    @classmethod
    def _coerce_and_check_terms(cls, v):
        if isinstance(v, str):
            v = [v]
        if not v:
            raise ValueError("search_terms must be a non-empty string or list")
        return v


# ---------- Response model ----------


class MPEC(BaseModel):
    """A single Minor Planet Electronic Circular entry."""

    fullname: str
    """MPEC identifier (e.g. ``"2004-Y25"``)."""

    title: str
    """MPEC title."""

    pubdate: str
    """Publication date (ISO format string)."""

    link: str
    """URL to the full MPEC text."""


class MPECsMixin(_MixinBase):
    def get_mpecs(self, search_terms: Union[str, List[str]]) -> Dict[str, List[MPEC]]:
        """Search for Minor Planet Electronic Circulars.

        Parameters
        ----------
        search_terms : str or list of str
            Object designation(s), MPEC name(s), or wildcard pattern(s)
            (using ``%`` for wildcards).

        Returns
        -------
        dict
            Mapping of each search term to a list of
            :class:`~mpc_client.models.MPEC` entries.
        """
        req = _validate(MPECsRequest, search_terms=search_terms)
        raw = self._get("/api/mpecs", json=req.search_terms)
        # The API may return results nested under a "results" key
        results = raw.get("results", raw) if isinstance(raw, dict) else raw
        return {
            term: [MPEC(**m) for m in mpecs]
            for term, mpecs in results.items()
            if isinstance(mpecs, list)
        }

    def get_discovery_mpec(self, designation: str) -> Optional[MPEC]:
        """Get the discovery MPEC for an object (the earliest by publication date).

        Parameters
        ----------
        designation : str
            Object designation.

        Returns
        -------
        MPEC or None
            The earliest :class:`~mpc_client.models.MPEC`, or ``None`` if none found.
        """
        result = self.get_mpecs(designation)
        mpecs = result.get(designation, [])
        if not mpecs:
            return None
        return sorted(mpecs, key=lambda m: m.pubdate)[0]
