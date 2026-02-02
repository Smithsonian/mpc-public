# Create directory
mkdir -p docs-public/mpc-ops-docs

# Write docs-public/mpc-ops-docs/index.md
cat > docs-public/mpc-ops-docs/index.md <<'EOF'
# MPC Operations Documentation

This page mirrors the links on the [MPC Ops documentation](https://minorplanetcenter.net/mpcops/documentation/) landing page.

It is intended as an alternate entry point for MPC documentation and services.

It is intended that the [MPC Ops documentation](https://minorplanetcenter.net/mpcops/documentation/) landing page
will soon be **replaced** by this simplified page.

---

## Contents

- [FAQs](faqs.md)
- [Astrometry guide](astrometry.md)
- [APIs](apis.md)
- [Replicated PostgreSQL tables](replicated-postgresql.md)
- [ADES](ades.md)
- [Program codes and observatory codes](programs-and-obscodes.md)
- [Singletons and archival observations (SARC)](sarc.md)
- [Negative observations protocol](negative-observations.md)
- [Orbital elements](orbital-elements.md)
- [Orbit and object types](orbit-and-object-types.md)
- [Identifications](identifications.md)
- [Artificial satellites](artificial-satellites.md)
- [Subscriptions](subscriptions.md)
- [Designations](designations.md)
- [Edgar Wilson Award](edgar-wilson-award.md)
EOF

# Write docs-public/mpc-ops-docs/faqs.md
cat > docs-public/mpc-ops-docs/faqs.md <<'EOF'
# FAQs

- [FAQs (index)](https://minorplanetcenter.net/mpcops/documentation/faqs/) — Common questions and answers across MPC operations.
EOF

# Write docs-public/mpc-ops-docs/astrometry.md
cat > docs-public/mpc-ops-docs/astrometry.md <<'EOF'
# MPC Guide to Minor Planet Astrometry

- [How do I begin?](https://minorplanetcenter.net/iau/info/Astrometry.html)
- [How do I report observations to the Minor Planet Center?](https://minorplanetcenter.net/iau/info/Astrometry.html)
- [How do I get an observatory code?](https://minorplanetcenter.net/iau/info/Astrometry.html#HowObsCode)
- [How do I submit my astrometry to the MPC using Tycho Tracker?](https://minorplanetcenter.net/mpcops/documentation/tycho-tracker/)
EOF

# Write docs-public/mpc-ops-docs/apis.md
cat > docs-public/mpc-ops-docs/apis.md <<'EOF'
# APIs (MPC APIs)

- [Where Are My Observations (WAMO)](https://minorplanetcenter.net/mpcops/documentation/wamo-api/)
- [Submission Status](https://minorplanetcenter.net/mpcops/documentation/submission-status-api/)
- [Designation Identifier](https://minorplanetcenter.net/mpcops/documentation/designation-identifier-api/)
- [Observations](https://minorplanetcenter.net/mpcops/documentation/observations-api/)
- [NEOCP Observations](https://minorplanetcenter.net/mpcops/documentation/neocp-observations-api/)
- [Check Near-Duplicates (CND)](https://minorplanetcenter.net/mpcops/documentation/cnd-api/)
- [Orbits](https://minorplanetcenter.net/mpcops/documentation/orbits-api/)
- [Observatory Codes](https://minorplanetcenter.net/mpcops/documentation/obscodes-api/)
- [MPECs](https://minorplanetcenter.net/mpcops/documentation/mpecs-api/)
- [Action Codes](https://minorplanetcenter.net/mpcops/documentation/action-codes-api/)
- [Lists of Objects](https://minorplanetcenter.net/mpcops/documentation/list-api/)
EOF

# Write docs-public/mpc-ops-docs/replicated-postgresql.md
cat > docs-public/mpc-ops-docs/replicated-postgresql.md <<'EOF'
# Replicated PostgreSQL Tables

- [Introduction and examples](https://minorplanetcenter.net/mpcops/documentation/replicated-tables-info-general/)
- [Schema](https://minorplanetcenter.net/mpcops/documentation/replicated-tables-schema/)
EOF

# Write docs-public/mpc-ops-docs/ades.md
cat > docs-public/mpc-ops-docs/ades.md <<'EOF'
# ADES (Astrometric Data Exchange Standard)

- [Introduction](https://minorplanetcenter.net/mpcops/documentation/ades/)
- [Valid ADES values](https://minorplanetcenter.net/mpcops/documentation/valid-ades-values)
- [ADES GitHub repository](https://github.com/IAU-ADES/ADES-Master/)
- [Official ADES format description (PDF)](https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf)
EOF

# Write docs-public/mpc-ops-docs/programs-and-obscodes.md
cat > docs-public/mpc-ops-docs/programs-and-obscodes.md <<'EOF'
# Program Codes and Observatory Codes

## Useful lists

- [Valid ADES values](https://minorplanetcenter.net/mpcops/documentation/valid-ades-values)
- [Program Codes](https://minorplanetcenter.net/mpcops/documentation/program-codes/)
- [Observatory codes](https://minorplanetcenter.net/iau/lists/ObsCodesF.html)

## Policy and APIs

- [Program Codes policy](https://minorplanetcenter.net/mpcops/documentation/program-codes-policy/)
- [Program Codes](https://minorplanetcenter.net/mpcops/documentation/program-codes/)
- [Observatory codes](https://minorplanetcenter.net/iau/lists/ObsCodesF.html)
- [How do I obtain an observatory code?](https://minorplanetcenter.net/iau/info/Astrometry.html#HowObsCode)
- [Observatory codes API](https://minorplanetcenter.net/mpcops/documentation/obscodes-api/)
EOF

# Write docs-public/mpc-ops-docs/sarc.md
cat > docs-public/mpc-ops-docs/sarc.md <<'EOF'
# Singletons and Archival Observations (SARC)

- [Singletons and archival observations committee (SARC)](https://minorplanetcenter.net/mpcops/documentation/sarc/)
EOF

# Write docs-public/mpc-ops-docs/negative-observations.md
cat > docs-public/mpc-ops-docs/negative-observations.md <<'EOF'
# Negative Observations Protocol

- [Protocol for Negative Observations for Virtual Impactors](https://minorplanetcenter.net/mpcops/documentation/negative-observations/)
EOF

# Write docs-public/mpc-ops-docs/orbital-elements.md
cat > docs-public/mpc-ops-docs/orbital-elements.md <<'EOF'
# Orbital Elements

- [MPC_ORB JSON](https://minorplanetcenter.net/mpcops/documentation/mpc-orb-json/)
- [Orbital elements in the *ele220* format](https://minorplanetcenter.net/mpcops/documentation/ele220/)
- [Standard export format for minor-planet orbits](https://minorplanetcenter.net/iau/info/MPOrbitFormat.html)
EOF

# Write docs-public/mpc-ops-docs/orbit-and-object-types.md
cat > docs-public/mpc-ops-docs/orbit-and-object-types.md <<'EOF'
# Orbit and Object Types

- [Orbit Type Definition](https://minorplanetcenter.net/mpcops/documentation/orbit-types/)
- [Object Type Definition](https://minorplanetcenter.net/mpcops/documentation/object-types/)
EOF

# Write docs-public/mpc-ops-docs/identifications.md
cat > docs-public/mpc-ops-docs/identifications.md <<'EOF'
# Identifications

- [Identifications (overview)](https://minorplanetcenter.net/mpcops/documentation/identifications/)
- [Submission Format](https://minorplanetcenter.net/mpcops/documentation/identifications/submission-format/)
- [Submit Identifications](https://minorplanetcenter.net/mpcops/submissions/identifications/)
- [MPC criteria for accepting or rejecting identifications](https://minorplanetcenter.net/mpcops/documentation/identifications/additional/)
EOF

# Write docs-public/mpc-ops-docs/artificial-satellites.md
cat > docs-public/mpc-ops-docs/artificial-satellites.md <<'EOF'
# Artificial Satellites

- [MPC Policy on Disposition and Distribution of Observations on Artificial Satellites](https://minorplanetcenter.net/mpcops/documentation/artificial-satellites/#mpc-artsat-obs-policy)
- [Artificial Satellites on the NEOCP](https://minorplanetcenter.net/mpcops/documentation/artificial-satellites/#neocp-artsats)
EOF

# Write docs-public/mpc-ops-docs/subscriptions.md
cat > docs-public/mpc-ops-docs/subscriptions.md <<'EOF'
# Subscription to MPC Notification Services

- [Subscribe to MPECs and MPC announcement services](https://mpc-service.atlassian.net/servicedesk/customer/portal/18)
EOF

# Write docs-public/mpc-ops-docs/designations.md
cat > docs-public/mpc-ops-docs/designations.md <<'EOF'
# Designations

## Minor Planets

- [Provisional designation definition for minor planets](https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/)

## Comets

- [Cometary Designations](https://www.minorplanetcenter.net/iau/lists/CometResolution.html)
EOF

# Write docs-public/mpc-ops-docs/edgar-wilson-award.md
cat > docs-public/mpc-ops-docs/edgar-wilson-award.md <<'EOF'
# Edgar Wilson Award

- [Award Information](https://minorplanetcenter.net/mpcops/documentation/edgar-wilson-award-information/)
- [Award Winners](https://minorplanetcenter.net/mpcops/documentation/edgar-wilson-award-winners/)
EOF

echo "Done. Created docs-public/mpc-ops-docs/*.md"

