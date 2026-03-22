"""Observatory Codes API mixin."""

from __future__ import annotations

from typing import Dict, Optional

from pydantic import ConfigDict

from ._base import _MixinBase
from ._compat import require_pandas
from ._requests import DictCompatModel


# ---------- Response model ----------

class Observatory(DictCompatModel):
    """Observatory information from the MPC observatory-codes list."""

    model_config = ConfigDict(extra="allow")

    obscode: Optional[str] = None
    """Three-character MPC observatory code (e.g. ``"500"``, ``"F51"``)."""

    name: str
    """Full observatory name."""

    longitude: Optional[float] = None
    """East longitude in degrees."""

    rhocosphi: Optional[float] = None
    """Parallax constant ρ cos φ′."""

    rhosinphi: Optional[float] = None
    """Parallax constant ρ sin φ′."""

    observations_type: Optional[str] = None
    """Observation type (e.g. ``"optical"``, ``"radar"``)."""


class ObscodesMixin(_MixinBase):

    def get_observatory(self, obscode: str) -> Observatory:
        """Get information about a specific observatory.

        Parameters
        ----------
        obscode : str
            Three-character observatory code (e.g. ``"500"``, ``"F51"``).

        Returns
        -------
        Observatory
            Observatory data including name, longitude, parallax constants.
        """
        data = self._get("/api/obscodes", json={"obscode": obscode})
        return Observatory(**data)

    def get_all_observatories(self) -> Dict[str, Observatory]:
        """Get information about all registered observatories.

        Returns
        -------
        dict
            Mapping of observatory code to :class:`~mpc_client.models.Observatory`.
        """
        raw = self._get("/api/obscodes", json={})
        return {k: Observatory(**v) for k, v in raw.items()}

    def get_all_observatories_df(self):
        """Get all observatories as a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            DataFrame indexed by observatory code.
        """
        pd = require_pandas()
        data = self.get_all_observatories()
        return pd.DataFrame.from_dict(
            {k: v.model_dump() for k, v in data.items()},
            orient="index",
        )

    def search_observatories(self, name_pattern: str):
        """Search observatories by name (case-insensitive substring match).

        Parameters
        ----------
        name_pattern : str
            Substring to search for in observatory names.

        Returns
        -------
        pandas.DataFrame
            Matching observatories.
        """
        df = self.get_all_observatories_df()
        mask = df["name"].str.lower().str.contains(name_pattern.lower(), na=False)
        return df[mask]
