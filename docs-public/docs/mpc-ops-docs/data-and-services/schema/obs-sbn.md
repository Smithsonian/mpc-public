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

## ADES Fields

| Column | Data type | Description |
|--------|-----------|-------------|
| remarks | text | Observer comment |
| mag | numeric | Apparent magnitude |
| rmsmag | numeric | Magnitude uncertainty |
| artsat | text | Artificial satellite identifier |
| notes | text | One-character note flags |
| frq | numeric | Carrier reference frequency [MHz] |
| localuse | text | Ancillary information container |
| sys | text | Coordinate frame for roving/space-based stations |
| rmscorr | numeric | RA-Dec correlation |
| dec | numeric | Declination [decimal degrees, J2000.0] |
| rmsdelay | numeric | Delay uncertainty [microseconds] |
| deprecated | character(1) | Deprecated observation (X=deprecated) |
| disc | character(1) | Discovery flag |
| rmsdoppler | numeric | Doppler shift uncertainty [Hz] |
| poscov11 through poscov33 | numeric | Position covariance matrix elements |
| unctime | numeric | Estimated systematic time error [seconds] |
| exp | numeric | Exposure time [seconds] |
| com | smallint | Center-of-mass flag (1=True, 0=False) |
| subfmt | text | Original submission format |
| shapeocc | boolean | Shape-based occultation flag |
| decstar | numeric | Occulted star Dec (stn=244) |
| rastar | numeric | Occulted star RA (stn=244) |
| obsid | text | Globally unique observation ID (MPC) |
| trkid | text | Globally unique tracklet ID (MPC) |
| permid | text | IAU permanent designation |
| deltadec | numeric | DeltaDec [arcsec, J2000.0] |
| deltara | numeric | DeltaRA*cos(Dec) [arcsec, J2000.0] |
| dist | numeric | Measured distance [degrees, J2000.0] |
| pa | numeric | Position angle [degrees, J2000.0] |
| mode | text | Instrumentation mode |
| trkmpc | text | MPC-internal object identifier |
| nucmag | smallint | Nuclear magnitude flag for comets |
| nstars | integer | Number of stars in astrometric fit |
| obssubid | text | Observer-included submission ID |
| stn | text | Observatory code |
| doppler | numeric | Radar Doppler shift [Hz] |
| delay | numeric | Radar time delay [seconds] |
| trksub | text | Observer-assigned object ID |
| subfrm | text | Original reported reference frame |
| obscenter | text | Origin of offset observations |
| ctr | integer | Origin of reference system (SPICE code) |
| band | text | Passband for photometry |
| photap | numeric | Photometric aperture radius [arcsec] |
| pos1, pos2, pos3 | numeric | Observer position |
| precdec | numeric | Archival Dec precision [arcsec] |
| precra | numeric | Archival RA precision [seconds] |
| prectime | integer | Archival time precision [millionths of day] |
| prog | text | Program code |
| rmsdec | numeric | Dec uncertainty [arcsec] |
| rmsdist | numeric | Distance uncertainty [arcsec] |
| rmspa | numeric | Position angle uncertainty [arcsec] |
| rmsra | numeric | RA*cos(Dec) uncertainty [arcsec] |
| rmstime | numeric | Time uncertainty |
| ra | numeric | Right Ascension [decimal degrees, J2000.0] |
| rmsfit | numeric | RMS of astrometric fit [arcsec] |
| seeing | numeric | Seeing disc [arcsec, FWHM] |
| ref | text | Standard reference/citation |
| astcat | text | Star catalog (astrometry) |
| photcat | text | Star catalog (photometry) |
| rcv | text | Receiving antenna (radar) |
| trx | text | Transmitting antenna (radar) |
| logsnr | numeric | log10(SNR) |
| provid | text | Unpacked provisional designation |
| obstime | timestamp(6) without time zone | UTC observation date/time |

## MPC Operations Fields

| Column | Data type | Description |
|--------|-----------|-------------|
| obs80 | text | 80 or 160-character observation string |
| healpix | bigint | HEALPix index (nside=32768, nested, ~6.4 arcsec pixel) |
| all_pub_ref | text[] | All publication references for the observation |
| created_at | timestamp(6) with time zone | Date and time of initial row insert |
| updated_at | timestamp(6) with time zone | Date and time of latest row update |
| designation_asterisk | boolean | Marks initial tracklets for component provisional designations |
| group_id | text | Duplicate grouping (not currently used) |
| replacesobsid | text | Replaced observation ID (not currently used) |
| id | integer | PostgreSQL auto-generated identifier |
| prev_desig | text | Previous designation for redesignated observations |
| prev_ref | text | Previous publication references |
| status | character(1) | P=published, p=accepted/waiting, I=ITF |
| orbit_id | text | Orbit calculation ID (not currently used) |
| submission_block_id | text | Unique submission block ID |
| submission_id | text | Unique submission ID |

## Other Fields

| Column | Data type | Description |
|--------|-----------|-------------|
| vel1, vel2, vel3 | numeric | Velocity components |
| fltr | character(3) | Filter |
| obstime_text | text | Observation time as text |

[Back to schema overview](../replicated-tables-schema.md)
