"""Observations API mixin."""

from __future__ import annotations

from typing import Any, Dict, List, Union

from pydantic import field_validator

from ._base import _MixinBase
from ._compat import require_pandas
from ._requests import _ObsFormatMixin, _validate
from .exceptions import MPCValidationError


# ---------- Request model ----------

class ObservationsRequest(_ObsFormatMixin):
    desig: str

    @field_validator("desig")
    @classmethod
    def _desig_not_empty(cls, v):
        if not v:
            raise ValueError("desig must be a non-empty string")
        return v


class ObservationsMixin(_MixinBase):

    def get_observations(
        self,
        desig: str,
        *,
        output_format: Union[str, List[str]] = "XML",
        ades_version: str = "2022",
    ) -> Dict[str, Any]:
        """Retrieve observations for a solar-system object.

        Parameters
        ----------
        desig : str
            Object designation (name, number, or provisional designation).
        output_format : str or list of str
            One or more of ``"XML"``, ``"ADES_DF"``, ``"OBS_DF"``, ``"OBS80"``.
        ades_version : str
            ADES format version: ``"2017"`` or ``"2022"`` (default).

        Returns
        -------
        dict
            Response dict keyed by the requested format(s).
        """
        req = _validate(ObservationsRequest, desig=desig, output_format=output_format, ades_version=ades_version)

        result = self._get(
            "/api/get-obs",
            json={
                "desigs": [req.desig],
                "output_format": req.output_format,
                "ades_version": req.ades_version,
            },
        )
        # API returns a list; return the first element for single-desig queries
        if isinstance(result, list) and result:
            return result[0]
        return result

    def get_observations_df(self, desig: str, *, fmt: str = "ADES_DF", ades_version: str = "2022"):
        """Retrieve observations as a pandas DataFrame.

        Parameters
        ----------
        desig : str
            Object designation.
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
        result = self.get_observations(
            desig, output_format=fmt, ades_version=ades_version,
        )
        return pd.DataFrame(result[fmt])
