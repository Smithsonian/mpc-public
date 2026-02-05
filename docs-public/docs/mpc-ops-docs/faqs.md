# Frequently Asked Questions

Common questions and answers about MPC operations and services.

## Submitting and Tracking Observations

??? question "How do I submit observations?"
    There are submission instructions [here](https://www.minorplanetcenter.net/iau/info/TechInfo.html).

    After you submit your observations, you can confirm they were received using [WAMO](https://minorplanetcenter.net/wamo/wamo.html) (Where Are My Observations).

??? question "Have my observations been processed/published? Where are they?"
    Try [WAMO](https://minorplanetcenter.net/wamo/wamo.html) (Where Are My Observations).

    A description of WAMO results is available [here](https://minorplanetcenter.net/wamo/help.html).

    If nothing is returned, your observations may have been rejected due to formatting issues.

??? question "Why were my observations rejected?"
    The most likely reason is large orbital fit residuals, including orbital fit residuals larger than your reported uncertainty.

    You can see whether this is the case by using an orbit fitter for the archival astrometry plus your submitted astrometry. If you find that the residuals are good, you can submit a ticket under 'General Support'.

## Observatory Codes and Object Identification

??? question "How do I get an observatory code?"
    The typical procedure for obtaining an observatory code is explained in the links below:

    - [How to begin](https://www.minorplanetcenter.net/iau/info/Astrometry.html#begin)
    - [Get an observatory code](https://www.minorplanetcenter.net/iau/info/Astrometry.html#HowObsCode)

??? question "What is this moving object in my image?"
    If you are interested in identifying a moving object, you can supply the RA, Dec, and Time information to [MPChecker](https://www.minorplanetcenter.net/cgi-bin/checkmp.cgi). This service will return a list of minor planets near that location at a given time.

    If you do not see a good match on that list, the object is most likely an artificial satellite. The MPC does not track artificial satellites, but you can try [online artificial satellite identification](https://www.projectpluto.com/sat_id2.htm).

    If you are convinced that the object is unknown, you can follow the procedure to [get an observatory code](https://minorplanetcenter.net//iau/info/Astrometry.html#HowObsCode), accurately determine the position of the object and time of observation, and [submit the astrometry to the MPC](https://minorplanetcenter.net/iau/info/TechInfo.html). As the MPC processes over 50 million observations per year, we are unable to measure images and only accept astrometry in obs80 or ADES format (see the above link).

## Naming and Discovery Credit

??? question "I have a question related to naming/citations."
    Naming is handled by IAU Working Group on Small Body Nomenclature at [contact@wgsbn-iau.org](mailto:contact@wgsbn-iau.org).

    They handle all matters related to the naming (and associated citation) for all minor planets and comets. You can also visit their [website](https://www.wgsbn-iau.org).

??? question "I discovered an object, but you have assigned the wrong discovery credit. Can you fix it?"
    Sorry! Please submit a ticket under 'General Support'.

## MPC Services and Subscriptions

??? question "How do I get removed from the MPEC mailing list?"
    Please use the following link to automatically update your email on the MPEC mailing list: [Subscription to Minor Planet Center Notification Services](https://mpc-service.atlassian.net/servicedesk/customer/portal/18).

??? question "How do I subscribe to receive the replicated MPC database?"
    Please contact Andrei Mamoutkine of the Small Bodies Node (SBN) at [amamoutk@umd.edu](mailto:amamoutk@umd.edu).

??? question "A file or website I am trying to use is corrupted/unavailable/has other problems. Can you fix it?"
    Please submit a ticket under 'General Help - Problem with Services'. Please provide the complete URL, and, if the issue relates to a file, attach the file as well.

??? question "I can't access your website anymore. Did you ban my IP Address?"
    If you submit too many requests to the MPC in a short time, your IP Address might have been blocked.

    Please change your process to limit queries to not more than 1 API request per 2 seconds, and submit a [helpdesk ticket](https://mpc-service.atlassian.net/servicedesk/customer/portal/) requesting we unblock your IP address.

## Helpdesk and Support

??? question "My ticket was 'Moved to Development'. What does that mean?"
    Some of the helpdesk tickets submitted to the MPC cannot be resolved immediately. This can include requests for new features or services, the re-implementation of services or files that are no longer produced, or other work that requires effort beyond typical day-to-day operations of the MPC. We do not have resources available to implement all user requests on short timescales. For user requests that we acknowledge would be valuable to implement, we set the ticket status to "Moved to Development".

    When a ticket is "Moved to Development", we create or link a matching task in our software development system. This can be "Low", "Medium", or "High", and the priority of the Helpdesk ticket will match the priority of the related task in our internal Development tracking system. This priority is regularly reviewed by MPC staff. High priority tasks have resources assigned and will be completed or have significant progress made within the next 3 months. Medium priority projects may have progress in the next 3 months, and Low priority projects are unlikely to be started until their priority is changed. Typically, staff only update the tickets when the development work is complete, unless the user asks additional questions.

    To view your ticket's priority, log in to the [MPC Helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portal/). On the upper right, click 'Requests' and select one of the options. This will show a table of all relevant tickets, with the priorities listed on the right-hand side. If the ticket(s) you are looking for are unavailable, you may need to add additional options in the 'Status' selection, which typically defaults to 'Open Tickets'. Add 'Moved to Development' to include these as well.

## Publications and Citations

??? question "How do I credit the MPC in my publication?"
    Data from the MPC's database is made freely available to the public. Funding for this data and the MPC's operations comes from a NASA PDCO grant (80NSSC22M0024), administered via a University of Maryland - SAO subaward (106075-Z6415201). The MPC's computing equipment is funded in part by the above award, and in part by funding from the Tamkin Foundation.
