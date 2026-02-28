"""NEOCP Observations API mixin."""

from ._compat import require_pandas
from .exceptions import MPCValidationError

_VALID_FORMATS = {"XML", "ADES_DF", "OBS_DF", "OBS80"}


class NEOCPMixin:

    def get_neocp_observations(
        self, trksub, *, output_format="XML", ades_version="2022"
    ):
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
        dict
            Response dict keyed by the requested format(s).
        """
        if not trksub:
            raise MPCValidationError("trksub must be a non-empty string")
        if isinstance(output_format, str):
            output_format = [output_format]
        for fmt in output_format:
            if fmt not in _VALID_FORMATS:
                raise MPCValidationError(
                    f"Invalid output_format '{fmt}'. Must be one of {_VALID_FORMATS}"
                )

        result = self._get(
            "/api/get-obs-neocp",
            json={
                "trksubs": [trksub],
                "output_format": output_format,
                "ades_version": ades_version,
            },
        )
        if isinstance(result, list) and result:
            return result[0]
        return result

    def get_neocp_observations_df(
        self, trksub, *, fmt="ADES_DF", ades_version="2022"
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
        return pd.DataFrame(result[fmt])
