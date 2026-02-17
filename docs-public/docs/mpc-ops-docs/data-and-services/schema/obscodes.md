# Schema: obscodes

The obscodes table is a replica of the MPC internal PostgreSQL table. It contains all observatory code information. The [Obscodes API](../../apis/obscodes.md) gets data from this internal PostgreSQL database.

!!! note
    This table contains additional information beyond the public Observatory Codes page, such as whether the observatory uses two-line observations.

| Column | Data type | Description |
|--------|-----------|-------------|
| uses_two_line_observations | boolean | Whether the station needs a second line in MPC-1992 80-column format |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| lastdate | character varying(10) | Last date for the observatory code |
| web_link | text | Station webpage link |
| longitude | numeric | Longitude [degrees east of Greenwich] |
| name_latex | character varying(255) | Name in LaTeX format |
| name_utf8 | character varying(255) | Name in UTF-8 format |
| name | character varying | Name of the station code |
| obscode | character varying(4) | Observatory station code |
| observations_type | character varying(255) | Observation type (optical, radar, satellite, occultation) |
| old_names | character varying[] | Old names for the observatory |
| rhosinphi | numeric | Parallax constant (rho*sin(phi)) |
| rhocosphi | numeric | Parallax constant (rho*cos(phi)) |
| short_name | character varying(255) | Short name for MPC publications |
| firstdate | character varying(10) | Start date for the observatory code |
| id | integer | PostgreSQL automatically generated identifier |

[Back to schema overview](../replicated-tables-schema.md)
