"""mpc_client — Python client for the Minor Planet Center APIs."""

from __future__ import annotations

__version__ = "0.1.0"

from .client import MPCClient
from .exceptions import (
    MPCAPIError,
    MPCRequestError,
    MPCResponseError,
    MPCNotFoundError,
    MPCValidationError,
)
from ._action_codes import ActionCodeResponse
from ._cnd import NearDuplicateMatch
from ._identifier import DesignationInfo
from ._mpecs import MPEC
from ._obscodes import Observatory
from ._observations import ObservationsResult
from ._orbits import OrbitalElements, OrbitalCoefficients, DesignationData, MagnitudeData
from ._submission import SubmissionResponse
from ._submission_status import SubmissionStatus, FaultEvent

__all__ = [
    "MPCClient",
    # Exceptions
    "MPCAPIError",
    "MPCRequestError",
    "MPCResponseError",
    "MPCNotFoundError",
    "MPCValidationError",
    # Response models
    "ActionCodeResponse",
    "DesignationData",
    "DesignationInfo",
    "FaultEvent",
    "MagnitudeData",
    "MPEC",
    "NearDuplicateMatch",
    "Observatory",
    "ObservationsResult",
    "OrbitalCoefficients",
    "OrbitalElements",
    "SubmissionResponse",
    "SubmissionStatus",
]
