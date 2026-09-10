# Schema: neocp_obs

The NEOCP observations table contains observations and corresponding ADES uncertainties for objects currently on the NEOCP.

!!! note
    Fields prefixed with "ADES:" are valid ADES fields.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `desig` | character varying(16) | Observer-assigned object identifier, unique within a submission batch. It could have been altered by the MPC if linking has been performed between NEOCP objects. |
| `trkid` | text | Globally Unique alphanumeric tracklet identifier assigned by MPC |
| `obs80` | character varying(255) | 80 or 160-Character observation string |
| `rmstime` | numeric | random uncertainty in time in seconds as estimated by the observer |
| `rmsra` | numeric | random component of the RA*cos(Dec) uncertainty in arcsec as estimated by the observer |
| `rmsdec` | numeric | random component of the Dec uncertainty in arcsec as estimated by the observer |
| `rmscorr` | numeric | correlation between RA and Dec, as estimated by the observer. This is derived from the RA-Dec covariance matrix, where the off-diagonal term is rmsCorr x rmsRA x rmsDec |
| `force_code` | text | This column is currently unused. |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
