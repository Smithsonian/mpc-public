"""Observations API mixin."""

from ._compat import require_pandas
from .exceptions import MPCValidationError

_VALID_FORMATS = {"XML", "ADES_DF", "OBS_DF", "OBS80"}


class ObservationsMixin:

    def get_observations(self, desig, *, output_format="XML", ades_version="2022"):
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
        if not desig:
            raise MPCValidationError("desig must be a non-empty string")
        if isinstance(output_format, str):
            output_format = [output_format]
        for fmt in output_format:
            if fmt not in _VALID_FORMATS:
                raise MPCValidationError(
                    f"Invalid output_format '{fmt}'. Must be one of {_VALID_FORMATS}"
                )

        result = self._get(
            "/api/get-obs",
            json={
                "desigs": [desig],
                "output_format": output_format,
                "ades_version": ades_version,
            },
        )
        # API returns a list; return the first element for single-desig queries
        if isinstance(result, list) and result:
            return result[0]
        return result

    def get_observations_df(self, desig, *, fmt="ADES_DF", ades_version="2022"):
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
