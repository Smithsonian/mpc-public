# MPC Processing

This page covers what happens to observations after they are received by the MPC, including publication, the NEO Confirmation Page, designation assignment, processing times and precovery.


## What happens to accepted observations?

Observations are published with different cadences depending on the type of object that has been reported.

- Observations of NEOs are published daily in the Daily Orbit Update (DOU, e.g. see [MPEC 2023-Q03](https://minorplanetcenter.net/mpec/K23/K23Q03.html)). The DOU is available online from the [Recent MPECs page](https://minorplanetcenter.net/mpec/RecentMPECs.html).
- All the other observations are published in the monthly [_Minor Planet Circulars (MPCs)_](https://minorplanetcenter.net/iau/services/MPCServices.html) or _Supplements_. <!-- TODO: update link when migrated -->
- [_Minor Planet Electronic Circulars_](https://minorplanetcenter.net/iau/services/MPCServices.html) are published for newly discovered NEOs, TNOs and natural satellites. <!-- TODO: update link when migrated -->
- _Observations and orbits of comets and A/ objects_ are also published (~weekly). (e.g. see [MPEC 2023-P65](https://minorplanetcenter.net/mpec/K23/K23P65.html))

As of [MPEC 2023-D40](https://www.minorplanetcenter.net/mpec/K23/K23D40.html) (February 21, 2023), Datacite DOIs are available for all new MPECs. The first published DOI is now available at <https://commons.datacite.org/doi.org/10.48377/mpec/2023-d40>. NASA ADS, based in Cambridge (MA) at the Center for Astrophysics, is in the process of mining the relevant data from Datacite, so that MPECs will be available on their system soon. This will allow all our users to cite their observations in scientific articles or proposals. The MPC is also in the process of creating DOIs for all the MPECs that have been released before February 21.


## What objects go on the NEOCP?

The objects that go on to the [NEO Confirmation Page](https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html) are those objects which, on the basis of their motion or orbit, appear to be NEOs and that have a digest2 score larger than 65. Objects that are suspected of being comets also appear.

[When removed from the NEOCP](https://minorplanetcenter.net/iau/NEO/NEOCPNotes.html), the inner-solar-system objects that get put on to _MPECs_ are as follows: <!-- TODO: update link when migrated -->

- Any object with perihelion distance less than 1.3 AU.
- Any object with a perihelion distance beyond 5.5 AU (Centaurs/SDO and TNOs are not listed in only one-opposition).
- "Main-belt" objects with eccentricities above 0.5.
- Comets.

In the past, objects with perihelia beyond 1.3 AU and eccentricities between 0.4 and 0.5 and/or inclinations above 40 degrees might appear on an _MPEC_ if there was not much activity. This was deemed to be somewhat arbitrary (particularly in light of the fact that the major surveys were counting how many discovery _MPECs_ they had!).


## How do I understand the designations the MPC sends me?

If you have 'new' objects you will receive a list matching your temporary designations to official provisional or permanent designations. Here is a (fictitious) sample assumed to have been sent in Feb. 1999, showing most of the probable forms:

```
By0001   (03244
ByLa01    J99A18T
ByLa02   (J81U78A
By0004   (By0003
By0003   (J99A08H
```

This may be interpreted as follows: By0001 is the numbered object (3244); ByLa01 is a new object 1999 AT18 that is credited to Byers and Langly; ByLa02 is the known unnumbered object 1981 UA78; By0003 and By0004 refer to the same object, now designated 1999 AH8, which is a recent discovery by another team.

In short, provisional and permanent designations _not_ prefaced with '(' are your discoveries. Provisional and permanent designations will be in the [packed form](../designations/packed-designations.md), as used on the observation record.

New designations are not assigned to objects observed on only one night, although you may receive designations if such objects can be identified with already-known objects.


## How quickly are observations processed?

In general, observation batches are processed by the MPC as soon as resources are available, in the order in which the observation batches were received. In order to utilise the resources of the MPC in the most efficient manner, different priorities are attached to the processing of different classes of observation. Processing priority is in the following order:

1. Potential new NEOs/unusual objects and comets, suitable for posting on the [NEO Confirmation Page](https://minorplanetcenter.net/iau/NEO/ToConfirm.html).
2. Follow-up observations of [NEOCP](https://minorplanetcenter.net/iau/NEO/ToConfirm.html) objects.
3. Other NEO observations.
4. Survey observations from last night and recent non-survey material.
5. Older non-survey material.
6. Survey observations from before last night.

Observations that are not submitted in the proper format are subject to delay.

Note that the different processing classes are dealt with at different rates. This does not affect the order in which "new" objects are processed.

The [MPC Processing times](https://minorplanetcenter.net/iau/delays/neocp_delay.html) page reports the current MPC processing status for some of our pipelines with highest priorities.


## What (p)recovered objects get MPECs?

In order to qualify for a special _MPEC_, (p)recovered NEAs must have been observed on two or more nights. When needed, e.g. in the case of virtual impactors, single-night (p)recoveries will simply appear on the next DOU _MPEC_ (assuming that the observations actually fit).

Precovery refers to the identification of images of a single-apparition object at an earlier opposition.

The [Recovery Page](https://minorplanetcenter.net/iau/recovery/recovery.html) provides new unpublished observations of NEOs and TNOs that are extending the arc from one opposition to multiple-oppositions and for which additional observations are highly desirable. Once new observations provide at least two distinct nights on the second apparition, a recovery MPEC will be issued and the published observations will be removed from the page.
