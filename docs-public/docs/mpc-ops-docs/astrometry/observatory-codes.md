# Observatory Codes

This page covers obtaining, using and updating observatory codes for astrometric observations.


## How do I get an observatory code?

Observatory codes are intended for "permanent" (repeated usage) observing sites. It is not necessary that your telescope is associated with any existing building in order to apply for an observatory code; setting up your portable telescope in your backyard is permanent enough to obtain an observatory code from the MPC. We encourage all observers to apply for an observatory code. The ["Roving Observers"](https://minorplanetcenter.net/iau/info/RovingObs.html) format should only be used in very specific cases by observers at temporary sites, preferably only by people with prior experience submitting measurements to the MPC. We always encourage observers to apply for an observatory code and not to use the Roving Observers format. <!-- TODO: update link when migrated -->

When you apply for an observatory code, you must complete the following tasks, preferably on the same day, in this order:

1. Submit a single submission with astrometric measurements meeting the requirements listed below.
2. Complete and submit the [new Observatory Code Request Form](https://minorplanetcenter.net/new_obscode_request).

Your observatory code request will not be processed until **both** the request form and qualifying measurements are received. Please submit your request and the necessary astrometric measurements close in time; do not submit one if you are not ready to submit the other.

**Your astrometry measurements must meet the following requirements**:

- You need to submit measurements of at least **ten numbered Near-Earth Asteroids**; the [Observing Target List](https://minorplanetcenter.net/whatsup/index) can be used to identify NEAs visible from your location.
- You **must not** include measurements of comets, natural satellites or objects that have yet to be numbered.
- Every object included must be **fainter than 16th magnitude**.
- Every object must be observed on **two distinct nights**, preferably less than a week apart. If weather interferes, the two nights can be some weeks apart. However, do not submit partial astrometry (or your request form) until you have obtained everything you need; submit everything at the same time. Note: The ten objects do not need to all be measured on the same two nights.
- Three to five observations of each object from each night should be included. **Do not report single positions per night**; single positions will cause your entire submission to be rejected. Reporting more than five measurements in a single night is generally not useful for constraining an orbit.
- At least one measurement of each object in each night **must include a photometric measurement** of the object's brightness, i.e. the apparent magnitude.
- **Use observatory code XXX** in the observation header and measurement lines when submitting measurements towards an observatory code request. Do **not** use any other code, as doing so may cause your submission to be processed incorrectly or be rejected. The observatory code XXX is specifically for measurements supporting an observatory code request; please do not use XXX once you have been assigned a real observatory code.
- The header of your submission must include a comment line with content formatted like this example:

        Long. 123 45 67.8 E, Lat. 12 34 56.7 N, Alt. 123m, Google Earth

    Where the longitude, latitude, altitude and source should be the same values as you provide in the observatory code request form.

- Measurements **must** be submitted in either ADES PSV or ADES XML. The older MPC1992 format is obsolete and must not be used for new observatory codes. Please follow the instructions documented on the [ADES Data Submission page](https://www.minorplanetcenter.net/mpcops/documentation/ades/) for details on how to prepare and submit your measurements in ADES format.

!!! note
    If your astrometry submission has severe problems (such as formatting errors, duplicate lines, single positions within a night, missing mandatory header fields, etc.) the entire submission gets automatically rejected and you may not get an e-mail about it. If you did not receive an acknowledgement email and you cannot find your measurements using the [Where Are My Observations (WAMO)](https://minorplanetcenter.net/wamo/) service, then your submission must have failed. In such case, please review your submission file to identify the problems, review [the submission instructions](reporting-observations.md#how-do-i-report-my-astrometry) and try again. If you cannot identify the problem, you can ask for assistance in the helpdesk ticket tied to your observatory code request; simply reply to the email that you received when you submitted the observatory code request form (it will be from "General Support" and will have "MPCHLP" in the subject line).

**The new observatory code request form requires you to provide the following information**:

- A contact name.
- A contact email address. It is important that you **use the same email address for both the request form and the astrometry submission**, so that they are automatically linked. Using different emails will result in longer processing times.
- A **submission ID** for your submission of the qualifying measurements. This means that you **must** submit measurements before you can submit the form, and that you **must** have received an acknowledgement e-mail of the submission (which will contain the submission ID).
- An observatory name. Optional, but if not given, the city/town name will be used. _The observatory name must not contain the name of a living person_.
- The observatory site. Name of nearest city, village, neighborhood, mountain, forest, etc.
- The country the observatory is located in.
- Latitude, in **degrees, arc-minutes and arc-seconds (including one or two decimals)** (_not decimal degrees_) N or S of the equator, in the WGS-84 system, e.g. _42 22 53.31 N_ or _42&deg;22'53.31"N_.
- Longitude, in **degrees, arc-minutes and arc-seconds (including one or two decimals)** (_not decimal degrees_) E or W of the Greenwich meridian, in the WGS-84 system. **Do not use negative longitudes**. Give a longitude as either:
    - a specific number of degrees, arc-minutes and arc-seconds E or W (being sure to state which direction) of the Greenwich meridian, e.g. _71 07 42.15 W_ or _71&deg;07'42.15"W_;
    - a specific number of degrees, arc-minutes and arc-seconds E of Greenwich (according to the IAU convention). If a site is just west of the Greenwich meridian, give the longitude as a quantity near 360&deg;, not as a negative quantity, e.g. _288 52 17.85 E_ or _288&deg;52'17.85"E_.
- The latitude and longitude must be given with a precision better than one arc-second, i.e. the arc-second values must have a decimal. **Do not report coordinates with integer arc-seconds**; that corresponds to a precision of several tens of meters on the surface, which is insufficient. Here are 3 possible ways (others exist) to obtain precise coordinates:
    - [Google Maps](https://www.google.com/maps/): find your observatory, and right click on it. Click on the decimal degrees numbers (usually at the top of the menu), paste that into the search bar and hit return. Google Maps now converts that to the desired degrees, arc-min, arc-sec format, with one decimal on the arc-seconds. Simply copy the reformatted value from the search bar.
    - [Google Earth](https://www.google.com/earth/about/versions/): find your observatory on the map, and right click on it. Click "Copy coordinates", and paste them into the search bar; unfortunately, this gives coordinates of insufficient precision (no decimal on the arc-seconds). Manually add decimal values (.1, .2, etc.) and click return, and repeat using trial and error until the search pin lands exactly on top of your observatory.
    - GPS unit/app: Record several measurements, preferably over the course of several days, and take the average value. If possible, hold the GPS unit as close as possible to the location where the telescope's two axes intersect.
- Altitude, which must be measured in **meters above mean sea-level** (unless measured with a GPS). Google Earth gives altitudes relative to mean sea level. GPS units vary, but typically have an option to display altitude above mean sea-level (if not, see below).
- The height of the telescope above ground (or wherever else 'altitude' is measured), in meters to the nearest whole meter. Leave this as 0 if the altitude provided corresponds to the height of the telescope, otherwise fill this value with the difference between the location where the telescope's two axes intersect and the location the 'altitude' refers to (typically ground level).
- The source for the specified coordinates and altitude (e.g., Google Earth, GPS, named map, etc.). If you measured your altitude using a GPS (or GPS app), you must select "GPS" and the correct option from the "Reference frame for altitude" drop-down box, where "EGM-96" corresponds to an altitude above mean sea-level and "WGS-84" corresponds to an altitude above the reference ellipsoid.

When you submit your observatory request form, you will receive two emails:

- one from "new\_obscode\_request" with subject line "New obscode request by Your Name"; this simply contains a copy of the information that you entered in the form. **Do not reply to this email.**
- one from "General Support" with subject line "MPCHLP-???? New obscode request by Your Name" (where ???? is a number). **Do not delete this email** and **make sure it is not in your spam folder**. This email thread is tied to your observatory code request. If we need to contact you about your request, we will reply to this email thread. Once your observatory code is assigned, we will let you know through this email thread. If you want to contact us about your request, you can reply to this email thread as well, simply reply above the dashed line and without altering the subject line.

A few additional notes:

- The longitude and latitude must be specified to a precision of 0.1 arcsecond or better. A useful tool for determining your site's coordinates is [Google Earth](http://earth.google.com). Note that we now use Google Earth to verify the given coordinates. If we have a query as to the location, we may ask for clarification/confirmation.
- If you do not use Google Earth, it is important to note that the longitude and latitude that you supply must be geographic coordinates, not geocentric coordinates.
- An observatory code will typically not be assigned if your astrometry shows large post-fit residuals (in coordinates, time or magnitude) or in other ways indicate poor quality. Such observations will be rejected and new, better, measurements will have to be provided in order to obtain an observatory code.
- The assignment of new codes is done manually in batches, usually once per week. If more than two weeks have passed since your submission, please contact us by replying to the "MPCHLP" email that you received when you submitted your request form.
- If you fail to supply sufficient measurements in your initial submission, fail to supply all required information, or your initial measurements are not of sufficient quality, an observatory code will not be assigned and we may contact you for additional information/measurements. We will only contact you if you have submitted the observatory code request form; we will not contact you if you have only submitted measurements.
- Even if you are only interested in comets, it is required that you follow these guidelines and not submit comet astrometry until you have successfully obtained an observatory code.
- For new observatory code requests with coordinates very close to an existing code, we may ask for additional information, or we may require additional evidence that separate observatory codes are necessary (we may, for example, request that you submit additional NEO measurements).

If any of the previous conditions are not met, the obscode will not be assigned.

If something is not clear or you don't know why your data have been rejected, please open a [Helpdesk ticket](https://mpc-service.atlassian.net/servicedesk/customer/portal/13/group/39/create/260) (or reply to the existing one tied to your observatory code request, subject line includes "MPCHLP") before trying to send more data to us.


## Does my observatory code move with me?

**No**, your observatory code does not move with you. Observatory codes are tied to a specific **location** relative to the center of the Earth (exceptions apply to "Roving Observer" and artificial satellite codes). If you move your observatory to a new site, you have to apply for a new code. If you go and observe at a friend's observatory, you must use their observatory code (applying for one if necessary) rather than using your own.


## Do closely spaced telescopes need separate observatory codes?

**Maybe**. It depends on the distance, the resolution of your telescope and what type of objects you observe. Telescopes using the same observatory code should never be more than 100 meters apart. However, if you intend to ever observe objects on [the Near-Earth Object confirmation page (NEOCP)](https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html), or intend to observe GPS satellites to calibrate your system clock, or for other reasons hope to observe objects very close to the Earth, closely spaced telescopes are more likely to require separate observatory codes. Telescopes can typically use the same obscode if they are less than X meters apart, where:

X [meters] = Y / D [meters]

where D is the diameter of the largest telescope, in meters, and Y varies as follows:

- Use Y=6 if you intend to observe GPS satellites in order to calibrate your system clock and know the time of your measurements to the best possible accuracy.
- Use Y=6 as well if your setup is able to routinely observe high-priority NEOCP objects, including potential impactors, **within hours** of the object being posted to the NEOCP.
- Use Y=15 if you will only occasionally observe NEOCP objects.
- Use Y=30 if you are not interested in observing NEOs and will primarily observe distant objects like Centaurs and Trans-Neptunian Objects.

Telescopes smaller than 50 cm (0.5 m) in diameter thus typically do not need separate observatory codes if they are all within 30 meters of each other, due to the limitations of their resolution. Telescope hosting facilities (where many privately owned small telescopes are hosted mere meters apart) can therefore consider applying for a single observatory code that all users of the facility can use; such a shared code should use a coordinate close to the center of the cluster of telescopes.

For new observatory code requests very close to an existing code, we may ask for additional information, or we may require additional evidence that separate observatory codes are necessary (we may, for example, request that you submit additional NEO measurements).


## How do I update my observatory code information?

If the information relating to an observatory code needs to be updated/corrected, simply raise a [Helpdesk ticket](https://mpc-service.atlassian.net/servicedesk/customer/portal/13/group/39/create/260) about it. Please note that if your observatory has been moved to a different site, you **cannot** simply change the associated coordinates to the new location; you must apply for a new observatory code for the new site. However, many obscodes were assigned based on low-precision coordinates; many have recently been found to be wrong by tens or even a hundred meters. If you have measured, either using Google Earth or a GPS, the location of your observatory more accurately and precisely than the coordinates the MPC currently use, we highly encourage you to contact us with such updates. Additionally, if you wish to change the name of your observatory, or change the contact person/email address, this can also be changed by opening a Jira ticket.

When reporting a change/update, please use the following format, to make our lives easier (a few lines have comments starting with a #; don't include that part):

```
observatory_code: ???  # The observatory code that you want to update
contact_name: New Contact Name
email_adr: new_contact@email.com
observatory_name: New Observatory Name
observatory_site: Updated Site Name
observatory_country: Updated Country Name
website_url: https://newobservatoryname.url
amateur: True/False
observatory_lat: ?? ?? ??.?? N/S
observatory_long: ??? ?? ??.?? E/W
reference: Google Earth/Google Maps/GPS
observatory_alt: 0  # Integer metres altitude of ground level
telescope_height: 0  # Integer metres above ground level
reference: Google Earth/GPS
gps_ref_frame: WGS-84/EGM1996/EGM2006/Mean sea level
```

You only need to report the fields that you think need to be changed. You do not need to guess at values for fields you do not want to change; simply do not include those lines.


## Are there restrictions on observatory names?

Yes and No.

No, in the sense that we cannot dictate what you choose to call your observatory.

Yes, in the sense that we don't have to use your observatory's name in the _MPCs_ if we don't think it is appropriate. Proper names or names of living people should not be chosen as site names. If your observatory's name is longer than 35 characters, please also suggest an abbreviated version, as long names cannot be used in all contexts.

Please be careful when you select your site name.
