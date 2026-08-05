"""MPCObsCodes class that is used to query the MPC database for observatory codes."""

# Standard imports
import json
import logging
import os
import time

import numpy as np
import requests

from wis.constants import Directories

logger = logging.getLogger(__name__)


class MPCObsCodes:
    """Class to query the MPC database for observatory codes.

    This class is used to get the geocentric XYZ coordinates for each observatory code.
    """

    # Define the local file to store the obscode data
    # NB: only used as a backup in case of failure to access db
    local_obscode_file = os.path.join(Directories.data_dir, "obscode.json")

    def __init__(self) -> None:
        """Initialize by querying the API for MPC ObsCodes."""
        # Query API for MPC ObsCodes
        self.geocentric_xyz_dict, self.two_line_dict = self.get_geocentric_xyz_dict()

    def query_obscodes_api(
        self,
    ) -> tuple[dict[str, np.ndarray], dict[str, bool]]:
        """Query the MPC REST API for ObsCodes."""
        GeocentricXYZ, TwoLine = {}, {}

        # Query the MPC REST API for all observatory codes
        try:
            response = requests.get(
                "https://data.minorplanetcenter.net/api/obscodes", json={}, timeout=10
            )
            response.raise_for_status()
            obscodes_data = response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to access MPC ObsCodes API: {e}") from e

        # Process each observatory code
        for obscode, data in obscodes_data.items():
            longitude = data.get("longitude")
            rhocos = data.get("rhocosphi")
            rhosin = data.get("rhosinphi")
            two_line = data.get("uses_two_line_observations", False)

            # For non-critical codes, skip rows with None values
            if longitude is None or rhocos is None or rhosin is None:
                logger.warning(f"Skipping obscode '{obscode}': None values")
                continue

            # Parse the variables out of the API response
            try:
                longitude_rad = float(longitude) * np.pi / 180.0
                rhocos_float = float(rhocos)
                rhosin_float = float(rhosin)

                # If this is not a 2-line obscode, calculate the geoXYZ and add to the dictionary
                if not two_line:
                    GeocentricXYZ[obscode] = np.array(
                        [
                            rhocos_float * np.cos(longitude_rad),
                            rhocos_float * np.sin(longitude_rad),
                            rhosin_float,
                        ]
                    )
                else:
                    TwoLine[obscode] = True
            except (TypeError, ValueError) as e:
                # Skip rows with invalid data (e.g., non-numeric values)
                logger.warning(f"Skipping obscode '{obscode}': invalid data: {e}")
                continue
        return GeocentricXYZ, TwoLine

    def get_geocentric_xyz_dict(
        self, fallback: bool = True, save_local: bool = True
    ) -> tuple[dict[str, np.ndarray], dict[str, bool]]:
        """Query the API for MPC ObsCodes, falling back to flat-file if required."""
        # When fallback=False, never use local file - always try API first
        if not fallback:
            try:
                logger.info("Obscodes: fetching from MPC API (fallback=False)")
                GeocentricXYZ, TwoLine = self.query_obscodes_api()
                if GeocentricXYZ and save_local:
                    self._write_local_obscode_file(GeocentricXYZ, TwoLine)
                    logger.debug(
                        f"Obscodes: saved to local file "
                        f"({len(GeocentricXYZ)} geocentric, {len(TwoLine)} two-line)"
                    )
                return GeocentricXYZ, TwoLine
            except Exception as e:
                raise ConnectionError(
                    f"Failed to access API for MPC ObsCodes: {e}"
                ) from e

        # When fallback=True, try local file first if fresh
        if not self._local_obscode_file_is_stale():
            try:
                GeocentricXYZ, TwoLine = self._read_local_obscode_file()
                if GeocentricXYZ:  # Only return if we got valid data
                    logger.debug(
                        f"Obscodes: using cached local file "
                        f"({len(GeocentricXYZ)} geocentric, {len(TwoLine)} two-line)"
                    )
                    return GeocentricXYZ, TwoLine
            except Exception:
                # If local file read fails, continue to API
                logger.warning("Obscodes: failed loading cached local file")
                pass

        # If local file is stale or doesn't exist, try API
        try:
            logger.info("Obscodes: fetching from MPC API")
            GeocentricXYZ, TwoLine = self.query_obscodes_api()

            # If we got data from API, save it locally
            if GeocentricXYZ and save_local:
                self._write_local_obscode_file(GeocentricXYZ, TwoLine)
                logger.debug(
                    f"Obscodes: saved to local file "
                    f"({len(GeocentricXYZ)} geocentric, {len(TwoLine)} two-line)"
                )

            return GeocentricXYZ, TwoLine
        except Exception as e:
            # Try to use local file as fallback even if stale
            try:
                GeocentricXYZ, TwoLine = self._read_local_obscode_file()
                logger.warning(
                    f"Obscodes: API failed, using stale local file "
                    f"({len(GeocentricXYZ)} geocentric, {len(TwoLine)} two-line)"
                )
                return GeocentricXYZ, TwoLine
            except Exception:
                pass
            raise ConnectionError(f"Failed to access API for MPC ObsCodes: {e}") from e

    def _read_local_obscode_file(self) -> tuple[dict[str, np.ndarray], dict[str, bool]]:
        with open(self.local_obscode_file) as f:
            d = json.load(f)
            return {k: np.array(v) for k, v in d["GeocentricXYZ_as_lists"].items()}, d[
                "TwoLine"
            ]

    def _write_local_obscode_file(
        self, GeocentricXYZ: dict[str, np.ndarray], TwoLine: dict[str, bool]
    ) -> None:
        GeocentricXYZ_as_lists = {k: v.tolist() for k, v in GeocentricXYZ.items()}
        with open(self.local_obscode_file, "w") as f:
            json.dump(
                {"GeocentricXYZ_as_lists": GeocentricXYZ_as_lists, "TwoLine": TwoLine},
                f,
            )

    def _local_obscode_file_is_stale(
        self,
    ) -> bool:
        # Is the local obscode file older than one day?
        return (
            not os.path.exists(self.local_obscode_file)
            or (time.time() - os.path.getmtime(self.local_obscode_file)) > 1 * 24 * 3600
        )
