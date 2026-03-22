"""Orbits API mixin."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from ._base import _MixinBase
from ._requests import _validate
from .exceptions import MPCValidationError
from ._requests import DictCompatModel


# ---------- Request model ----------

class OrbitRequest(BaseModel):
    desig: str

    @field_validator("desig")
    @classmethod
    def _desig_not_empty(cls, v):
        if not v:
            raise ValueError("desig must be a non-empty string")
        return v


# ---------- Response models ----------

class OrbitalCoefficients(DictCompatModel):
    """A set of orbital coefficients (cometarian or Cartesian)."""

    model_config = ConfigDict(extra="allow")

    coefficient_names: List[str]
    """Names of the orbital elements in order
    (cometarian: ``['q', 'e', 'i', 'node', 'argperi', 'tp']``;
    Cartesian: ``['x', 'y', 'z', 'vx', 'vy', 'vz']``)."""

    coefficient_values: List[float]
    """Fitted values for each orbital element in SI/au/deg units."""

    coefficient_uncertainties: Optional[List[float]] = None
    """1-σ uncertainties on each element, if available."""


class DesignationData(DictCompatModel):
    """Designation metadata embedded in an orbital elements record."""

    model_config = ConfigDict(extra="allow")

    permid: Optional[str] = None
    """Permanent object number as a string (e.g. ``"1"`` for Ceres)."""

    packed_primary_provisional_designation: Optional[str] = None
    """Packed MPC provisional designation (e.g. ``"I01A00A"``)."""

    unpacked_primary_provisional_designation: Optional[str] = None
    """Human-readable provisional designation (e.g. ``"A801 AA"``)."""


class MagnitudeData(DictCompatModel):
    """Photometric parameters for a solar-system object."""

    model_config = ConfigDict(extra="allow")

    H: Optional[float] = None
    """Absolute magnitude in the V band."""

    G: Optional[float] = None
    """Slope parameter for the H–G magnitude system (Bowell et al. 1989)."""


class OrbitalElements(DictCompatModel):
    """Orbital elements for a solar-system object (``mpc_orb`` structure).

    All fields beyond the declared ones are preserved and accessible
    via attribute or dict-style access.
    """

    model_config = ConfigDict(extra="allow")

    COM: Optional[OrbitalCoefficients] = None
    """Cometarian (perihelion-based) orbital elements."""

    CAR: Optional[OrbitalCoefficients] = None
    """Cartesian state-vector elements."""

    designation_data: Optional[DesignationData] = None
    """Designation and identification metadata."""

    magnitude_data: Optional[MagnitudeData] = None
    """Absolute magnitude and slope parameter."""


class OrbitsMixin(_MixinBase):

    def get_orbit(self, desig: str) -> Optional[OrbitalElements]:
        """Retrieve orbital elements for an object.

        Returns an :class:`~mpc_client.models.OrbitalElements` instance, or
        ``None`` if the object was not found (the API returns an empty list
        rather than a 404 for unknown designations).

        Parameters
        ----------
        desig : str
            Object designation (name, number, or provisional designation).

        Returns
        -------
        OrbitalElements or None
            The orbital elements, or ``None`` if not found.
        """
        req = _validate(OrbitRequest, desig=desig)
        result = self._get("/api/get-orb", json={"desig": req.desig})
        if (
            isinstance(result, list)
            and result
            and "mpc_orb" in result[0]
            and result[0]["mpc_orb"]
        ):
            return OrbitalElements(**result[0]["mpc_orb"][0])
        return None

    def get_orbit_raw(self, desig: str) -> List[Dict[str, Any]]:
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
        req = _validate(OrbitRequest, desig=desig)
        return self._get("/api/get-orb", json={"desig": req.desig})
