# Valid ADES Field Values

The tables below list all values accepted by the MPC for key fields in ADES (Astrometric Data Exchange Standard) submissions. Use of an unlisted value in any of these fields will cause a batch to be rejected.

Deprecated values are shown in *italics*. These are accepted for historical data but should not be used in new submissions unless specifically noted.


## mode (Instrumentation Type)

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


## astCat / photCat (Star Catalogs)

| Cat | Description |
|-----|-------------|
| Gaia3 | Gaia DR 3 |
| Gaia3E | Gaia EDR 3 |
| Gaia2 | Gaia DR 2 |
| Gaia1 | Gaia DR 1 |
| Gaia_2016 | Gaia epoch 2016 |
| Gaia_Int | Gaia_Int |
| PS1_DR1 | PanSTARRS-1 DR 1 |
| PS1_DR2 | PanSTARRS-1 DR 2 |
| ATLAS2 | ATLAS-REFCAT 2 |
| UCAC5 | UCAC 5 |
| UCAC4 | UCAC 4 |
| URAT1 | URAT 1 |
| 2MASS | 2MASS |
| NOMAD | NOMAD |
| PPMXL | PPM-XL |
| UBSC | USNO Bright-star Catalog |
| *UCAC3* | *UCAC 3* |
| *UCAC2* | *UCAC 2* |
| *UCAC1* | *UCAC 1* |
| *USNOB1* | *USNO B1.0* |
| *USNOA2* | *USNO A2.0* |
| *USNOSA2* | *USNO SA2.0* |
| *USNOA1* | *USNO A1.0* |
| *USNOSA1* | *USNO SA1.0* |
| *Tyc2* | *Tycho 2* |
| *Tyc1* | *Tycho 1* |
| *Hip2* | *Hipparcos 2* |
| *Hip1* | *Hipparcos 1* |
| *ACT* | *ACT* |
| *GSCACT* | *GSC-ACT* |
| *GSC2.3* | *GSC 2.3* |
| *GSC2.2* | *GSC 2.2* |
| *GSC1.2* | *GSC 1.2* |
| *GSC1.1* | *GSC 1.1* |
| *GSC1.0* | *GSC 1.0* |
| *GSC* | *GSC (unspecified version)* |
| *SDSS8* | *SDSS DR8* |
| *SDSS7* | *SDSS DR7* |
| *CMC15* | *CMC 15* |
| *CMC14* | *CMC 14* |
| *SSTRC4* | *SST-RC4* |
| *SSTRC1* | *SST-RC1* |
| *MPOSC3* | *MPOSC 3* |
| *PPM* | *PPM* |
| *AC* | *Astrographic Catalogue* |
| *SAO1984* | *SAO 1984* |
| *SAO* | *SAO* |
| *AGK3* | *AGK 3* |
| *FK4* | *FK4* |
| *ACRS* | *ACRS* |
| *LickGas* | *Lick Gaspra Catalogue* |
| *Ida93* | *Ida93 Catalogue* |
| *Perth70* | *Perth 70* |
| *COSMOS* | *COSMOS/UKST Southern Sky Catalogue* |
| *Yale* | *Yale* |
| *ZZCAT* | *USNO Zodiacal Zone Catalog* |
| *IHW* | *International Halley Watch* |
| *GZ* | *Giacobini-Zinner Catalogue* |
| *UNK* | *UNKNOWN* |

To request the addition of a new catalog, submit a [Helpdesk ticket](https://mpc-service.atlassian.net/servicedesk/customer/portals).


## band (Photometric Passbands)

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


## notes (Observing Notes)

Up to six notes may be included on a single observation.

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
| L | Corrected for differential color refraction |
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
| Z | Astrometry from a survey reported by a non-survey measurer/pipeline |


## photMod (Photometric Model)

| photMod | Description |
|---------|-------------|
| HG | HG model |
| H | HG model, assumed G |
| HG1G2 | HG1G2 model |
| HG12 | HG1,2 model |
| NEATM | NEA Thermal Model |
| FRM | Fast Rotator Model |


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
