# Program Codes

The Minor Planet Center assigns program codes to identify different observers using the same telescope. These codes distinguish between multiple observation programs at individual facilities.


## Format Differences

The MPC1992 80-column format and ADES format differ in their program code representation. In ADES and the `obs_sbn` table, the `prog` field uses base-62 encoding of the progressive number assigned to each program code. Single-character representations exist for codes up to progressive number 93. Beyond that threshold, no single-character representation exists, so the program code field remains blank in the 80-column format.


## Allowed Program Code Values

The comprehensive listing includes:

- **Observatory Code**: The MPC's designation for each observatory
- **Program Code**: Single-character identifier assigned by the MPC to each observer
- **Program Code Progressive Number**: Sequential number assigned to the program code
- **Program Code in Base62**: Base-62 conversion of the progressive number
- **Contact Name**: Primary observer's name
- **Additional Coinvestigators**: Collaborating researchers (same code applies to all)


## Available Formats

The program codes data is accessible in two formats:

1. **Legacy Format**: [Plain text file](https://minorplanetcenter.net/iau/lists/ProgramCodes.txt)
2. **Modern Format**: [JSON file](https://minorplanetcenter.net/static/downloadable-files/program_codes.json)

For additional context, consult the [program codes policy](program-codes-policy.md) regarding code assignment procedures.
