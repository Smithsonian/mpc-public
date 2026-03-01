# Identifications

The Minor Planet Center (MPC) uses the term "identification" to refer to the situations
when:

- Two or more tracklets are discovered to be the same underlying object and hence a new
  designation is created. We refer to this kind of link as **ITF-to-ITF**.
- A tracklet is discovered to be the same underlying object as an existing designated
  object or of a NEOCP object. We refer to this kind of link as **ITF-to-DES** or
  **ITF-to-NEOCP**.
- Two or more designated orbits are discovered to be the same underlying object and hence
  an identification is made between their designations. We refer to this kind of link as
  **DES-to-DES**.
- Two or more objects on the NEOCP are linked together. We refer to this kind of link as
  **NEOCP-to-NEOCP**.

The MPC allows and encourages external users to submit suggested identifications, 
which are then processed by an automated `Identifications Pipeline`. 
The criteria adopted by the pipeline for the acceptance or rejection of submitted identifications are 
described and linked below. 
The pipeline is designed to process a large volume of submissions, and is designed to be conservative/cautious 
in accepting identifications, in order to minimize the number of false positives.

## Documentation

<div class="contents-grid"></div>

- [Identifications API](../apis/identifications.md)
- [MPC criteria for accepting or rejecting identifications](acceptance-criteria.md)
- [Tutorial on Identification Submission API](https://docs.minorplanetcenter.net/tutorials/notebooks/mpc_tutorial_api_identifications)

## Submit Identifications

- [Submit identifications (upload form)](https://minorplanetcenter.net/mpcops/submissions/identifications/)


---

## The Identifications Pipeline

Identifications can be submitted by users for any of these linkage types.

- The pipeline attempts to automatically process any object type submitted.

- NEO and MBA linkages are processed automatically.
- ITF tracklets can be added to an NEOCP candidate.
- Two NEOCP candidates can be linked to one another while on the NEOCP.
- NEOCP candidates can be linked to a known object (and will subsequently be removed
  from the NEOCP).
- NEOCP candidates can be labeled as artificial, as long as sat_id identifies them as
  well. The same applies to ITF tracklets.
- The automated processing will fail for parabolic and hyperbolic orbits.
- The automated processing will *likely fail* for distant objects (such as TNOs) and
  Natural Satellites.
- Comets are not processed automatically.
- If an NEOCP candidate is matched with a known one-opposition NEO and new astrometry
  extends the arc to multiple-opposition, a recovery MPEC is issued if new astrometry
  provides two distinct nights: two nights are defined when the arc length of the NEOCP
  object covers more than 0.75 days (or covers more than 0.5 day when the astrometry is
  from at least three distinct obscodes).
- Single tracklets or shorter arcs extending NEO or TNO from one-opposition to
  multi-oppositions are moved to the
  [recovery page](https://minorplanetcenter.net/iau/recovery/recovery.html).
- Identifications of numbered objects with unnumbered objects are processed immediately
  by the pipeline, but only published during MPCs.

- If a linkage is approved for a Comet, Natural Satellite, or a TNO which requires an
  MPEC, the object is sent to a manual queue for publication.
- We strongly discourage the submission of links that only provide single tracklet on a
  new apparition - that could be a false positive. At least two tracklets on the same
  apparition usually proves the link is correct.


## Processing Timelines and Status

The identifications pipeline can process up to approximately 1,000 linkages per day.
However, other internal MPC processes or procedures with higher priority may pause or
slow down the ID pipeline.

- The current status of the identification pipeline can be viewed
  [here](https://minorplanetcenter.net/iau/delays/neocp_delay.html).
- The identification pipeline runs every 5 minutes, fetching unprocessed submissions,
  prioritizing NEOCP submissions. We suggest submitting smaller batches (<= 100
  identifications) and waiting until the batches are processed before submitting new
  ones.
- Designation-to-Designation linking (DES-DES) is suspended while MPC publications are
  being prepared. Submitted linkages will be processed after the MPCs are published.
- The identifications pipeline is paused while the DAILY ORBIT UPDATE (DOU) is being
  prepared (12:00 UTC), the pause takes usually 20-60 minutes.
- The MPC reviews every week all the submissions that have failed in the pipeline. As a
  result, additional linkages may be manually accepted. Please note that the fraction of
  failed identifications is very small, usually between 1% and 2%.
- Comets, Natural Satellites, and (most) TNOs are manually processed. This may take a
  few weeks. If your linkage is time critical in some way, please submit a
  [Jira ticket](https://mpc-service.atlassian.net/servicedesk/customer/portals).
- If you have any doubts about the status of your submission, please contact us using the
  [Jira Helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portals).


## Submitting Identifications

Identifications can be submitted using the
[file upload form](https://minorplanetcenter.net/mpcops/submissions/identifications/) or
using the API ([documentation](../apis/identifications.md), [tutorial](https://docs.minorplanetcenter.net/tutorials/notebooks/mpc_tutorial_api_identifications.html)).
Before submitting your identifications please read through the documentation on the
required format. See below for various links.

- [Identifications API](../apis/identifications.md)
- [Submit identifications](https://minorplanetcenter.net/mpcops/submissions/identifications/)
- [MPC criteria for accepting identifications](acceptance-criteria.md)

!!! warning
    The submission form does not currently support:

    - The deletion of identifications.
    - Designations that need to be retired.
    - Identifications where some tracklets need to be redesignated before the
      identification can be processed.


## Failed Submissions

If you'd like to receive an automated message when your submitted linkage failed in the
ID pipeline, please add the following text in the comment section: `REPLY_EMAIL` and
don't forget to submit your email address as well in the
[submission header](../apis/identifications.md).

Potential reasons for failures:

- The User has submitted the observations of a single night that extends one apparition
  to two oppositions. This is not allowed.
- Short arc issue: minimum conditions not met (See the
  [criteria](acceptance-criteria.md)).
- The User has requested to link two one-apparition TNOs. This is not allowed.
- The User has submitted an arc extension for a one apparition TNO. At present, this is
  not automated and it won't be handled by the pipeline.
- Near duplicates present - detection(s) of submitted ITF tracklet as part of a submitted
  linkage is very close (spatially - 2 arc seconds, temporally - 2 seconds) to another
  ITF or published detection(s).
- The orbit fit failed.
- The following designation is not allowed \<DESIGNATION\> - e.g. designations starting
  with K15B and K14W cannot be currently created until the
  [Extended Packed Provisional Designation Scheme](../designations/provisional-designations.md#extended-packed-provisional-designation-scheme)
  is implemented.
- NEW NEO Identified from ITF to ITF: MPEC Needed (MPEC for NEO is issued manually).
- Not enough nights in a multi-apparition ITFITF orbit (See the
  [criteria](acceptance-criteria.md)).
- ITF to ITF object is too large - New ITFITF objects that are unusually large (measured
  by the absolute magnitude H) are left for manual processing: NEOs H<17, Mars-Crossers
  H<16.5, inner and central MB H<16, outer MB H<15.5, Hildas and Trojans H<14.
- Designation does not exist.


## Double Designations

A subset of identifications is made between objects designated within the same
opposition. Historically, the MPC referred to these as "double designations". An example
involves the double designation/identification made between 2017 SL83 and 2017 UH33.

As of June 1, 2020, the MPC will cease to use the "double designation" terminology and
will simply refer to them as identifications.


## Summary of Linkages

Every year, the MPC creates a summary report of all the identifications that have been
submitted, accepted by our pipeline and then published.

- [2021 Summary](https://minorplanetcenter.net/mpcops/documentation/identifications/stats/2021/)
- [2022 Summary](https://minorplanetcenter.net/mpcops/documentation/identifications/stats/2022/)
- [2023 Summary](https://minorplanetcenter.net/mpcops/documentation/identifications/stats/2023/)
- [2024 Summary](https://minorplanetcenter.net/mpcops/documentation/identifications/stats/2024/)
- [2025 Summary](https://minorplanetcenter.net/mpcops/documentation/identifications/stats/2025/)


## The Isolated Tracklet File (ITF)

The Isolated Tracklet File (ITF) containing Isolated Tracklets can be downloaded
[from here](https://minorplanetcenter.net/iau/ITF/itf.txt.gz). Please ensure you have
read the [acceptance criteria documentation](acceptance-criteria.md).
