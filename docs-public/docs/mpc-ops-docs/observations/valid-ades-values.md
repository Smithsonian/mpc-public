# Valid ADES Field Values

The tables below list all values accepted by the MPC for key fields in ADES (Astrometric Data Exchange Standard) submissions. Use of an unlisted value in any of these fields will cause a batch to be rejected.

Deprecated values are shown in *italics*. These are accepted for historical data but should not be used in new submissions unless specifically noted.


## mode (Instrumentation Type)

[//]: # (TODO: Is there a db table for this list? If so, produce this markdown and the JSON from that table.)

| mode | Description |
|------|-------------|
| CCD | Charge-Coupled Device |
| CMO | Complementary Metal Oxide Semiconductor (CMOS) |
| VID | Video frames |
| TDI | Time-delay Integration CCD |
| OCC | Occultation |
| *PHO* | *Photographic* |
| *ENC* | *Encoder* |
| *PMT* | *Photo-Multiplier Tube* |
| *MIC* | *Micrometer* |
| *MER* | *Meridian/Transit Circle* |
| *UNK* | *Unknown* |

A JSON representation of this table is available [here](static/mode-instrumentation-types.json).

## astCat / photCat (Star Catalogs)

--8<-- "docs/mpc-ops-docs/observations/static/catalog-codes.md"

To request the addition of a new catalog, submit a [Helpdesk ticket](https://mpc-service.atlassian.net/servicedesk/customer/portals).
A JSON representation of this table is available [here](./static/catalog-codes.json).

## band (Photometric Passbands)

--8<-- "docs/mpc-ops-docs/observations/static/mag-bands.md"

[//]: # (TODO: Generate this table and JSON from `vmsops:mag_bands`; the `deprecated` field needs to be added first.)

| band | Description |
|------|-------------|
| Lu | LSST u band |
| Lg | LSST g band |
| Lr | LSST r band |
| Li | LSST i band |
| Lz | LSST z band |
| Ly | LSST y band |
| VR | DECam VR band |
| Vj | Johnson-Cousins V |
| Rc | Johnson-Cousins R |
| Ic | Johnson-Cousins I |
| Bj | Johnson-Cousins B |
| Uj | Johnson-Cousins U |
| Sg | Sloan g band |
| Sr | Sloan r band |
| Si | Sloan i band |
| Sz | Sloan z band |
| Pg | Pan-STARRS g band |
| Pr | Pan-STARRS r band |
| Pi | Pan-STARRS i band |
| Pz | Pan-STARRS z band |
| Pw | Pan-STARRS w band |
| Py | Pan-STARRS y band |
| Ao | ATLAS o band |
| Ac | ATLAS c band |
| G | Gaia G band |
| Gb | Gaia G_BP band |
| Gr | Gaia G_RP band |
| W | Wide |
| *U* | *U band* |
| *B* | *Photographic* |
| *V* | *Visual* |
| *R* | *Red* |
| *I* | *Near IR* |
| *g* | *g band* |
| *r* | *r band* |
| *i* | *i band* |
| *z* | *z band* |
| *w* | *w band* |
| *y* | *y band* |
| *o* | *ATLAS o band* |
| *c* | *ATLAS c band* |
| *J* | *1.275 micron band* |
| *H* | *1.662 micron band* |
| *K* | *2.159 micron band* |
| *Y* | *1.035 micron band* |
| *C* | *Clear* — MUST NOT be used on new submissions |
| *L* | *Unknown* — MUST NOT be used on new submissions |
| *u* | *Unknown* — MUST NOT be used on new submissions |

A JSON representation of this table is available [here](./static/mag-bands.json). See also the [Magnitude Band API](../apis/mag-band.md) for programmatic, real-time access to this data.

## notes (Observing Notes)

Up to six notes may be included on a single observation.

[//]: # (TODO: Generate this table and JSON from `vmsops:publishable_notes`)

| note | Description |
|------|-------------|
| *A* | *Earlier approximate position inferior* |
| a | Sense of motion ambiguous |
| B | Bright sky/black or dark plate |
| b | Bad seeing |
| c | Crowded star field |
| D | Declination uncertain |
| d | Diffuse image |
| E | At or near edge of plate/frame |
| e | Extrapolation to zero aperture technique used |
| F | Faint image |
| f | Involved with emulsion, plate or CCD flaw |
| G | Poor guiding |
| g | No guiding |
| H | Hand measurement of CCD image |
| h | Observed through cloud/haze |
| I | Involved with star |
| *i* | *Inkdot measured* |
| K | Stacked image |
| k | Stare-mode observation by scanning system |
| L | Color corrected observations |
| M | Measurement difficult |
| m | Image tracked on object motion |
| N | Near edge of plate, measurement uncertain |
| n | Normal place |
| O | Image out of focus |
| *o* | *Plate measured in one direction only* |
| P | Position uncertain |
| p | Poor image |
| R | Right ascension uncertain |
| r | Poor distribution of reference stars |
| S | Poor sky |
| s | Streaked image |
| T | Time uncertain |
| t | Trailed image |
| U | Uncertain image |
| u | Unconfirmed image |
| V | Very faint image |
| W | Weak image |
| w | Weak solution |
| Z | Astrometry from large surveys without program codes reported by a non-survey measurerer/pipeline |

A JSON representation of this table is available [here](./static/observing-notes.json).

## photMod (Photometric Model)

| photMod | Description |
|---------|-------------|
| HG | HG model |
| H | HG model, assumed G |
| HG1G2 | HG1G2 model |
| HG12 | HG1,2 model |
| NEATM | NEA Thermal Model |
| FRM | Fast Rotator Model |

A JSON representation of this table is available [here](./static/photometric-models.json).

## subFmt (Submission Format)

| subFmt | Description |
|--------|-------------|
| PRE | Pre-MPC |
| M47 | MPC1947 |
| M92 | MPC1992 |
| A17 | ADES version 2017 |
| A22 | ADES version 2022 |


## sys (Coordinate Frame)

| sys | Description |
|-----|-------------|
| WGS84 | Geodetic reference ellipsoid |
| ITRF | Cylindrical |
| IAU | IAU planetary cartographic model for bodies other than Earth |
| ICRF_AU | Cartesian (AU) |
| ICRF_KM | Cartesian (km) |
