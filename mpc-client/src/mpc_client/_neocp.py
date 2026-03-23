"""NEOCP Observations API mixin."""

from __future__ import annotations

from typing import List, Union

from pydantic import field_validator

from ._base import _MixinBase
from ._compat import require_pandas
from ._observations import ObservationsResult
from ._requests import _ObsFormatMixin, _validate
from .exceptions import MPCValidationError


# ---------- Request model ----------

class NEOCPRequest(_ObsFormatMixin):
    trksub: str

    @field_validator("trksub")
    @classmethod
    def _trksub_not_empty(cls, v):
        if not v:
            raise ValueError("trksub must be a non-empty string")
        return v

# ---------- Response model ----------

class NEOCPMixin(_MixinBase):

    def get_neocp_observations(
        self,
        trksub: str,
        *,
        output_format: Union[str, List[str]] = "XML",
        ades_version: str = "2022",
    ) -> ObservationsResult:
        """Retrieve observations for an object currently on the NEOCP.

        Parameters
        ----------
        trksub : str
            Tracklet identifier (temporary designation) on the NEOCP.
        output_format : str or list of str
            One or more of ``"XML"``, ``"ADES_DF"``, ``"OBS_DF"``, ``"OBS80"``.
        ades_version : str
            ``"2017"`` or ``"2022"`` (default).

        Returns
        -------
        ObservationsResult
            Response with attributes for each requested format.
        """
        req = _validate(NEOCPRequest, trksub=trksub, output_format=output_format, ades_version=ades_version)

        result = self._get(
            "/api/get-obs-neocp",
            json={
                "trksubs": [req.trksub],
                "output_format": req.output_format,
                "ades_version": req.ades_version,
            },
        )
        if isinstance(result, list) and result:
            return ObservationsResult(**result[0])
        return ObservationsResult(**(result if isinstance(result, dict) else {}))

    def get_neocp_observations_df(
        self, trksub: str, *, fmt: str = "ADES_DF", ades_version: str = "2022"
    ):
        """Retrieve NEOCP observations as a pandas DataFrame.

        Parameters
        ----------
        trksub : str
            Tracklet identifier on the NEOCP.
        fmt : str
            ``"ADES_DF"`` or ``"OBS_DF"``.
        ades_version : str
            ``"2017"`` or ``"2022"`` (default).

        Returns
        -------
        pandas.DataFrame
        """
        pd = require_pandas()
        if fmt not in ("ADES_DF", "OBS_DF"):
            raise MPCValidationError("fmt must be 'ADES_DF' or 'OBS_DF'")
        result = self.get_neocp_observations(
            trksub, output_format=fmt, ades_version=ades_version,
        )
        return pd.DataFrame(getattr(result, fmt))
