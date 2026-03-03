# Getting Started with Astrometry

This page covers the basics of equipment, measurement techniques, comparison star catalogues, corrections, timing and what objects to observe.


## What equipment do I need?

Almost any type of telescope will do (reflector or refractor). You will need to know the focal length of your telescope and the physical size of your CCD's pixels to calculate the pixel scale. Your setup should be such that the pixel scale is no greater than 2"/pixel (preferably) or 3"/pixel (at worst). In practice, your optimal pixel scale is something that you will have to determine for yourself, taking into consideration the capabilities of your telescope and CCD and the seeing at your site. If your pixel scale is much larger than the values quoted above, then the quality of the astrometry will suffer. If your pixel scale is too low for your local setup, then the signal-to-noise of the images may be low as each image is spread over a large number of pixels.

You will also need a computer to capture the images and software to perform the reductions. Various software packages are available to process the images. We suggest you consult the [Minor Planet Mailing List](https://groups.io/g/mpml/) for information about the latest popular software.

An accurate clock/watch set to Coordinated Universal Time (UTC) is a must and this must be checked regularly (as a minimum, at the start of each observing session) against a reliable standard.

Access to e-mail is also important, both for reporting observations to and receiving designations from the [Minor Planet Center (MPC)](https://minorplanetcenter.net/iau/mpc.html). <!-- TODO: update link when migrated -->


## What sort of CCD should I use?

It is not our place to recommend specific brands of CCDs. A look through any popular astronomy magazine shows that there are a variety of CCDs available. The CCD that is right for you depends on your computer system and on how much you want to spend. CMOS sensors are also now available and their performances seem to be very good especially for fast moving objects.


## How do I make measurements?

The exact details of how you will make measurements on your images and perform the reductions will depend on the software package you are using. In broad terms, you will determine pixel x,y for the centers of a number of comparison stars of known position (at least three comparison stars, preferably as many as are on the image) and the minor bodies in each image. Using these x,y measurements (determined to a fraction of a pixel) and the comparison star coordinates (taken from a suitable reference catalogue), the program should then do a least-squares plate-constants (LSPC) solution to derive the unknown coordinates of the minor bodies. Be suspicious of any package that does not do a proper LSPC solution!

You must not attempt to derive positions by overlaying charts on your images or by estimating positions by eye. The accuracy of these positions will not be sufficient.

The MPC also encourages submitters, especially those searching through archival astrometry, to carefully examine any marginal detections. Astrometry should be reported only for detections with a sufficiently high signal-to-noise ratio to withstand external independent review of the images. We note that synthetic tracking software, such as Tycho Tracker, often requires significant experience to avoid submitting stacked noise in sky location of the expected position of an object.


## Where should I obtain my comparison star coordinates?

Most CCD fields tend to be rather small (a few tens of arcminutes wide) and this has in the past precluded the use of traditional standard astrometric catalogues. Fortunately, the situation is now much improved and most astrometric software allows suitable catalogues to be queried over the network (e.g., from sources such as Vizier) or from a local copy.

It is the recommendation of the Minor Planet Center that observers should migrate to using the [Gaia](https://www.esa.int/Science_Exploration/Space_Science/Gaia_overview) catalogues (DR2, DR3 and future ones). Other acceptable catalogues include UCAC4 and UCAC5.

The following sources MUST NOT be used for comparison-star coordinates:

- The World Coordinate System information in the FITS headers for images in the Digital Sky Survey (whether accessed via the Web or via the highly-compressed CD-ROM version).
- Any B1950.0 star catalogue (e.g., SAO Catalogue).


## What corrections should I apply to the derived positions?

None!

No corrections should be made by the observer for parallax and no attempt should be made to correct the UTC times of observation to Terrestrial Time (TT), the uniform timescale used in orbit computations.


## How do I obtain an accurate time?

Getting an accurate time when measuring astronomical images is extremely important (see [the paper by Farnocchia et al (2022)](https://iopscience.iop.org/article/10.3847/PSJ/ac7224/meta) containing the results of the first [IAWN](https://iawn.net/) campaign).

Note that the determination of an accurate time for an observation depends not only on having access to a reliable standard, but also by understanding the delays in the observing system.

- The first step consists in obtaining the current UTC from the [U.S. Naval Observatory's Time Service Department](https://aa.usno.navy.mil/faq/UT).
- Then we suggest observers to regularly check their estimated observation times against GPS satellites. For more information about how to do it, please see the page ['Calibrating timing of astronomical images using navigation satellites'](https://www.projectpluto.com/gps_expl.htm) on the [Project Pluto website](https://www.projectpluto.com/).


## What objects should I be observing?

Those observers who wish some guidance on what objects to observe are advised to check out the MPC [NEA Planning Aid](https://minorplanetcenter.net/cgi-bin/neaobs.cgi), [Observer Target List](https://minorplanetcenter.net/whatsup) or [Observable-Object List Customizer](https://minorplanetcenter.net/iau/lists/Customize.html).

Other services are also available, such as [NEOfixer](https://neofixer.arizona.edu/) or the [Priority List from ESA](https://neo.ssa.esa.int/priority-list).

Some observers have set up their own web pages, generally to encourage follow-up of their own discoveries. We have [collected together](https://minorplanetcenter.net/iau/MPEph/FollowUp.html) some of these sites, but if you wish to be added to the list, please let us know through [Jira](https://mpc-service.atlassian.net/servicedesk/customer/portals).

Ephemerides for minor planets can be generated using the [Minor Planet Ephemeris Service](https://minorplanetcenter.net/iau/MPEph/MPEph.html).
