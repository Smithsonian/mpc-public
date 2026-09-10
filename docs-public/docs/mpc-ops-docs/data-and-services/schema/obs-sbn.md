# Schema: obs_sbn

The observations table is a replica of the MPC internal PostgreSQL table. It contains all published observations and Isolated Tracklet File (ITF) observations.

## Known issues

!!! warning
    - **Missing observations:** Some observations present in flat files are missing from the database (on the order of hundreds of old observations).
    - **Duplicate observations:** Multiple entries with the same `obs80_bit` and station code.
    - **Near-duplicate observations:** Remeasurements sent without MPC knowing.
    - **Fields with invalid values:** See MPC Explorer for details.

## Useful information

- Do NOT compare to `db_search` (which uses MariaDB, being retired). The `obs_sbn` data is more reliable.
- For duplicates, keep the more recent one or the one with more information.
- Fields prefixed "ADES:" are valid ADES fields; "MPC_ops:" are MPC internal operations fields.


<!-- The column tables below are generated from the authoritative replicated-schema definitions (column names, types and comments). -->

## ADES Fields

| Column | Data type | Description |
|--------|-----------|-------------|
| `trksub` | text | Observer-assigned object identifier, unique within a submission batch |
| `trkid` | text | Globally unique tracklet identifier assigned by the MPC |
| `obsid` | text | Globally unique observation identifier assigned by the MPC |
| `ref` | text | Standard reference field used for citations |
| `permid` | text | IAU permanent designation (e.g. the IAU number for a numbered minor planet) |
| `provid` | text | unpacked MPC assigned provisional designation (for more information see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/) |
| `artsat` | text | Artificial satellite identifier |
| `mode` | text | mode of instrumentation (for the documentation on valid values, see https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#mode) |
| `stn` | text | Observatory code assigned by the MPC for ground-based or spaced-based stations (for the documentation on valid values, see https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#stn) |
| `trx` | text | Station codes of transmitting antenna for radar observations |
| `rcv` | text | Station codes of receiving antenna for radar observations |
| `sys` | text | Coordinate frame for roving or space-based station coordinates (for the documentation on valid values, see https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#sys) |
| `ctr` | integer | Origin of the reference system given by the coordinate frame (sys). Use public SPICE codes for possible values (https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/naif_ids.html), e.g. 399=geocenter |
| `pos1` | numeric | Position of the observer (see https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf) |
| `pos2` | numeric | Position of the observer (see https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf) |
| `pos3` | numeric | Position of the observer (see https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf) |
| `poscov11` | numeric | Element (1,1) of the upper triangular part of the covariance matrix for the observer position in the same units of position coordinates. Missing fields are presumed zero. |
| `poscov12` | numeric | Element (1,2) of the upper triangular part of the covariance matrix for the observer position in the same units of position coordinates. Missing fields are presumed zero. |
| `poscov13` | numeric | Element (1,3) of the upper triangular part of the covariance matrix for the observer position in the same units of position coordinates. Missing fields are presumed zero. |
| `poscov22` | numeric | Element (2,2) of the upper triangular part of the covariance matrix for the observer position in the same units of position coordinates. Missing fields are presumed zero. |
| `poscov23` | numeric | Element (2,3) of the upper triangular part of the covariance matrix for the observer position in the same units of position coordinates. Missing fields are presumed zero. |
| `poscov33` | numeric | Element (3,3) of the upper triangular part of the covariance matrix for the observer position in the same units of position coordinates. Missing fields are presumed zero. |
| `prog` | text | Program code assigned by the MPC |
| `obstime` | text | UTC date and time of the observation. |
| `ra` | numeric | Right Ascension is decimal degrees in J2000.0 reference frame |
| `dec` | numeric | Declination is decimal degrees in J2000.0 reference frame |
| `rastar` | numeric | For occultation, only when stn=244, Right Ascension in the J2000.0 reference frame in decimal degress of the occulted star. |
| `decstar` | numeric | For occultation, only when stn=244, Declination in the J2000.0 reference frame in decimal degress of the occulted star. |
| `obscenter` | text | Origin of offset observations (full name of a planet or permID or provID for a small body) |
| `deltara` | numeric | Measured DeltaRA*cos(Dec) in arcsec in the J2000.0 reference frame for offset measurements of a satellite with respect to osbCenter, or for occultation observations with respect to the star (stn=244) |
| `deltadec` | numeric | Measured DeltaDec in arcsec in the J2000.0 reference frame for offset measurements of a satellite with respect to osbCenter, or for occultation observations with respect to the star (only if stn=244) |
| `dist` | numeric | Measured distance in arcsec in degrees in the J2000.0 reference frame for offset measurements of a satellite wrt obsCenter, or for occultation observations wrt the star (only if stn=244) |
| `pa` | numeric | Measured Position Angle in arcsec in degrees in the J2000.0 reference frame for offset measurements of a satellite wrt obsCenter, or for occultation observations wrt the star (only if stn=244) |
| `rmsra` | numeric | Random component of the RA*cos(Dec) uncertainty in arcsec as estimated by the observer |
| `rmsdec` | numeric | Random component of the Dec uncertainty in arcsec as estimated by the observer |
| `rmsdist` | numeric | Random component of the distance uncertainty in arcsec as estimated by the observer |
| `rmspa` | numeric | Random component of the position angle uncertainty in arcsec as estimated by the observer |
| `rmscorr` | numeric | Correlation between RA and Dec or between distance and position angle. This is derived from the covariance matrix, where the off-diagonal term is rmsCorr x rmsRA x rmsDec (for RA and Dec), and rmsCorr x rmsdist x rmspa (for dist and pa) |
| `delay` | numeric | Observed radar time delay in seconds |
| `rmsdelay` | numeric | Delay uncertainty in microseconds |
| `doppler` | numeric | Observed radar Doppler shift in Hz |
| `rmsdoppler` | numeric | Doppler shift uncertainty in Hz |
| `astcat` | text | Star catalog used for the astrometric reduction or, in case of occultation observations, for the occulted star (a list of accepted astcat values is availble at the following link https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#astCat) |
| `mag` | numeric | Apparent magnitude in specified band |
| `rmsmag` | numeric | Apparent magnitude uncertainty in magnitudes |
| `band` | text | Passband designation for photometry (a list of accepted astcat values is availble at the following link https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#band) |
| `photcat` | text | Star catalog used for the photometric reduction (a list of accepted astcat values is availble at the following link https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#astCat) |
| `photap` | numeric | Photometric aperture radius in arcsec |
| `nucmag` | smallint | Nuclear magnitude flag for comets, primarily used for archival data (photap should be used to communicate information in the new standard). 1=True for archival cometary nuclear magnitude measurements, 0=False otherwise. |
| `logsnr` | numeric | The log10 of the signal-to-noise ratio of the source in the image integrated on the entire aperture used for astrometric centroid |
| `seeing` | numeric | Size of seeing disc in arcsec, measured at Full-Width, Half-Max of the target point spread function |
| `exp` | numeric | Exposure time in seconds |
| `rmsfit` | numeric | RMS of fit of astrometric comparison stars in arcsec |
| `com` | smallint | Flag to indicate that the observation is reduced to the center of mass. Values are 1=True, 0=False. False implies a measurement to the peak power position |
| `frq` | numeric | Carrier reference frequency in MHz |
| `disc` | character(1) | Discovery flag (more documentation needs to be added here). |
| `subfrm` | text | Originally reported reference frame for angular measurements. The subfrm does not reflect the frame of the associated ADES observations, which are always J2000.0. For example, B1950.0 corresponds to the letter A in column 14 in the 80-column format |
| `subfmt` | text | Format in which the observation was originally submitted to the MPC. This is filled by the MPC (a list of accepted astcat values is availble at the following link https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#subfmt) |
| `prectime` | integer | Precision in millionths of a day of the reported observation time for archival MPC1992 observations and earlier data |
| `precra` | numeric | Precision for archival MPC1992 observations or earlier data in seconds for RA |
| `precdec` | numeric | Precision for archival MPC1992 observations or earlier data in arcsec for Dec |
| `unctime` | numeric | Estimated systematic time error in seconds. This field indicates a presumed level of systematic clock error. |
| `notes` | text | A set of one-character note flags to communicate observing circumstances (a list of accepted notes values is availble at the following link https://minorplanetcenter.net/mpcops/documentation/valid-ades-values/#notes |
| `remarks` | text | A comment provided by the observer. |
| `deprecated` | character(1) | Deprecated observation that is preserved for historical purpose. Do not use it in the orbit fitting. The only allowed value is X |
| `localuse` | text | Container to hold subelements carrying ancillary information not envisioned by the standard |
| `nstars` | integer | Number of stars in the astrometric fit |
| `rmstime` | numeric | Random uncertainty in time as estimated by the observer |
| `trkmpc` | text | MPC-internal object identifier |
| `shapeocc` | boolean | For occultation observations, a flag to indicate that the observation reduction assumes a shape-based plane-of-sky cross-section. Values are 1=True or 0=False that implies that a circular cross section was assumed |
| `obssubid` | text | Observation identifier, optionally included by the observer in the submission, that is unique to a given observing program |

## MPC Operations Fields

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `submission_id` | text | Unique MPC-assigned submission ID |
| `submission_block_id` | text | Unique MPC-assigned submission block ID |
| `obs80` | text | 80 or 160-Character observation string |
| `status` | character(1) | processing status. Allowed values are: P for ufficially published in a circular (DOU, mid-month, monthly), p for accepted and waiting for publication in the next circular, I for ITF observations |
| `healpix` | bigint | A convenience calculation that maps the observed (Ra,Dec) to a healpix (healpix.sourceforge.io) patch of the sky indicated by the recorded integer. The chosen mapping assumes nside = 32768 & nested = True (see https://astropy-healpix.readthedocs.io/en/latest/coordinates.html), corresponding to a pixel scale of approx 6.4 arcsec. |
| `prev_desig` | text | Previous designation for a redesignated observations (see also the obs_alteration_redesignations table https://minorplanetcenter.net/mpcops/documentation/obs-alterations-redesignations/) |
| `prev_ref` | text | Previous publication references |
| `created_at` | timestamp with time zone | Date and time of initial row insert |
| `updated_at` | timestamp with time zone | Date and time of latest row update |
| `orbit_id` | text | Unique identifier for the orbit calculation. This field is not currently used |
| `designation_asterisk` | boolean | Equivalent of the asterisks used to mark initial tracklets for component provisional designations. One object can have multiple discovery_asterisks |
| `all_pub_ref` | text[] | Array of publication references that contained any information about the observation |
| `replacesobsid` | text | Observation identifier of the old published observations that has been replaced by this new observation. This field is not currently used. |
| `group_id` | text | Observation group identifier used to group duplicate/near-duplicate observations. This field is not currently used |

## Other Fields

| Column | Data type | Description |
|--------|-----------|-------------|
| `desig` | character(12) | MPC designation associated with the observation. |
| `orig_mag_band` | character(1) |  |
| `orig_obs_note` | character(1) |  |
| `obs80_bit` | character(42) | Stable 42-character slice of `obs80` (characters 16–57), used as a join key. |
| `orbit_type` | smallint |  |
| `permid_pkd` | text | Packed form of the IAU permanent designation (number). |
| `provid_pkd` | text | Packed form of the MPC provisional designation. |
| `frag` | text |  |
| `prev_obsid` | text |  |
| `mpc1992_date` | text | Observation date in the MPC 1992 (80-column) format. |
| `mpc1992_ra` | text | Right Ascension in the MPC 1992 (80-column) format. |
| `mpc1992_decl` | text | Declination in the MPC 1992 (80-column) format. |
| `prev_desig_pkd` | text | Packed form of the previous designation. |
| `trackpa` | numeric |  |
| `rmsalongtrack` | numeric |  |
| `rmscrosstrack` | numeric |  |
| `iau_desig` | text | IAU designation. |
| `desig_disc` | character(1) |  |
| `pending_publication` | text |  |
| `has_previous_designation` | boolean |  |
| `flag_consistent_obs` | boolean |  |
| `flag_all_object_obs_consistent` | boolean |  |
| `flag_allowed_external` | boolean |  |
| `action_required_consistency` | integer |  |
| `mpc1992_label` | text | Object label in the MPC 1992 (80-column) format. |
| `discovery_obs_flag` | boolean |  |
| `primary_provisional_packed_designation` | text | Packed primary provisional designation. |
| `init_mpec_ref` | text |  |
| `vel1` | numeric | Observer velocity, component 1 (space-based / roving stations). |
| `vel2` | numeric | Observer velocity, component 2 (space-based / roving stations). |
| `vel3` | numeric | Observer velocity, component 3 (space-based / roving stations). |
| `fltr` | character(3) | Filter |

[Back to schema overview](../replicated-tables-schema.md)
