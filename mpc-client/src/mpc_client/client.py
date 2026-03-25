"""MPCClient — unified client for all Minor Planet Center APIs."""

from __future__ import annotations

from typing import Optional

from ._action_codes import ActionCodesMixin
from ._base import BaseAPI
from ._cnd import CNDMixin
from ._identifier import IdentifierMixin
from ._mpecs import MPECsMixin
from ._neocp import NEOCPMixin
from ._obscodes import ObscodesMixin
from ._observations import ObservationsMixin
from ._orbits import OrbitsMixin
from ._submission import SubmissionMixin
from ._submission_status import SubmissionStatusMixin


class MPCClient(
    IdentifierMixin,
    ObscodesMixin,
    SubmissionStatusMixin,
    CNDMixin,
    MPECsMixin,
    ObservationsMixin,
    NEOCPMixin,
    OrbitsMixin,
    ActionCodesMixin,
    SubmissionMixin,
    BaseAPI,
):
    """Python client for the Minor Planet Center REST APIs.

    Parameters
    ----------
    api_key : str or None
        Reserved for future use.  Defaults to ``None``.
    timeout : int
        Request timeout in seconds.  Defaults to 60.

    Examples
    --------
    >>> from mpc_client import MPCClient
    >>> mpc = MPCClient()
    >>> mpc.identify("Ceres")  # doctest: +SKIP
    {'Ceres': {'permid': '1', ...}}
    """

    def __init__(self, *, api_key: Optional[str] = None, timeout: int = 60) -> None:
        super().__init__(api_key=api_key, timeout=timeout)

    def __repr__(self) -> str:
        return "MPCClient()"
