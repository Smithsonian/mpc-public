# Schema: neocp_obs

The NEOCP observations table contains observations and corresponding ADES uncertainties for objects currently on the NEOCP.

!!! note
    Fields prefixed with "ADES:" are valid ADES fields.

| Column | Data type | Description |
|--------|-----------|-------------|
| obs80 | character varying(255) | 80 or 160-character observation string |
| rmscorr | numeric | ADES: RA-Dec correlation |
| rmsdec | numeric | ADES: Dec uncertainty [arcsec] |
| rmsra | numeric | ADES: RA*cos(Dec) uncertainty [arcsec] |
| rmstime | numeric | ADES: Time uncertainty [seconds] |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| trkid | text | Globally unique tracklet identifier (MPC) |
| desig | character varying(16) | Observer-assigned object identifier |
| id | integer | PostgreSQL automatically generated identifier |
| force_code | text | Currently unused |

[Back to schema overview](../replicated-tables-schema.md)
