# Schema: obscodes

The obscodes table is a replica of the MPC internal PostgreSQL table. It contains all observatory code information. The [Obscodes API](../../apis/obscodes.md) gets data from this internal PostgreSQL database.

!!! note
    This table contains additional information beyond the public Observatory Codes page, such as whether the observatory uses two-line observations.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier for row of data |
| `obscode` | character varying(4) | Obscode station code |
| `longitude` | numeric | Longitude of the station code (in degrees east of Greenwich) |
| `rhocosphi` | numeric | Parallax constants where phi is the geocentric latitude and rho is the geocentric distance in earth radii |
| `rhosinphi` | numeric | Parallax constants where phi is the geocentric latitude and rho is the geocentric distance in earth radii |
| `name` | character varying | Name of the stations code |
| `owner` | character varying | Name of the owner of the station code |
| `country` | character(2) | Station code country |
| `amateur` | smallint | Integer indicating whether the observer is an amateur |
| `reference` | character varying(16) | MPC reference for the publication of the station code |
| `pos_not_first_ref` | smallint | N/A |
| `firstdate` | character varying(10) | Start date for the observatory code |
| `lastdate` | character varying(10) | Last date for the observatory code |
| `web_link` | text | Link for the station webpage |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |
| `short_name` | character varying(255) | Short name used for MPC publications and files |
| `contact_email` | character varying[] | Email of the contact for the stations code |
| `latitude` | numeric | Latitude of the station code |
| `coordinate_source` | character varying(255) | Source for the coordinate values (e.g. GPS) |
| `elevation` | numeric | Elevation from the sea level |
| `elevation_model` | character varying(255) | Model used to compute the elevations (e.g. WGS84) |
| `uses_two_line_observations` | boolean | Boolean indicating whether the station code needs a second line when the position is reported in the MPC-1992 80-column format (e.g. satellite observations) |
| `old_names` | character varying[] | Old names for the observatory |
| `old_data` | jsonb | Binary json storing an archival version of the information for a given station code |
| `obscode_main` | character varying(4) | Main observatory code. This is used when multiple station are closed to each other. |
| `time_delta_seconds` | real | Delta time in seconds used for grouping near-duplicates |
| `arcsecond_radius` | real | Radius in arcseconds used for grouping near-duplicates |
| `name_utf8` | character varying(255) | Name of the observatory code in UTF-8 format |
| `name_latex` | character varying(255) | Name of the observatory code in latex format |
| `observations_type` | character varying(255) | Observation type (e.g. optical, radar, satellite, occultation) |
| `has_prog_code` | boolean |  |
| `progcode_needs_sarc_approval` | boolean |  |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
