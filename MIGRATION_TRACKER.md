# Documentation Migration Tracker

Last updated: 2026-03-01

**Discovery methodology (2026-03-01):** This tracker was populated by (a) searching all pages under `docs/mpc-ops-docs/` for outbound links to `https://minorplanetcenter.net/`, then (b) fetching each of those legacy pages and extracting any additional links to other `https://minorplanetcenter.net/` pages not already tracked. This two-level crawl is not exhaustive — newly migrated pages or previously unvisited legacy pages may introduce further links — so this process should be repeated periodically.

## Summary

| Status | Count |
|---|---|
| Migrated | 13 |
| WIP | 1 |
| Redirect banner needed | 14 |
| Redirect banner added | 0 |
| Deprecation banner needed | 2 |
| Legacy page removed | 0 |
| To migrate | 26 |
| To deprecate | 2 |
| TBD | 34 |
| Skip (service/MPEC/data) | 47 |

## By Category

| Category | Migrated | WIP | To Do | TBD | Deprecate | Skip |
|---|---|---|---|---|---|---|
| Designations | 8 | 0 | 0 | 0 | 0 | 6 |
| Identifications | 3 | 1 | 0 | 0 | 0 | 2 |
| Astrometry | 1 | 0 | 1 | 3 | 1 | 6 |
| Observations & Formats | 0 | 0 | 9 | 3 | 0 | 3 |
| Orbits | 0 | 0 | 10 | 2 | 0 | 1 |
| Observatory & Program Codes | 0 | 0 | 3 | 0 | 0 | 5 |
| Data & Services | 1 | 0 | 3 | 20 | 0 | 16 |
| Miscellaneous | 0 | 0 | 0 | 6 | 1 | 8 |
| **Total** | **13** | **1** | **26** | **34** | **2** | **47** |

---

## Detailed Tables

### Designations

| Legacy Path | Migration | New Location | Legacy Banner | Notes |
|---|---|---|---|---|
| `/iau/info/OldDesDoc.html` | migrated | `designations/provisional-designations.md` | redirect-needed | Consolidated with provisional-designation-definition |
| `/mpcops/documentation/provisional-designation-definition/` | migrated | `designations/provisional-designations.md` | redirect-needed | Consolidated with OldDesDoc |
| `/iau/info/TempDesDoc.html` | migrated | `designations/temporary-designations.md` | redirect-needed | |
| `/iau/info/HowNamed.html` | migrated | `designations/how-asteroids-are-named.md` | redirect-needed | |
| `/iau/lists/CometResolution.html` | migrated | `designations/cometary-designation-system.md` | redirect-needed | |
| `/iau/info/PackedDes.html` | migrated | `designations/packed-designations.md` | redirect-needed | Includes extended packed format from mpcops |
| `/iau/info/PackedDates.html` | migrated | `designations/packed-dates.md` | redirect-needed | |
| `/iau/lists/DualStatus.html` | migrated | `designations/dual-status-objects.md` | redirect-needed | |
| `/iau/lists/MPNames.html` | skip | - | none | Auto-generated name list |
| `/iau/lists/NumberedMPs.html` | skip | - | none | Auto-generated discovery circumstances |
| `/iau/lists/PeriodicCodes.html` | skip | - | none | Periodic comet codes (numerical); auto-generated |
| `/iau/lists/PeriodicCodes1.html` | skip | - | none | Periodic comet codes (alphabetical); auto-generated |
| `/iau/lists/LastYear.html` | skip | - | none | Auto-generated recent comet designations |
| `/submit_name` | skip | - | none | Asteroid naming submission form |

### Identifications

| Legacy Path | Migration     | New Location | Legacy Banner | Notes |
|---|---------------|---|---|---|
| `/mpcops/documentation/identifications/` | migrated      | `identifications/index.md` | redirect-needed | Full overview content |
| `/mpcops/documentation/identifications/submission-format/` | migrated      | `identifications/submission-format.md` | redirect-needed | |
| `/mpcops/documentation/identifications/additional/` | migrated      | `identifications/acceptance-criteria.md` | redirect-needed | |
| `/mpcops/submissions/identifications/` | skip          | - | none | Submission form |
| `/mpcops/documentation/identifications/stats/` | skip          | - | none | Auto-generated yearly stats pages |
| `/static/submissions/media/identifications_api_example.py` | WIP: [PR38](https://github.com/Smithsonian/mpc-public/pull/38) | - | redirect-needed | API example script |

### Astrometry

| Legacy Path | Migration  | New Location | Legacy Banner | Notes                                                                                                         |
|---|------------|---|---|---------------------------------------------------------------------------------------------------------------|
| `/iau/info/Astrometry.html` | migrated   | `astrometry/` (5 pages) | redirect-needed | Split into getting-started, observatory-codes, reporting-observations, discoveries-and-credit, mpc-processing |
| `/iau/info/CatalogueCodes.html` | to-migrate | - | none | Catalogue codes reference; priority: medium                                                                   |
| `/iau/info/VideoNormalPlaces.html` | TBD | - | none | Service to extract an "average" from video frames                                                             |
| `/iau/info/AGuidetoVideoAstrometry.pdf` | TBD        | - | none | External PDF guide from 2015: Tangra software site last updated 2018                                          |
| `/iau/info/VideoAstrometry.pdf` | TBD        | - | none | External PDF guide from 2009: Tangra software site last updated 2018                                          |
| `/iau/info/Coverage.html` | skip       | - | none | Sky coverage submission service                                                                               |
| `/iau/SkyCoverage.html` | skip       | - | none | Sky coverage plots service                                                                                    |
| `/cgi-bin/checkmp.cgi` | skip       | - | none | MPChecker service                                                                                             |
| `/iau/MPEph/MPEph.html` | skip       | - | none | Ephemeris service                                                                                             |
| `/iau/MPEph/FollowUp.html` | deprecate  | - | deprecation-needed | Follow-up sites;                                                                                              |
| `/iau/MPEph/NewObjEphems.html` | skip       | - | none | New object ephemeris service                                                                                  |
| `/cgi-bin/neaobs.cgi` | skip       | - | none | NEA observation planning tool                                                                                 |

### Observations & Formats

| Legacy Path | Migration  | New Location | Legacy Banner | Notes                                                          |
|---|------------|---|---|----------------------------------------------------------------|
| `/iau/info/ADES.html` | to-migrate | - | none | ADES format description; priority: high                        |
| `/iau/info/ObsFormat.html` | to-migrate | - | none | MPC1992 observation format; priority: high                     |
| `/iau/info/ObsDetails.html` | to-migrate | - | none | Observation details header format; priority: medium            |
| `/iau/info/RovingObs.html` | to-migrate | - | none | Roving observers format; priority: medium                      |
| `/iau/info/TelescopeDetails.html` | to-migrate | - | none | Telescope details header format; priority: medium              |
| `/iau/info/References.html` | to-migrate | - | none | Reference codes for observations; priority: medium             |
| `/iau/info/commandlinesubmissions.html` | to-migrate | - | none | cURL/command-line submission guide; priority: medium           |
| `/mpcops/documentation/negative-observations/` | to-migrate | - | none | Negative observation protocol; priority: low                   |
| `/mpcops/documentation/ades/` | TBD        | - | none | ADES docs : Has this been done already?                        |
| `/mpcops/documentation/valid-ades-values` | TBD        | - | none | ADES valid values reference (dynamic): can this be migrated?   |
| `/submit_psv` | skip       | - | none | PSV submission form                                            |
| `/submit_xml` | skip       | - | none | XML submission form                                            |
| `/iau/info/ADESFieldValues.html` | TBD | - | none | ADES field value reference; linked from ADES.html |
| `/iau/info/ObsNote.html` | to-migrate | - | none | Observation alphabetic notes; priority: medium |
| `/cgi-bin/feedback_submit_obs.cgi` | skip       | - | none | Already marked as deprecated (Old observation submission form) |

### Orbits

| Legacy Path | Migration | New Location | Legacy Banner | Notes |
|---|---|---|---|---|
| `/iau/info/MPOrbitFormat.html` | to-migrate | - | none | Minor planet orbit format; priority: high |
| `/iau/info/CometOrbitFormat.html` | to-migrate | - | none | Comet orbit format; priority: high |
| `/iau/info/SatOrbitFormat.html` | to-migrate | - | none | Natural satellite orbit format; priority: medium |
| `/iau/info/OrbFormat.html` | to-migrate | - | none | General orbit format overview; priority: medium |
| `/iau/info/OrbNote.html` | to-migrate | - | none | Orbit alphabetic notes; priority: medium |
| `/iau/info/Perturbers.html` | to-migrate | - | none | Perturbing bodies reference; priority: low |
| `/iau/info/UValue.html` | to-migrate | - | none | Uncertainty parameter U; priority: medium |
| `/mpcops/documentation/orbit-types/` | to-migrate | - | none | Orbit type definitions; priority: medium |
| `/mpcops/documentation/object-types/` | to-migrate | - | none | Object type definitions; priority: medium |
| `/mpcops/documentation/ele220/` | to-migrate | - | none | ele220 format |
| `/iau/MPCORB.html` | TBD | - | none | MPCORB orbit file documentation/download page |
| `/mpcops/documentation/mpc-orbits/` | TBD | - | none | MPC orbits documentation on mpcops |
| `/mpcops/documentation/mpc-orb-json/` | skip | - | none | Covered by mpc_orb package docs |

### Observatory & Program Codes

| Legacy Path | Migration | New Location | Legacy Banner | Notes |
|---|---|---|---|---|
| `/iau/info/ObservatoryCodes.html` | to-migrate | - | none | Observatory codes documentation; priority: high |
| `/mpcops/documentation/program-codes/` | to-migrate | - | none | Program codes documentation; priority: high |
| `/mpcops/documentation/program-codes-policy/` | to-migrate | - | none | Program codes policy; priority: medium |
| `/new_obscode_request` | skip | - | none | Observatory code request form |
| `/iau/lists/ObsCodes.html` | skip | - | none | Observatory codes plaintext list |
| `/iau/lists/ObsCodesF.html` | skip | - | none | Observatory codes formatted list |
| `/iau/lists/ProgramCodes.txt` | skip | - | none | Program codes plaintext file |
| `/submit_action_code` | skip | - | none | Action code submission form |

### Data & Services

| Legacy Path | Migration | New Location | Legacy Banner | Notes |
|---|---|---|---|---|
| `/iau/info/TechInfo.html` | to-migrate | - | none | General technical information; priority: medium |
| `/iau/NEO/NEOCPNotes.html` | to-migrate | - | none | NEOCP documentation/notes; priority: medium |
| `/mpcops/documentation/tycho-tracker/` | to-migrate | - | none | Tycho Tracker guide; priority: medium |
| `/iau/NEO/ToConfirm.html` | skip | - | none | NEOCP main page (dynamic service) |
| `/iau/NEO/toconfirm_tabular.html` | skip | - | none | NEOCP tabular view (dynamic) |
| `/iau/NEO_dev/toconfirm_tabular.html` | skip | - | none | NEOCP dev endpoint |
| `/iau/NEO_dev/neocp.txt` | skip | - | none | NEOCP plaintext data feed |
| `/wamo/` | skip | - | none | WAMO service (all subpages) |
| `/whatsup` | skip | - | none | What's Up service |
| `/iau/delays/neocp_delay.html` | skip | - | none | Processing status page (dynamic) |
| `/iau/recovery/recovery.html` | skip | - | none | Recovery page (dynamic) |
| `/iau/ITF/itf.txt.gz` | skip | - | none | Identification tracking data file |
| `/iau/data/skycov.tgz` | skip | - | none | Sky coverage data archive |
| `/Extended_Files/neocp_new.json` | skip | - | none | NEOCP JSON data feed |
| `/iau/lists/Customize.html` | skip | - | none | Observable object customizer (service) |
| `/iau/special/AmateurDiscoveries.txt` | TBD | - | none | Statistics data file; currently commented out in docs |
| `/iau/special/CountObsByYear.txt` | TBD | - | none | Statistics data file; currently commented out in docs |
| `/iau/special/DesignationsStatus.txt` | TBD | - | none | Statistics data file; currently commented out in docs |
| `/iau/special/residuals.txt` | TBD | - | none | Residual statistics by obs code; currently commented out in docs |
| `/iau/special/residuals2.txt` | TBD | - | none | Numbered MP residual statistics; currently commented out in docs |
| `/iau/special/magweights.txt` | TBD | - | none | Magnitude weighting file; currently commented out in docs |
| `/iau/special/posweights.txt` | TBD | - | none | Astrometry weighting file; currently commented out in docs |
| `/iau/info/NonEnglish.html` | migrated | `data-and-services/non-english-characters.md` | redirect-needed | Non-English characters in asteroid names |
| `/iau/info/MPCOpStatus.html` | TBD | - | none | MPC operational status documentation |
| `/iau/ECS/MPCAT/MPCAT.html` | TBD | - | none | Minor planet catalogue export format |
| `/iau/ECS/MPCAT-OBS/MPCAT-OBS.html` | TBD | - | none | Observation catalogue export format |
| `/iau/ECS/MPCUPDATE/MPCUPDATE.html` | TBD | - | none | MPC daily update export format |
| `/iau/ECS/MPCArchive/MPCArchive_TBL.html` | TBD | - | none | MPC archive export format |
| `/iau/Ephemerides/EphemOrbEls.html` | TBD | - | none | Ephemeris/orbit element export format |
| `/iau/Ephemerides/SoftwareEls.html` | TBD | - | none | Software orbit element format |
| `/iau/NatSats/NaturalSatellites.html` | TBD | - | none | Natural satellites hub page |
| `/iau/NEO/TheNEOPage.html` | TBD | - | none | NEO information hub |
| `/iau/artsats/artsats.html` | TBD | - | none | Artificial satellites page |
| `/mpcops/documentation/artificial-satellites/` | TBD | - | none | Artificial satellite observation policy/docs |
| `/mpcops/documentation/neocp-prev-des-removal/` | TBD | - | none | NEOCP previous designation removal policy |
| `/mpcops/orbits/no-orbits-astrometry/` | TBD | - | none | Documentation about astrometry without orbits |
| `/iau/NEO/PossNEO.html` | skip | - | none | Possible NEO list (dynamic) |
| `/iau/NEO/pccp_tabular.html` | skip | - | none | PCCP tabular view (dynamic) |
| `/iau/NEO/ToConfirmRA.html` | skip | - | none | NEOCP sorted by RA (dynamic) |
| `/iau/MPCStatus.html` | skip | - | none | MPC operational status (dynamic) |

### Miscellaneous

| Legacy Path | Migration | New Location | Legacy Banner | Notes                                |
|---|-----------|---|---|--------------------------------------|
| `/iau/info/MPECComputers.html` | deprecate | - | deprecation-needed | Very outdated computer list          |
| `/iau/info/MPES.pdf` | skip      | - | none | Ephemeris Service PDF reference guide |
| `/iau/mpc.html` | TBD      | - | TBD | A copy of the MPC main page ???      |
| `/iau/services/MPCServices.html` | TBD      | - | TBD | MPC *publications* directory  |
| `/mpec/RecentMPECs.html` | skip      | - | none | Recent MPECs index                   |
| `/mpcops/mpecs/` | skip      | - | none | MPEC search tool                     |
| `/mpcops/submissions/cometary/` | skip      | - | none | Cometary submission form             |
| `/media/newsletters/` | skip      | - | none | Newsletter PDFs                      |
| `/iau/MPC_Documentation.html` | TBD | - | none | Master documentation index; useful to audit for completeness |
| `/iau/services/IAUC.html` | TBD | - | none | IAU Circulars information |
| `/iau/services/MPS.html` | TBD | - | none | Minor Planet Supplements information |
| `/iau/services/ECS.html` | TBD | - | none | Electronic Circulars/Supplements |
| `/iau/lists/Lists.html` | skip | - | none | Lists master index (auto-generated) |
| `/iau/lists/MPLists.html` | skip | - | none | Minor planet lists index (auto-generated) |
| `/iau/lists/CometLists.html` | skip | - | none | Comet lists index (auto-generated) |

---

## Classification Rules

- **`migrated`**: Content has been brought into docs-public under `docs/mpc-ops-docs/`
- **`to-migrate`**: Documentation page worth migrating (priority noted: high/medium/low)
- **`deprecate`**: Not worth migrating; will be removed with a deprecation banner
- **`skip`**: Service endpoints, MPECs, auto-generated lists, interactive tools, data files - never migrated, kept as external links
- **`TBD`**: Not yet decided whether to migrate or deprecate; needs further review

## Legacy Banner States

For migrated pages:

1. **`redirect-needed`** - Page migrated but legacy page has no banner yet
2. **`redirect-added`** - Legacy page has a banner saying "This page has moved to docs.minorplanetcenter.net/..."
3. **`removed`** - Legacy page has been taken down

For deprecated pages:

1. **`deprecation-needed`** - Decided to deprecate but no banner yet
2. **`deprecation-added`** - Legacy page has a banner saying "This page will be removed on [date]"
3. **`removed`** - Legacy page has been taken down

## TODO Comment Cross-Reference

The following `<!-- TODO: update link when migrated -->` comments exist in docs-public and reference legacy pages that are tracked above as `to-migrate`:

| File | Legacy URL Referenced | Tracker Status |
|---|---|---|
| `astrometry/index.md` | `/iau/info/commandlinesubmissions.html` | to-migrate |
| `astrometry/index.md` | `/mpcops/documentation/tycho-tracker/` | to-migrate |
| `astrometry/index.md` | `/iau/info/ObsFormat.html` | to-migrate |
| `astrometry/index.md` | `/iau/info/ObsDetails.html` | to-migrate |
| `astrometry/reporting-observations.md` | `/iau/info/ObsFormat.html` | to-migrate |
| `astrometry/reporting-observations.md` | `/iau/info/ADES.html` | to-migrate |
| `astrometry/reporting-observations.md` | `/iau/info/commandlinesubmissions.html` | to-migrate |
| `astrometry/reporting-observations.md` | `/iau/info/ObsDetails.html` | to-migrate |
| `astrometry/reporting-observations.md` | `/iau/services/MPCServices.html` | skip |
| `astrometry/mpc-processing.md` | `/iau/services/MPCServices.html` | skip |
| `astrometry/mpc-processing.md` | `/iau/NEO/NEOCPNotes.html` | to-migrate |
| `astrometry/discoveries-and-credit.md` | `/iau/services/MPCServices.html` | skip |
| `astrometry/discoveries-and-credit.md` | `/iau/info/Coverage.html` | skip |
| `astrometry/observatory-codes.md` | `/iau/info/ObservatoryCodes.html` | to-migrate |
| `astrometry/getting-started.md` | `/iau/mpc.html` | skip |
