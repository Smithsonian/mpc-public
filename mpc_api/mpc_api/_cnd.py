"""Check Near-Duplicates (CND) API mixin."""

from .exceptions import MPCValidationError


class CNDMixin:

    def check_near_duplicates(
        self,
        obs,
        *,
        time_separation_s=60,
        angle_separation_arcsec=5,
        omit_separation=False,
    ):
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
        if isinstance(obs, str):
            obs = [obs]
        if not obs:
            raise MPCValidationError("obs must be a non-empty string or list")
        if not 0 <= time_separation_s <= 60:
            raise MPCValidationError("time_separation_s must be between 0 and 60")
        if not 0 <= angle_separation_arcsec <= 10:
            raise MPCValidationError("angle_separation_arcsec must be between 0 and 10")

        payload = {
            "obs": obs,
            "time_separation_s": time_separation_s,
            "angle_separation_arcsec": angle_separation_arcsec,
            "omit_separation": omit_separation,
        }
        result = self._get("/api/cnd", json=payload)
        return result.get("results", {})

    def count_near_duplicates(self, obs, **kwargs):
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
