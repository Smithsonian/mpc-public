"""Main wis.py module for the calculation of coordinates of observatories.

By default these are heliocentric equatorial coordinates
(but the underlying spicepy functions can be used to get other coordinate systems if desired).
"""

# Standard library imports
# -----------------------------------------
import logging
import operator
from types import TracebackType

# Third-party imports
# -----------------------------------------
import numpy as np
import spiceypy as sp
from astropy.time import Time
from cachetools import LRUCache, cachedmethod
from cachetools.keys import hashkey

# Local imports
# -----------------------------------------
from wis.constants import PhysicalConstants
from wis.kernel_instances_satellites import satellite_kernels
from wis.kernelspecifier import KernelSpecifier
from wis.obscodes import MPCObsCodes

# Set up logger
logger = logging.getLogger(__name__)


class Wis(MPCObsCodes):
    """Class to manage the calculation of observatory locations.

    Users must explicitly specify which kernels to load. Only specified kernels
    are downloaded and loaded into memory, reducing startup time and resource usage.

    Examples:
        >>> from wis.kernels import DE430
        >>> with Wis(kernels=DE430) as w:
        ...     # Only DE430 kernel loaded

        >>> from wis.kernels import DE430, TESS
        >>> with Wis(kernels=[DE430, TESS]) as w:
        ...     # DE430 ground kernel and TESS (C57) satellite kernel loaded

        >>> from wis.kernels import DE430
        >>> from my_module import MyCustomKernel
        >>> with Wis(kernels=[DE430, MyCustomKernel]) as w:
        ...     # Mix built-in and custom kernels
    """

    # Any ability to specify `center`, `frame` or `abcorr` has been removed for the sake of simplicity
    #  - While the underlying spicepy functions can be used to get other coordinate systems if desired,
    #    this module is intended purely as a simplified convenience tool for the MPC
    #  => I have set these to default values that are appropriate for HELIOCENTRIC EQUATORIAL coordinates
    center, frame, abcorr = "SUN", "J2000", "NONE"
    ground_kernel_obscodes = ("GROUND430", "GROUND440")
    known_satellite_obscodes = tuple(
        satellite_kernels
    )  # from wis/wis/kernel_instances_satellites.py

    def __init__(self, kernels: KernelSpecifier | list[KernelSpecifier]) -> None:
        """Initialize a Wis instance with the specified kernels.

        Args:
            kernels: KernelSpecifier object(s) to load. Must explicitly specify which
                    kernels to load. Use wis.kernels exports for built-in kernels,
                    or pass custom KernelSpecifier objects.

        Raises:
            ValueError: If kernels is None or not provided.

        Examples:
            >>> from wis.kernels import DE430
            >>> with Wis(kernels=DE430) as w:
            ...     # Ground observatories only

            >>> from wis.kernels import DE430, TESS
            >>> with Wis(kernels=[DE430, TESS]) as w:
            ...     # Ground observatories and TESS satellite
        """
        # Call MPCObsCodes's __init__ to ensure it is properly set up
        super().__init__()

        # The cache for get_obs_helio_equ_AU is PER-INSTANCE: the cache key describes
        # only the call signature (obscode, times, flags), not which kernels are loaded,
        # so a shared cache would let a DE430 instance serve a DE440 instance's results.
        self.cache_get_obs_helio_equ_AU: LRUCache = LRUCache(maxsize=1024)

        # Populated by __enter__; the position methods refuse to run until then
        self.loaded_kernels: list[KernelSpecifier] = []
        self._entered = False

        # Validate kernels parameter
        if kernels is None:
            raise ValueError(
                "Must specify kernels to load. "
                "Import from wis.kernels (e.g., DE430, DE440, KEPLER, TESS) "
                "or provide custom KernelSpecifier objects."
            )

        # Normalize to a list
        if isinstance(kernels, KernelSpecifier):
            self.kernels_param = [kernels]
        elif isinstance(kernels, list):
            if not kernels:
                raise ValueError("kernels list cannot be empty")
            self.kernels_param = kernels
        else:
            raise ValueError(
                f"Invalid kernels type: {type(kernels)}. "
                "Expected KernelSpecifier or list of KernelSpecifier."
            )

    def __enter__(self) -> "Wis":
        """Load the specified kernels into memory.

        Returns:
            Wis: The instance for use in context manager.
        """
        # Load all specified kernels
        self.loaded_kernels = []
        loaded_obscodes = set()  # Track loaded obscodes to avoid duplicates

        for kernel in self.kernels_param:
            # Skip if already loaded (avoid duplicate loading)
            if kernel.obscodeMPC in loaded_obscodes:
                continue

            kernel.load()
            self.loaded_kernels.append(kernel)
            loaded_obscodes.add(kernel.obscodeMPC)

        # we always need a ground kernel for 1) the leapseconds kernel and 2) the sun's
        # position for heliocentric queries
        if not self._has_ground_kernel():
            sp.kclear()
            raise ValueError(
                "No ground kernel loaded. A ground kernel (DE430 or DE440) is always "
                "required — it supplies the leapsecond file and planetary ephemeris "
                "needed for all position calculations. Example:\n"
                "  from wis.kernels import DE430, TESS\n"
                "  Wis(kernels=[DE430, TESS])"
            )

        logger.info(
            f"Loaded {len(self.loaded_kernels)} kernel(s): "
            f"{[k.name for k in self.loaded_kernels]}"
        )

        self._entered = True
        return self  # so that Wis instance can be used as 'w' inside 'with'

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """Clear the loaded SPICE kernels and cache on exiting the context manager."""
        sp.kclear()  # <- Clear the spice kernels from memory
        self.cache_get_obs_helio_equ_AU.clear()  # <- Clear the cache
        self.loaded_kernels = []
        self._entered = False
        return False  # <- Do not suppress exceptions

    def _require_context(self) -> None:
        """Raise if the instance is not currently inside its `with` block.

        The kernels are only furnished by __enter__ (and are unloaded again by
        __exit__), so any position query outside that block would either fail
        deep inside SPICE or read stale kernel state.
        """
        if not self._entered:
            raise RuntimeError(
                "Wis must be used as a context manager, e.g.\n"
                "  from wis.kernels import DE430\n"
                "  with Wis(kernels=DE430) as w:\n"
                "      w.get_obs_helio_equ_AU('F51', times)"
            )

    def _has_ground_kernel(self) -> bool:
        """Check if a ground kernel (DE430 or DE440) is loaded."""
        for kernel in self.loaded_kernels:
            if kernel.obscodeMPC in self.ground_kernel_obscodes:
                return True
        return False

    def _has_satellite_kernel(self, obscode: str) -> bool:
        """Check if a specific satellite kernel is loaded."""
        for kernel in self.loaded_kernels:
            if (kernel.obscodeMPC == obscode) and (
                kernel.obscodeMPC not in self.ground_kernel_obscodes
            ):
                return True
        return False

    def _get_kernel_for_obscode(self, obscode: str) -> KernelSpecifier:
        """Get the loaded kernel for a specific obscode.

        Args:
            obscode: MPC observatory code

        Returns:
            KernelSpecifier: The kernel for this obscode

        Raises:
            RuntimeError: If no kernel for this obscode is loaded.
        """
        for kernel in self.loaded_kernels:
            if kernel.obscodeMPC == obscode:
                return kernel
        raise RuntimeError(f"No kernel loaded for obscode {obscode}")

    def compute_key(*args: object, **kwargs: object) -> tuple:
        """Generate a unique cache key for `get_obs_helio_equ_AU` (below).

        Made more complex by the need to deal with positional arguments and keyword arguments.

        N.B.: `test_speed` seems to show that the caching helps make it ~100x faster to get the same data
        """
        # Extract positional arguments
        _, name, times = args[0], args[1], args[2]
        # Key on the UTC JDs, because that is what `_convert_time` actually feeds to
        # SPICE. Keying on `times.jd` instead would make Time(X, scale="utc") and
        # Time(X, scale="tdb") collide despite being ~69s (i.e. ~2000km) apart.
        times_jd_tuple = tuple(np.atleast_1d(times.utc.jd))  # type: ignore

        # fallback_to_geo / return_velocity may be passed positionally (indices
        # 3/4) or by keyword; read positionals first so positional calls do not
        # collide on the kwargs defaults. (get_obs_bary_equ_AU passes
        # fallback_to_geo positionally.)
        fallback_to_geo = (
            args[3] if len(args) > 3 else kwargs.get("fallback_to_geo", False)
        )
        return_velocity = (
            args[4] if len(args) > 4 else kwargs.get("return_velocity", False)
        )

        # Create a unique hash key
        return hashkey(name, times_jd_tuple, fallback_to_geo, return_velocity)

    @cachedmethod(operator.attrgetter("cache_get_obs_helio_equ_AU"), key=compute_key)
    def get_obs_helio_equ_AU(
        self,
        obscodeMPC: str,
        times: Time,
        fallback_to_geo: bool = False,
        return_velocity: bool = False,
    ) -> tuple[np.ndarray, ...] | None:
        """Get the heliocentric equatorial coordinates of the observatory at the specified times.

        Args:
            obscodeMPC: MPC observatory code (e.g., '675' for Palomar, 'C57' for TESS)
            times: Astropy Time object with observation times
            fallback_to_geo: If True, treat unknown obscodes as geocenter (500)
            return_velocity: If True, also return the observatory velocities. For
                ground stations this is the full topocentric velocity (geocenter
                orbital velocity plus the Earth-rotation contribution of the
                observatory offset).

        Returns:
            If return_velocity is False: tuple of (positions [AU], light_travel_times [days]).
            If return_velocity is True: tuple of (positions [AU], velocities [AU/day],
            light_travel_times [days]).
            None if obscode unknown and fallback_to_geo is False.

        Raises:
            RuntimeError: If the instance is not being used as a context manager, or
                           if the required kernel for this obscode is not loaded.
                           Error message indicates which kernel to include.
        """
        self._require_context()

        # Check if required kernel is loaded BEFORE converting time (which needs SPICE)
        # This must be done first because _check_input_formats calls _convert_time
        # which requires leapsecond kernels to be loaded
        has_satellite_kernel = self._has_satellite_kernel(obscodeMPC)

        if obscodeMPC in self.geocentric_xyz_dict:  # <- Known ground station
            # Runtime validation: check if ground kernel is loaded
            if not self._has_ground_kernel():
                logger.error(
                    f"Cannot calculate position for ground observatory {obscodeMPC}: "
                    f"No ground kernel loaded. Please include DE430 or DE440 "
                    f"in your kernels list when instantiating Wis. "
                    f"Example: Wis(kernels=[DE430])"
                )
                return None
        elif not has_satellite_kernel:
            if obscodeMPC in self.known_satellite_obscodes:
                logger.error(
                    f"Cannot calculate position for satellite {obscodeMPC}: "
                    f"the {satellite_kernels[obscodeMPC].name} kernel is not loaded. "
                    f"Import the kernel object from wis.kernels and include it in "
                    f"your kernels list when instantiating Wis. Example:\n"
                    f"  from wis.kernels import DE430, TESS\n"
                    f"  Wis(kernels=[DE430, TESS])"
                )
                return None
            if not fallback_to_geo:
                # Unknown obscode and not falling back
                logger.error(
                    f"Unknown obscode {obscodeMPC} and fallback_to_geo is False. "
                    "Cannot calculate position. Please check your obscode or set "
                    "fallback_to_geo=True."
                )
                return None

        # Now safe to convert time (requires SPICE kernels)
        # NB: routing state is kept in LOCALS, not on self: this method is cached, so on
        # a cache hit the body never runs and any attribute set here would be stale.
        obscodeMPC, epochs_tuple = self._check_input_formats(obscodeMPC, times)

        # get the heliocentric equatorial coordinates for the obscode in question
        # Validation already done above, so just route to appropriate handler
        if obscodeMPC in self.geocentric_xyz_dict:  # <- Known ground station
            return self._get_ground_posns(obscodeMPC, epochs_tuple, return_velocity)

        elif self._has_satellite_kernel(obscodeMPC):
            return self._get_satellite_posns(obscodeMPC, epochs_tuple, return_velocity)

        elif fallback_to_geo:  # <- Treat unknown as geocenter
            return self._get_ground_posns("500", epochs_tuple, return_velocity)
        else:
            return None  # <- Unknown obscode and not falling back to geocenter

    def get_bary_wrt_helio(
        self, times: Time
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get the position of the barycenter [0] w.r.t. the heliocenter [10] at the specified times.

        Calls spkezr("0", ..., "10"): target=SSB(0), observer=Sun(10), so the
        returned position vector is r_ssb - r_sun (barycenter relative to heliocenter).
        To convert a heliocentric position to barycentric, subtract this offset:
            r_bary = r_helio - get_bary_wrt_helio()[0]

        Note: This method requires a ground kernel to be loaded (for Earth position).

        Returned Arrays:
        - posns: shape=(N_times,3) array of position vectors [AU]
        - vels: shape=(N_times,3) array of velocity vectors [AU/day]
        - ltts: shape=(N_times) array of light travel times [days]
        """
        # Runtime validation
        self._require_context()
        if not self._has_ground_kernel():
            raise RuntimeError(
                "get_bary_wrt_helio requires a ground kernel. "
                "Please include DE430 or DE440 in your kernels list."
            )

        states, ltts = sp.spkezr(
            "0", np.array(self._convert_time(times)), self.frame, self.abcorr, "10"
        )
        states = np.array(states)
        return (
            self._convert_posn(states[:, :3]),
            self._convert_vel(states[:, 3:]),
            self._convert_ltts(ltts),
        )

    def get_obs_bary_equ_AU(
        self,
        obscodeMPC: str,
        times: Time,
        fallback_to_geo: bool = False,
        return_velocity: bool = False,
    ) -> np.ndarray | tuple[np.ndarray, np.ndarray] | None:
        """Get the barycentric equatorial coordinates of an observatory.

        Just a wrapper that combines get_obs_helio_equ_AU
        (r_obs - r_sun, heliocentric) with get_bary_wrt_helio
        (r_ssb - r_sun, barycenter w.r.t. heliocenter)

        If return_velocity is True, returns a tuple of (positions [AU],
        velocities [AU/day]); otherwise returns the positions array only.
        """
        helio_result = self.get_obs_helio_equ_AU(
            obscodeMPC, times, fallback_to_geo, return_velocity=return_velocity
        )
        if helio_result is None:
            return None

        # get_bary_wrt_helio returns r_ssb - r_sun (barycenter w.r.t. heliocenter).
        # r_obs_bary = r_obs_helio - (r_ssb - r_sun) = r_obs - r_ssb
        # The same relation applies to the velocities.
        bary_wrt_helio_posns, bary_wrt_helio_vels, _ = self.get_bary_wrt_helio(times)

        if return_velocity:
            obs_helio, obs_helio_vel, _ = helio_result
            return (
                obs_helio - bary_wrt_helio_posns,
                obs_helio_vel - bary_wrt_helio_vels,
            )

        obs_helio, _ = helio_result
        return obs_helio - bary_wrt_helio_posns

    def _get_satellite_posns(
        self, obscodeMPC: str, epochs: tuple, return_velocity: bool = False
    ) -> tuple[np.ndarray, ...]:
        """Evaluate the position of a satellite at each epoch using the loaded kernels."""
        # Get the kernel for this satellite from loaded kernels
        kernel = self._get_kernel_for_obscode(obscodeMPC)
        self.obscodeJPL = kernel.obscodeJPL

        if return_velocity:
            # spkezr returns the full state (position + velocity) at each epoch
            states, ltts = sp.spkezr(
                self.obscodeJPL, np.array(epochs), self.frame, self.abcorr, self.center
            )  # [km, km/s], [s]
            states = np.array(states)
            return (
                self._convert_posn(states[:, :3]),  # -> AU
                self._convert_vel(states[:, 3:]),  # -> AU/day
                self._convert_ltts(ltts),  # -> days
            )

        self.obs_helio_equ, self.ltts = sp.spkpos(
            self.obscodeJPL, np.array(epochs), self.frame, self.abcorr, self.center
        )  # [km, s]
        self.obs_helio_equ_AU = self._convert_posn(
            self.obs_helio_equ
        )  # -> astronomical units
        self.ltts = self._convert_ltts(self.ltts)  # -> days
        return self.obs_helio_equ_AU, self.ltts

    def _get_ground_posns(
        self, obscodeMPC: str, epochs: tuple, return_velocity: bool = False
    ) -> tuple[np.ndarray, ...]:
        """Evaluate the HELIOCENTRIC EQUATORIAL position of a ground-based observatory at each epoch using the loaded kernels."""
        # Get geocentric observatory posn for supplied obs-code
        # NB: this is initially in fractions of an earth-radius, so we convert to km
        self.obs_geo = (
            self.geocentric_xyz_dict[obscodeMPC] * PhysicalConstants.Rearth_km
        )

        if return_velocity:
            # sxform returns the 6x6 STATE transformation matrix (position + velocity)
            # from ITRF93 to the required frame at each epoch. Unlike pxform it accounts
            # for the rotation rate of the Earth-fixed frame, so applying it to the
            # Earth-fixed state [obs_geo, 0] yields both the rotated position and the
            # topocentric velocity due to Earth's rotation.
            # https://spiceypy.readthedocs.io/en/main/documentation.html#spiceypy.spiceypy.sxform
            state_geo = np.concatenate([self.obs_geo, np.zeros(3)])  # [km, km/s]
            obs_geo_states = np.array(
                [sp.sxform("ITRF93", self.frame, epoch) @ state_geo for epoch in epochs]
            )
            obs_geo_equ_AU = self._convert_posn(obs_geo_states[:, :3])  # -> AU
            obs_geo_equ_vel = self._convert_vel(obs_geo_states[:, 3:])  # -> AU/day

            # Get the HELIOCENTRIC EQUATORIAL state of the GEOCENTER ('399' = Earth)
            geo_states, ltts = sp.spkezr(
                "399", np.array(epochs), self.frame, self.abcorr, self.center
            )
            geo_states = np.array(geo_states)
            geo_helio = self._convert_posn(geo_states[:, :3])  # -> AU
            geo_helio_vel = self._convert_vel(geo_states[:, 3:])  # -> AU/day

            # Combine geocenter and observatory-offset contributions
            return (
                obs_geo_equ_AU + geo_helio,
                obs_geo_equ_vel + geo_helio_vel,
                self._convert_ltts(ltts),  # -> days
            )

        # Use pxform to return the matrix that transforms position vectors from ...
        # ITRF93 (not IAU_EARTH) frame to J2000 frame at specified epoch.
        # Rotate the observatory posn vec to the required frame ( the J2000 default means this would be EQUATORIAL)
        # https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/pxform.html
        # https://spiceypy.readthedocs.io/en/v2.3.1/documentation.html#spiceypy.spiceypy.pxform
        self.obs_geo_equ = np.array(
            [
                np.dot(sp.pxform("ITRF93", self.frame, epoch), self.obs_geo)
                for epoch in epochs
            ]
        )
        self.obs_geo_equ_AU = self.obs_geo_equ / PhysicalConstants.au_km

        # Get the HELIOCENTRIC EQUATORIAL position of the GEOCENTER at each epoch
        # NB '399' is the NAIF code for the Earth
        # ( the default frame=J2000 & center=SUN means this would be HELIOCENTRIC EQUATORIAL)
        self.geo_helio, self.ltts = sp.spkpos(
            "399", np.array(epochs), self.frame, self.abcorr, self.center
        )
        self.geo_helio = self._convert_posn(self.geo_helio)  # -> astronomical units
        self.ltts = self._convert_ltts(self.ltts)  # -> days

        # Combine vectors to get the posn vec of the observatory in HELIOCENTRIC EQUATORIAL coords
        self.obs_helio_equ_AU = self.obs_geo_equ_AU + self.geo_helio

        return self.obs_helio_equ_AU, self.ltts

    def _convert_time(self, times: Time) -> tuple:
        """Convert the supplied astropy-times to the required format for spiceypy.

        Returning a TUPLE to help with caching of `_get_satellite_posns` & `_get_ground_posns`.
        """
        return tuple(
            sp.utc2et("JD" + str(jdutc)) for jdutc in np.atleast_1d(times.utc.jd)
        )

    def _convert_posn(self, posns: np.ndarray) -> np.ndarray:
        """Convert positions from km->AU."""
        return np.asarray(posns) / PhysicalConstants.au_km

    def _convert_ltts(self, ltts: np.ndarray) -> np.ndarray:
        """Conversion time from s->Day."""
        return np.asarray(ltts) / PhysicalConstants.day_s

    def _convert_vel(self, vels: np.ndarray) -> np.ndarray:
        """Convert velocities from km/s -> AU/day."""
        return np.asarray(vels) / (PhysicalConstants.au_km / PhysicalConstants.day_s)

    def _check_input_formats(
        self,
        obscodeMPC: str,  # MPC Observatory (Station) code
        times: Time,  # Astropy Time object [http://docs.astropy.org/en/stable/time/]
    ) -> tuple[str, tuple]:
        """Check that the inputs are formatted correctly."""
        # Check that the obscode is formatted correctly
        # (NB we do NOT check specific obscode values here because we do the routing in __init__  )
        if not isinstance(obscodeMPC, str):
            raise ValueError(f"Supplied obscode [{obscodeMPC}] is not a string")
        if len(obscodeMPC) not in [3, 4]:
            raise ValueError(
                f"Supplied obscode [{obscodeMPC}] is not of length 3 or 4 "
            )

        # Check supplied time is of the correct format
        # (NB we do NOT convert to spicypy format here because we do not have kernels loaded)
        if not isinstance(times, Time):
            raise ValueError(f"Supplied time [{times}] is not an astropy Time object")

        return obscodeMPC, self._convert_time(times)

    def _get_kernel_info(self) -> dict:
        """Return information about currently loaded kernels.

        Returns:
            dict: Information about loaded kernels including:
                - kernel_names: List of loaded kernel names
                - loaded_kernels: Metadata for each loaded kernel
        """
        return {
            "kernel_names": [k.name for k in self.loaded_kernels],
            "loaded_kernels": [
                {
                    "name": k.name,
                    "obscodeMPC": k.obscodeMPC,
                    "obscodeJPL": k.obscodeJPL,
                }
                for k in self.loaded_kernels
            ],
        }
