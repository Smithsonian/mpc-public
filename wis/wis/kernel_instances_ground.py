"""This file constructs a KernelSpecifier object for the kernels necessary to perform the calculations for ground-based observatories."""

# -----------------------------------------
# Local imports
# -----------------------------------------
from wis.kernelspecifier import KernelSpecifier

"""
# Set-up KernelSpecifier(s) to cope with all ground-based obscodes

Notes from Davide Farnocchi [davide.farnocchia@jpl.nasa.gov] ...
For the Earth orientation kernels, see here: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/

- earth_720101_070426.bpc: reconstruction through 2007
- earth_latest_high_prec.bpc: latest high-precision reconstruction (I suggest getting it daily)
- earth_200101_990628_predict.bpc: future predicts

- MJP:2025-01-31: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/aareadme.txt suggests these 2 would
  be a good working combo:
   --- earth_*_combined.bpc
   --- earth_latest_high_prec.bpc

The readme file contains more details.
With these kernels you can the frame conversion between equatorial J2000 and body-fixed (ITRF93) using pxform:
https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/pxform.html

Note that the order in which you load kernels matters, later takes precedence for competing data:
https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/kernel.html#Kernel%20Priority
Predicts should go first and reconstructions later.

TODO: 2025
 - Create a way to flexibly get the latest earth kernels
 - Create a way to flexibly get the latest pck kernels
 - Create a way to order the files preferentially (predicts first, reconstructions later)
"""
# --------------------------------------------------------------------------


# check JPL -- do they say how often / publish message when?
common_files = [
    "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls",
    "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc",
    "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc",
]

common_wildcards = {
    "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/": "earth_*_combined.bpc"
}

# Have to redownload every time
# - redownload at some period ~1day
common_timecritical = [
    "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc"
]

# NB: These kernels cover all ground-based observatories, so we only need one set (per ephemeris model
# - The obscode-variables don't really fit very well here, so we'll just use 'GROUND***'

# Export individual kernel objects
DE430 = KernelSpecifier(
    obscodeMPC="GROUND430",
    obscodeJPL="GROUND430",
    name="DE430",
    files=[
        *common_files,
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp",
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc",
    ],
    wildcards=common_wildcards,
    timecritical=common_timecritical,
)

DE440 = KernelSpecifier(
    obscodeMPC="GROUND440",
    obscodeJPL="GROUND440",
    name="DE440",
    files=[
        *common_files,
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp",
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de440.tpc",
    ],
    wildcards=common_wildcards,
    timecritical=common_timecritical,
)

# Keep GROUND dict for backward compatibility in internal code
GROUND = {
    "DE430": DE430,
    "DE440": DE440,
}

__all__ = ["DE430", "DE440", "GROUND"]
