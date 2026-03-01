# Reporting Observations

This page covers how to format and submit observations to the MPC, including format requirements, quality standards and common mistakes to avoid.


## How do I begin reporting?

Please follow these rules:

- If your site does not have an observatory code, [ask for it!](observatory-codes.md#how-do-i-get-an-observatory-code)
- If possible, report at least three observations of each object from each night: do not report single positions per night. As a general rule, batches that contain single positions will be returned in their entirety to the submitter.
- You should not start by observing fast-moving objects. It is important that you gain experience by observing "routine" objects before attempting to observe "unusual" objects. We also expect you to prove that you can produce good astrometry of known objects before you begin to discover new objects.
- In general, comets are harder to measure than minor planets. If we have a new observer reporting comet observations of bad or indifferent quality we do not know if it is simply a problem due to the comet (big, bright difficult-to-measure image) or a problem with the measurement/reduction process.
- The MPC encourages submitters, especially those searching through archival astrometry, to carefully examine any marginal detections. Astrometry should be reported only for detections with a sufficiently high signal-to-noise ratio to withstand external independent review of the images. We note that synthetic tracking software, such as Tycho Tracker, often requires significant experience to avoid submitting stacked noise in sky location of the expected position of an object.
- Reporting magnitudes is optional, but highly desirable. Please try to report magnitudes if you are submitting archival astrometry.
- MPC encourages observers to use the correct keywords in the observational header, particularly when it comes to rapid processing of NEOs or comets. Without the correct keyword, tracklets could end up in a wrong or slower queue. In addition, please submit new NEOs separately from NEOCP followup and/or incidental astrometry. Lastly, please follow the instructions on how to format other elements of the header. Issues such as omitting space between initial and last name slows down the process of the submitted astrometry since the automated program code assignment will not be possible (follow the instructions reported on the [how to specify observational details page](https://www.minorplanetcenter.net/iau/info/ObsDetails.html)). <!-- TODO: update link when migrated -->

In particular:

- Batches containing observations of new NEO candidates must have "NEO CANDIDATE" in the subject line.
- Batches containing observations of objects already on the NEOCP must have "NEOCP" in the subject line.
- Batches containing observations of new comet candidates must have "NEW COMET" in the subject line.
- Batches containing observations of new TNO candidates must have "NEW TNO" in the subject line.

See also [How do I report my astrometry?](#how-do-i-report-my-astrometry) and [What quality of measurements should I aim to produce?](#what-quality-of-measurements-should-i-aim-to-produce).


## How do I report my astrometry?

Astrometric observations can be reported in two different formats:

- The longstanding 80-character MPC1992 format (also informally called obs80).
- The more recent [IAU Astrometric Data Exchange Standard (ADES)](#whats-the-ades-format).

Observations reported in the MPC1992 format need to follow the rules detailed on the [page describing the format](https://minorplanetcenter.net/iau/info/ObsFormat.html). Please read this document carefully and report the observations in the correct format. <!-- TODO: update link when migrated -->

Observations reported in ADES format need to follow the rules described in the [ADES documentation](https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf) and on the [MPC ADES Data Submission page](https://minorplanetcenter.net/iau/info/ADES.html). <!-- TODO: update link when migrated -->

Observations of minor planets, comets and natural satellites, formatted as specified above, can be reported via:

1. E-mail to [obs@cfa.harvard.edu](mailto:obs@cfa.harvard.edu) (MPC1992 only)
2. Observation Submission Forms (ADES only):
    - [ADES XML Submission Form](https://minorplanetcenter.net/submit_xml)
    - [ADES PSV Submission Form](https://minorplanetcenter.net/submit_psv)
3. [MPC1992 cURL instructions](https://minorplanetcenter.net/iau/info/commandlinesubmissions.html) <!-- TODO: update link when migrated -->

In addition to the above points, please also check the following notes:

- Do not report more than one position for each time of observation. Observations of objects that contain multiple positions for a single time of observation will be returned to the submitter for correction.
- When there is no trailing of the minor planet image (or you are measuring the middle of a trail) the time of observation is the mid-exposure time. If you are measuring both ends of a trail, then one end is associated with the start of the exposure, the other with the end. Alternatively, if the trail is very short, you can simply report the mid-point. However, you must not report both a trail-end and mid-point measures from the same trail.
- Note that reported magnitudes must be derived from the individual frames: do not obtain a magnitude from one frame and then copy it on all the other observations. Also, ensure that you report the magnitudes with the astrometry: do not say "Photometry to follow".
- Always report positions for every moving object in your images. Do not assume that just because an object is numbered that continuing observations are not important. The inclusion of well-known objects, particularly when there are also observations of unidentified objects, serves as a useful check of the quality of your measurements.


## What's the ADES format?

The Astrometric Data Exchange Standard (ADES) format was adopted by the IAU in August 2015. It was introduced with the goal of standardizing the exchange and the storage of astrometric data (observations and uncertainties) and their associated data description between observers and orbit computing centers. The MPC accepts and internally uses observations in this format.

Details are available on the [ADES GitHub repository](https://github.com/IAU-ADES/ADES-Master) and on the [MPC ADES webpage](https://minorplanetcenter.net/iau/info/ADES.html). <!-- TODO: update link when migrated -->

The use of the ADES format is not mandatory at the moment, but the MPC strongly encourages users to familiarize themselves with the format and the repository.


## How many observations should I make of each object?

As a general rule, when pursuing high precision astrometry, it is preferable to obtain small quantities of deep, high SNR data.

- The MPC typically recommends taking a few observations over a period of an hour or so per object, per night. Additional astrometric positions are typically not helpful for the determination of the orbit.
- Observations of specific objects are best made on pairs of nearby nights as the accuracy of isolated single-night observations can be difficult to judge. By observing on pairs of nights any ambiguity is removed.
- Please try to not make only one observation of each object per night. Without specific appropriate reasons, if a batch contains any single positions, the entire batch will not be accepted and it will be returned to the sender.
- Observations of a potentially new object in groups many hours apart on a single night _can_ be useful in particular in the case of a newly-discovered object that may be close to the Earth.

However, we recognize that there might be cases in which more observations are needed, e.g. for photometric purposes, or for an object during a close encounter with the Earth. Even though the MPC always encourages the acquisition of high quality astrometry, we emphasize that it is not our place to discard large numbers of observations when they get sent to us. There will be cases in which objects are going to have hundreds of published astrometric and photometric measurements. While the MPC already de-weights these measurements for our orbit fits, it is up to the end user to decide what they want to do with them.


## What quality of measurements should I aim to produce?

Astrometry is a field where bad measures are generally of little or no use. It is important that observers can consistently produce observations with a consistency of <1" for observations using the same comparison stars, and a night-to-night consistency limited only by the comparison star catalogue.

A few additional notes:

- Please check if you have any timing errors before submitting observations (see [How do I obtain an accurate time?](getting-started.md#how-do-i-obtain-an-accurate-time)).
- Please note that if you are using the [ADES](#whats-the-ades-format) format, you are also able to report your astrometric uncertainties. Be sure you have read how to compute and submit your uncertainties in the [ADES documentation](https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf).


## Can I report approximate or preliminary measures?

No.

Approximate measurements will be ignored. Only report final astrometry.

Don't report preliminary measures and then improve them. It is very time-consuming to replace preliminary measures.


## Do I need to identify objects?

You do not need to identify objects, but we suggest you do it if you can. All the observations will be validated anyway through orbit fitting.

If you do not identify the object, the MPC checking procedures will first check if the object can be linked to any known solar system objects before processing it.

However, every reported observation must have a designation. If you don't know the designation of a particular object, or are not bothering to identify objects, use an observer-assigned temporary designation. Observer-assigned temporary designations should be unique--don't call everything `X`!

Observer-assigned temporary designations should be seven characters or less long, and begin in column 6 of the observational record. The designations must not be of the form of the packed (e.g. K23A00B, 00001, ~0023) or unpacked designations (e.g. 2023AB, 1, 620127) used by the MPC. Also:

- Observations of NEOCP objects must always be tagged with their NEOCP designations, as well as the initial observations made in support of an observatory code request.
- Observations reported for the first time when asking for a new observatory code need to include the provisional designation or the number that identifies the object.
- Observations of the same object on different nights must be given the same temporary designation only if they are reported in the same message and you are absolutely positive that all the nights refer to the same object. Correspondences of observer-assigned temporary and MPC-assigned provisional designations will be reported back to the observer via e-mail (see also [How do I understand the designations the MPC sends me?](mpc-processing.md#how-do-i-understand-the-designations-the-mpc-sends-me)).
- Do not continue to use your observer-assigned designations once official provisional or permanent designations have been assigned.


## Should I separate comet and minor-planet observations?

The assignment of different types of objects to various queues for processing is automatic and based on the orbit corresponding to the designation assigned to each observation. Observations of different types of objects may now be freely mixed.


## Batches with multiple observatory codes

If you want to submit observations from two or more observatory codes in the same message, you must group each site's observations under an observational header appropriate for the site. A representation of an example follows:

```
COD 608
OBS ...
MEA ...
... Rest of header ...
Observations from code 608
COD 644
OBS ...
MEA ...
... Rest of header ...
Observations from code 644
```

Failure to format the message as shown above will result in the batch being rejected by the automated routines. Note that later headers do not inherit anything from earlier headers. So you must include, at a minimum, OBS/MEA/TEL/NET lines on later headers.

Note that this scheme must be followed if there are two (or more) headers from the same observatory code in the same message.


## E-mail recommendations

If you can, please use the [cURL submission method](https://minorplanetcenter.net/iau/info/commandlinesubmissions.html) to submit the observations. If you submit ADES observations, the cURL method and website submission forms are also the only methods allowed; you cannot submit ADES by email. <!-- TODO: update link when migrated -->

In case you are submitting observations in the MPC1992 format and you want to use e-mail, the following guidelines should be noted with regard to any e-mail submission of observations:

- Observations must be reported as plain ASCII files. Do not send, e.g., UUENCODE'd or BINHEX'ed files. This is important if you are using e-mail attachments.
- Please ensure that your mailer does not split the 80-column observation records--many mailers, such as PINE, will automatically break a line at about 72 characters. In PINE you can avoid this problem if the observations you wish to send are in a separate file by including the file using CTRL-R, rather than by using cut and paste.
- If you are using a mailer that can send HTML mail, please disable the inclusion of the HTML version. Inclusion of the HTML version more than doubles the length of the e-mail and the repetition of material is completely useless. In addition, the inclusion of HTML text may trigger the MPC's antispam e-mail filters, causing your message to be flagged as spam.
- Never send any kind of word-processor/DTP file. If you use a word processor or DTP package to prepare your observations, ensure that you use the package's 'Save as ASCII' option.

If you cannot send unencoded attachments and the batches are not more than a few KB in size, you can use the [Observation Submission Form](https://minorplanetcenter.net/cgi-bin/feedback_submit_obs.cgi?S=Observation%20submission%20via%20website&D=O).

Or you can use the [cURL submission method](https://minorplanetcenter.net/iau/info/commandlinesubmissions.html) to submit batches of any size. <!-- TODO: update link when migrated -->


## Spam-blocking systems

If you use any sort of spam-blocking system to sift your incoming e-mail, you are warned that it is your responsibility to ensure that e-mail from the MPC is passed unimpeded. The list of e-mail addresses that must be allowed through are autoack/mpc/autodes/des/(initial.surname) at cfa.harvard.edu. If e-mail from any of these addresses is blocked, you may not get ACKs or designation files. Bounced messages will not be resent.

Note that "Allowed Sender" systems will not work with our automated routines that send out information as e-mail returned to certain addresses will bounce.


## How do I know the MPC received my observations?

Upon receipt of a batch of observations, we send an automatic acknowledgement back to you. E-mail is not perfect and messages do sometimes get lost.

If you have not received any acknowledgement from us or if you want to know what happened to your observations, please use our [WAMO service](https://minorplanetcenter.net/wamo/).

Please also check that you have correctly used all the fields in the header. See [Information on how to personalize the acknowledgement](https://minorplanetcenter.net/iau/info/ObsDetails.html). <!-- TODO: update link when migrated -->

If something is not clear or you still have questions about your observations, please submit a [Jira ticket](https://mpc-service.atlassian.net/servicedesk/customer/portals).

Note that the acknowledgement is automatic and simply informs you that we have received your message. It says nothing about the formatting of the observations contained therein or their quality.


## A message bounced. Do I need to resend it?

It depends on the source of the bounceback message. obs@cfa.harvard.edu is an e-mail alias (google-group) that forwards incoming messages to various different internal email accounts.

You should only resend your message if the bounceback indicates that obs@cfa is the source of the failure.

You do not need to resend your message if the bounceback comes from any other e-mail address.


## What is the purpose of the contact details?

The contact details as published in the [_MPCs_](https://minorplanetcenter.net/iau/services/MPCServices.html) for each observatory code are intended as a contact point for persons with queries regarding a specific program. The contact address does not have to be the street address of the observatory. For professional programs it should be noted that the contact details are NOT intended to be a list of P.I.s on the project. <!-- TODO: update link when migrated -->

The contact details MUST include:

- the name of a person connected with the program (who is willing to answer queries about the presented observations)
- a snail-mail address for that person (this can be a P.O. Box)
- an e-mail address for that person

[Information on how to specify the contact address](https://minorplanetcenter.net/iau/info/ObsDetails.html) (as well as names of observers and measurers) is available. <!-- TODO: update link when migrated -->


## What are some common mistakes?

1. **Incorrectly-Identified Objects.**

    If you try to identify objects, ensure that the identifications are correct and that you used the packed forms of the designations in the appropriate columns of the observational records. If in doubt, use temporary designations.

2. **Incorrect Times of Observations.**

    Ensure that the mid-points of your exposures are timed and reported correctly! The most common error by observers (and one of the trickiest to correct if the observation has already been published) is incorrect observation times (or occasionally even _dates_).

3. **Non-ASCII Submissions.**

    Ensure that you send only plain ASCII e-mails. Encoded attachments will be ignored by the automated processing routines.

4. **Incorrectly-Specified Observer Details.**

    If you do not include an [observational header](https://minorplanetcenter.net/iau/info/ObsDetails.html) before the observations, the e-mail message will not be recognized as containing observations. <!-- TODO: update link when migrated -->

    Some observers specify observer details in the form used in the _MPCs_. These details are usually nicely formatted, but the observation processing routines will ignore them. Observer details must be formatted in [the proper format](https://minorplanetcenter.net/iau/info/ObsDetails.html). <!-- TODO: update link when migrated -->


## Should I check my observations before reporting them?

Observer checking does not need to be anything more than checking that what you actually send is what you meant to send. Checking of designations, observation dates and times, positions and the [format](https://minorplanetcenter.net/iau/info/ObsFormat.html) is advisable. <!-- TODO: update link when migrated -->
