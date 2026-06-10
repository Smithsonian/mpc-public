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


## Assigned Program Codes

Information on assigned program codes is accessible in two formats:

1. [Plain text format](https://minorplanetcenter.net/iau/lists/ProgramCodes.txt)
2. [JSON format](https://minorplanetcenter.net/static/downloadable-files/program_codes.json)


## Quality Monitoring

The MPC continuously evaluates the astrometric quality of all submitted observations. Prior to assigning new observatory codes, the organization performs thorough verification of the astrometry provided by users requesting codes. Detailed instructions are available in the [astrometry guide](observatory-codes.md#how-do-i-get-an-observatory-code).


## Policy Changes

Previously, program-code assignments had not received the same level of scrutiny as observatory code assignments. This is changing.

**Effective August 4th, 2025**, a program code will be assigned by default to all new observatory codes.

Additional refinements regarding program code assignments for archival observations and non-historical stations are in development, with further details to be announced.

[//]: # (TODO: Link in SARC policy stuff)
