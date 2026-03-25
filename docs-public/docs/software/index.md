# MPC Software

Software packages developed and maintained by the Minor Planet Center.

---

## digest2

NEO orbit classification from short-arc astrometric tracklets.

digest2 is a fast short-arc orbit classifier for minor planets, primarily used to identify Near-Earth Object (NEO) candidates from astrometric tracklets. It has been in operational use at the Minor Planet Center for over 15 years and is a key component of the NEO discovery workflow.

Available as both a C command-line tool and a pip-installable Python package (`pip install digest2`).

<div class="contents-grid"></div>

- [digest2 on GitHub](https://github.com/Smithsonian/mpc-public/tree/main/digest2)

---

## mpc_orb

Standardized JSON format for the exchange of best-fit orbit data for solar-system bodies.

mpc_orb defines a JSON-based format for exchanging orbit data for minor planets, comets, irregular satellites, and interstellar interlopers. The MPC currently populates mpc_orb.json files using data from the orbfit package, but the format is intended for generic exchange of orbit data from any source.

Available as a pip-installable Python package (`pip install mpc_orb`).

<div class="contents-grid"></div>

- [mpc_orb on GitHub](https://github.com/Smithsonian/mpc-public/tree/main/mpc_orb)

---

## ADES (Astrometry Data Exchange Standard)

The standard format for submitting and exchanging astrometric observations of solar-system objects.

ADES defines both XML and PSV (pipe-separated value) formats for astrometric data exchange. It is jointly maintained by the MPC and the JPL Center for Near Earth Object Studies (CNEOS).

<div class="contents-grid"></div>

- [ADES on GitHub](https://github.com/IAU-ADES/ADES-Master/tree/master)
