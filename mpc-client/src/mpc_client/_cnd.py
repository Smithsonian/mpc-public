"""Check Near-Duplicates (CND) API mixin."""

from __future__ import annotations

from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field, field_validator

from ._base import _MixinBase
from ._requests import _validate


# ---------- Request model ----------

class CNDRequest(BaseModel):
    obs: List[str]
    time_separation_s: float = Field(default=60, ge=0, le=60)
    angle_separation_arcsec: float = Field(default=5, ge=0, le=10)
    omit_separation: bool = False

    @field_validator("obs", mode="before")
    @classmethod
    def _coerce_and_check_obs(cls, v):
        if isinstance(v, str):
            v = [v]
        if not v:
            raise ValueError("obs must be a non-empty string or list")
        return v


class CNDMixin(_MixinBase):

    def check_near_duplicates(
        self,
        obs: Union[str, List[str]],
        *,
        time_separation_s: float = 60,
        angle_separation_arcsec: float = 5,
        omit_separation: bool = False,
    ) -> Dict[str, Any]:
        """Check whether observations have near-duplicates in the MPC database.

        Parameters
        ----------
        obs : str or list of str
            Observation(s) in MPC 80-column (or 160-column) format.
        time_separation_s : float
            Temporal threshold in seconds (0–60). Default 60.
        angle_separation_arcsec : float
            Spatial threshold in arcseconds (0–10). Default 5.
        omit_separation : bool
            If True, omit separation values from results.

        Returns
        -------
        dict
            Mapping of each input observation to its list of near-duplicate matches.
        """
        req = _validate(
            CNDRequest,
            obs=obs,
            time_separation_s=time_separation_s,
            angle_separation_arcsec=angle_separation_arcsec,
            omit_separation=omit_separation,
        )

        payload = {
            "obs": req.obs,
            "time_separation_s": req.time_separation_s,
            "angle_separation_arcsec": req.angle_separation_arcsec,
            "omit_separation": req.omit_separation,
        }
        result = self._get("/api/cnd", json=payload)
        return result.get("results", {})

    def count_near_duplicates(self, obs: Union[str, List[str]], **kwargs: Any) -> Dict[str, int]:
        """Count near-duplicates for each input observation.

        Accepts the same keyword arguments as :meth:`check_near_duplicates`.

        Returns
        -------
        dict
            Mapping of each input observation to the number of matches found.
        """
        results = self.check_near_duplicates(obs, **kwargs)
        return {
            k: len(v) if isinstance(v, list) else 0
            for k, v in results.items()
        }
