"""Designation Identifier API mixin."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator

from ._base import _MixinBase
from ._requests import _validate


# ---------- Request model ----------

class IdentifierRequest(BaseModel):
    ids: List[str]

    @field_validator("ids", mode="before")
    @classmethod
    def _coerce_and_check_ids(cls, v):
        if isinstance(v, str):
            if not v:
                raise ValueError("ids must be a non-empty string or list")
            v = [v]
        if not v:
            raise ValueError("ids must be a non-empty string or list")
        return v


# ---------- Response model ----------

class DesignationInfo(BaseModel):
    """Designation look-up result for a single queried identifier."""

    model_config = ConfigDict(extra="allow")

    found: Optional[int] = None
    """1 if the identifier was resolved, 0 otherwise."""

    permid: Optional[str] = None
    """Permanent identifier (object number as a string), if assigned."""

    name: Optional[str] = None
    """IAU-approved name, if assigned."""

    iau_designation: Optional[str] = None
    """IAU designation string (e.g. ``"(90377)"`` for numbered objects)."""

    object_type: Optional[List[Any]] = None
    """Two-element list ``[type_name (str), type_code (int)]`` classifying the object."""


class IdentifierMixin(_MixinBase):

    def identify(self, ids: Union[str, List[str]]) -> Dict[str, DesignationInfo]:
        """Look up designation information for one or more objects.

        Parameters
        ----------
        ids : str or list of str
            Object identifier(s) — names, numbers, or provisional designations.

        Returns
        -------
        dict
            Mapping of each queried identifier to its
            :class:`~mpc_client.models.DesignationInfo`.
        """
        req = _validate(IdentifierRequest, ids=ids)
        raw = self._get("/api/query-identifier", json={"ids": req.ids})
        return {k: DesignationInfo(**v) for k, v in raw.items()}
