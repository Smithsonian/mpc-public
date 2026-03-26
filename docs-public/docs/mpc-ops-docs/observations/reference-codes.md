# Reference Codes on Observations

Astrometric observations of comets, minor planets, and natural satellites accepted for publication in Minor Planet Circulars (MPCs), Minor Planet Supplements (MPSs), Minor Planet Electronic Circulars, and IAU Circulars receive a publication reference in columns 73-77 of the observation record.


## Temporary References on MPECs

Observations appearing on MPECs receive temporary references that are later replaced by permanent ones when published in MPCs or MPSs.

| Column | Purpose |
|--------|---------|
| 1 | "E" |
| 2 | Half-month of MPEC preparation |
| 3-5 | Circular number within the half-month |

Example: "MPEC 2004-P03" observations use reference `EP003`


## Permanent References

### Five-Digit References (MPC publication <= 99999)

| Column | Purpose |
|--------|---------|
| 1-5 | MPC number |

Example: `24133` = [MPC 24133](https://minorplanetcenter.net/iau/ECS/MPCArchive/1994/MPC_19941118.pdf)

### "@" + Four-Digit References (MPC > 99999)

| Column | Purpose |
|--------|---------|
| 1 | "@" |
| 2-5 | MPC number minus 100000 |

Example: `@0133` = MPC 100133

### "#" + Four Characters (MPC > 109999)

| Column | Purpose |
|--------|---------|
| 1 | "#" |
| 2-5 | Base-62 encoded (MPC number - 110000) |

Uses characters `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`

Example: `#002B` = MPC 110135

### Lower-case Letter + Four Digits (MPS publication)

| Column | Purpose |
|--------|---------|
| 1 | Encoded (MPS number ÷ 10000) |
| 2-5 | (MPS number) MOD 10000 |

Encoding: CHAR(97 + INT(MPS_Number / 10000)). "a" = MPS 1-9999, "b" = MPS 10000-19999, etc.

Examples: `j8391` = MPS 98391, `a0320` = MPS 320, `k0001` = MPS 100001

### Tilde + Four Base-62 Characters (MPS > 260000)

| Column | Purpose |
|--------|---------|
| 1 | "~" |
| 2-5 | Base-62 encoded (MPS number - 260000) |

Examples: `~0000` = MPS 260000, `~007M` = MPS 260456

### Upper-case Letter + Four Digits (Various journals)

| Column | Purpose |
|--------|---------|
| 1 | Journal identifier |
| 2-5 | Circular number |

Journal identifiers:

- **H** = Harvard Announcement Card (HAC)
- **I** = IAU Circular (IAUC)
- **M** = Minor Planet Circulars (MPC)
- **R** = Planetenzirkular des Astronomischen Rechen-Institut (RI)

Examples: `R0034` = RI 34, `I2340` = IAUC 2340


### Two or More Letters (Non-MPC journals)

Journal identifiers range from two to five characters, often including volume or circular numbers.

| ID | Type | Publication |
|----|------|-------------|
| AA | V | Astronomy and Astrophysics |
| AB | C | Bulletin des Astrophysikalischen Observatoriums Abastumani |
| AC | C | Astronomisches Zirkular der Akademie der Wissenschaften der UdSSR |
| AE | V | Astronomical Papers prepared for the use of the American Ephemeris and Nautical Almanac |
| AJ | V | Astronomical Journal |
| AN | V | Astronomische Nachrichten |
| AP | V | Astrophysical Journal Supplement |
| APO | V | Annales de l'Observatoire de Paris: Observations |
| AS | V | Acta Astronomica Sinica |
| AZ | V | Astronomicheskij Zhurnal |
| AcA | V | Acta Astronomica |
| As | V | Astronomy and Astrophysics Supplement |
| BA | V | Bulletin Astronomique |
| BB | V | Bulletin Astronomique de l'Observatoire Royal de Belgique, Uccle |
| BC | V | Bulletin of the Astronomical Institutes of Czechoslovakia |
| BG | V | Bulletin de l'Observatoire Astronomique de Beograd |
| BN | I | Bulletin of the Astronomical Institutes of the Netherlands |
| BP | V | Bulletin de la Societe des amis des sciences et des lettres de Poznan |
| BZ | V | Beobachtungs-Zirkulare der Astronomischen Nachrichten |
| CB | I | Comet Bulletin of the Orient Astronomical Association |
| CC | V | Observatorio Astronomico de Cordoba, Serie Contribuciones |
| CD | I | Tsirkulyari Rasadkhonai Stalinobod |
| CK | V | Izvestiya Krymskoj Astrofizicheskoj Observatorii |
| CM | V | Circulaire de l'Observatoire de Marseille |
| CMC | V | Carlsberg Meridian Circle Publications |
| CO | V | Odesskij Gosudarstvennyj Universitet Izvestiya Astronomicheskoj Observatorii |
| CR | V | Comptes Rendus hebdomadaires de l'academie des sciences de Paris |
| CS | V | Soobshcheniya Gosudarstvennogo Astronomicheskogo Instituta imeni P. K. Shternberga |
| GOxxx | Y | Greenwich Observations for the year 1xxx |
| HA | V | Harvard Annal |
| HD | V | Veroffentlichungen der Landessternwarte Heidelberg |
| HTCDR | - | Hipparcos-Tycho CD-ROM |
| IHW | D | International Halley Watch CD-ROM |
| Ic | V | Icarus |
| JB | V | Journal of the British Astronomical Association |
| JC | C | Japan Astronomical Study Association Circular |
| JO | V | Journal des Observateurs |
| KB | V | Bulletin of the Kwasan Observatory, Kyoto |
| KK | C | Kiev Komet Tsirkular |
| LB | C | Lick Observatory Bulletin |
| LO | C | Lowell Observatory Bulletin |
| LP | V | Publicaciones Observatorio Astronomico de La Plata |
| MN | V | Monthly Notices |
| NA | V | Annales de l'Observatoire de Nice |
| NC | C | Nihondaira Observatory Circular |
| NO | V | Publications of the U.S. Naval Observatory, Second Series |
| NZ | C | Nachrichtenblatt der Astronomischen Zentralstelle |
| OB | V | The Observatory |
| PA | V | Publications of the Astronomical Society of the Pacific |
| PC | C | Poulkovo Observatory Circular |
| PD | V | Tartu Astronoomia Observatooriumi Publikatsioonid |
| PK | V | Pyublikatsii Kievskoj Astronomicheskoj Observatorii |
| PO | I | Perth Observatory Communication |
| PP | I | Izvestiya Glavnoj Astronomicheskoj Observatorii v Pulkove |
| PT | V | Pubblicazioni del Osservatorio di Torino |
| PZ | C | Zirkular des Astronomischen Hauptobservatoriums Pulkowo |
| RA | V | Ricerche Astronomiche |
| RM | V | Memoirs of the Royal Astronomical Society |
| SA | V | Monthly Notices of the Astronomical Society of Southern Africa |
| SOB | V | Observatory Bulletin |
| TB | V | Tokyo Astronomical Bulletin |
| TC | C | Transval Observatory Circular |
| TI | V | Astronomia-Optika Institucio, Universitato de Turku, Informo |
| UC | C | Circular of the Union Observatory, Johannesburg |
| WO | V | Astronomical Observations of the U.S. Naval Observatory, Washington |
| WiA | V | Annalen der Sternwarte der Universitat Wien |
| pM | V | Mitteilungen der Nikolai-Hauptsternwarte zu Pulkowo |

Type notation: V = volume numbers, C = circular numbers, I = issue number, D = CD-ROM numbers, Y = years

Examples: `AN080` = AN 80, `MN008` = MN 8
