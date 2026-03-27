# Updating Locations for Observatory Codes

Observatory codes are assigned to observatories that report astrometric observations of minor planets, comets or irregular natural satellites. New codes are regularly assigned based on new observers or literature extraction. For guidance on obtaining an observatory code, consult the [Guide to Minor Body Astrometry](../astrometry/observatory-codes.md#how-do-i-get-an-observatory-code).

Historical observatory positions derive from 19th and early 20th-century almanac listings. The MPC recommends all positions reference the [WGS84 datum](https://en.wikipedia.org/wiki/World_Geodetic_System). Those with previously reported coordinates are encouraged to remeasure using Google Earth and submit updated values.

The [current list of assigned codes](https://data.minorplanetcenter.net/explorer/?tab=Lists&list=Observatory+Codes) is available online.


## What to Report

Include the following when submitting updated coordinates:

- **Longitude** (sexagesimal format, 0.1" or better precision)
- **Latitude** (sexagesimal format, 0.1" or better precision)
- **Altitude** (meters)
- **Source documentation**
    - For Google Earth: state source name
    - For GPS: specify if altitude references WGS84 ellipsoid or mean sea level
    - Other sources are discouraged
- **Instrument height** above ground (optional, in meters)


### Submission Format Examples

```
COM OC, xxx xx xx.xx E, xx xx xx.xx N, xxxx m, GoogleEarth
COM OC, xxx xx xx.xx E, xx xx xx.xx S, xxxx m, GPS, MSL
COM OC, xxx xx xx.xx W, xx xx xx.xx N, xxxx m, GPS, ELL
COM OC, xxx xx xx.xx E, xx xx xx.xx N, xxxx m, 10 m, GoogleEarth
```

For website reporting:

```
URL OC http://...
```

[Submit updated coordinates](https://cgi.minorplanetcenter.net/cgi-bin/feedback.cgi?U=ObservatoryCodes.html&S=Updated%20Coordinates)


## Known Low-Precision Sites

The following observatories need high-precision coordinate updates via Google Earth:

| Code | Name | Current Coordinates |
|------|------|---------------------|
| 588 | Eremo di Tizzano | 11.25 E, 0.715 N |
| 792 | University of Rhode Island, Quonochontaug | 288.30 E, 0.753 N |
| 863 | Furukawa | 137.18 E, 0.807 N |
| 986 | Ascot | 358.75 E, 0.624 N |
| 989 | Wilfred Hall Observatory, Preston | 357.69 E, 0.600 N |
| E21 | Norma Rose Observatory, Leyburn | 151.5667 E, 0.8838 N |
| E27 | Thornlands | 153.2667 E, 0.8871 N |

Updated coordinates appear in the online observatory code list following the next DOU MPEC issuance.


## Requests for Assistance

Identification help is needed for these historical or unclear sites:

| Code | Site | Coordinates | Issue |
|------|------|-------------|-------|
| 008 | Algiers-Bouzareah | 003°02.1' E 36°48.1' N | Need observatory identification |
| 012 | Uccle | 004°21'30" E 50°47'53" N | Clarify instrument locations |
| 065 | Traunstein | 012°38'24" E 47°52'26" N | Locate observatory site |
| 066 | Athens | 023°43'05.83" E 37°58'24.21" N | Confirm identification |
| 109 | Algiers-Kouba | 003°04.3' E 36°44.3' N | Historical; possibly demolished |
| 556 | Reintal | 011°37.2' E 47°45.4' N | Locate observatory |
| 589 | Santa Lucia Stroncone | 012°40'39.24" E 42°30'22.61" N | Identify dome feature |

Provide identification justification ("I work there," "I've observed there," etc.) when [reporting findings](https://cgi.minorplanetcenter.net/cgi-bin/feedback.cgi?U=ObservatoryCodes.html&S=Updated%20Coordinates).
