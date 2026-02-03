/**
 * @File d2ades.c
 * @author Richard Cloete
 * @Email richard.cloete@cfa.harvard.edu
 * @Description parse an ADES XML file and return a tracklet
 * @Param filepath -- the path to the ADES XML file
 * @Return tracklet -- the tracklet
 */

#include <libxml/tree.h>
#include <libxml/parser.h>
#include <libxml/xpath.h>
#include <stdlib.h>
#include <string.h>
#include "common.h"
#include "digest2.h"
#include "d2ades.h"
#include <time.h>
#include <math.h>

/**
    parse_optical - function to parse the optical elements in an XML document
    @cur: current xmlNodePtr pointing to the root of the optical elements
    This function takes in an xmlNodePtr pointing to the root of the optical elements in an XML
    document and parses it to extract the various fields of the optical data. It then stores these
    fields in an opticalPtr struct and returns it.
    Returns: a pointer to the optical struct containing the parsed data
    **/
static opticalPtr parse_optical(xmlNodePtr cur) {

    /* Allocate the struct */
    opticalPtr ret = (opticalPtr) malloc(sizeof(optical));
    memset(ret, 0, sizeof(optical));

    /* We don't care what the top level element name is */
    /* COMPAT xmlChildrenNode is a macro unifying libxml1 and libxml2 names */
    /* Iterate through child nodes */
    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "provID")))
            ret->trkSub = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "trkSub")))
            ret->trkSub = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "obsID")))
            ret->obsID = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "trkID"))) {
            ret->trkID = xmlNodeGetContent(cur);
            int numToRemove = 3;
            int trkIDLen = strlen(ret->trkID);
            if (trkIDLen > numToRemove) {
                memmove(ret->trkID, ret->trkID + numToRemove,
                        trkIDLen - numToRemove + 1); // +1 to include the null terminator
            }
        }
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "mode")))
            ret->mode = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "stn")))
            ret->stn = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "obsTime")))
            ret->obsTime = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "ra")))
            ret->ra = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "dec")))
            ret->dec = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "rmsRA")))
            ret->rmsRA = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "rmsDec")))
            ret->rmsDec = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "astCat")))
            ret->astCat = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "mag")))
            ret->mag = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "rmsMag")))
            ret->rmsMag = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "band")))
            ret->band = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "logSNR")))
            ret->logSNR = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "seeing")))
            ret->seeing = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "exp")))
            ret->exp = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "subFmt")))
            ret->subFmt = xmlNodeGetContent(cur);

        // SATELLITE
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "sys")))
            ret->sys = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "pos1")))
            ret->pos1 = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "pos2")))
            ret->pos2 = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "pos3")))
            ret->pos3 = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "ref")))
            ret->ref = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "ctr")))
            ret->ctr = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "precTime")))
            ret->precTime = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "precRA")))
            ret->precRA = xmlNodeGetContent(cur);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "precDec")))
            ret->precDec = xmlNodeGetContent(cur);
        cur = cur->next;
    }

    return (ret);
}

/**
 * convert_to_modified_julian_date - Convert a date and time string in ISO format to the modified Julian date
 * @iso_string: A string in the format "YYYY-MM-DDTHH:MM:SS" that represents a date and time in the ISO format
 * Returns the modified Julian date (MJD) as a double. The MJD is calculated by dividing the number of seconds since
 * the Unix epoch by 86400.0 and adding 40587.0
 * The function assumes the input is in the UTC timezone and it will fail if the input string is in different format.
 */
double convert_to_modified_julian_date(const char* iso_string) {
    struct tm tm;
    strptime(iso_string, "%Y-%m-%dT%H:%M:%S", &tm);
    time_t t = timegm(&tm);
    return (double)(t / 86400.0) + 40587.0;
}

/**
* @brief Processes an optical observation and stores the relevant information in an observation struct.
* @param optical A pointer to an opticalPtr struct that holds the optical observation data.
* @param obsp A pointer to an observation struct that will hold the processed observation data.
* @return _Bool indicating whether the processing was successful or not.
*/
_Bool processOptical(opticalPtr optical, observation *obsp) {

    // parse the station code
    int site = parseCod3((char *) optical->stn);
    if (site < 0)
        return 0;

    // parse the date and time and convert to MJD
    const char* datetime = (const char*) optical->obsTime;
    obsp->mjd = convert_to_modified_julian_date(datetime);

    double ra = strtod((char *) optical->ra, NULL);
    ra = ra * M_PI / 180;

    double dec = strtod((char *) optical->dec, NULL);
    dec = dec * M_PI / 180;

    obsp->ra = ra;
    obsp->dec = dec;

    // convert the magnitude to double
    double mag = (optical->mag != NULL) ? strtod((char *) optical->mag, 0) : 0;
    double vmag = 0.0;
    if(optical->band != NULL){
        vmag = updateMagnitude(*optical->band, mag);
    }

    obsp->vmag = vmag;
    obsp->site = site;
    obsp->spacebased = 0;

    // if optical rmsRA or rmsDec are null, just set to 0.
    obsp->rmsRA = (optical->rmsRA != NULL) ? strtod((char *) optical->rmsRA, 0) : 0;
    obsp->rmsDec = (optical->rmsDec != NULL) ? strtod((char *) optical->rmsDec, 0) : 0;

    obsp->rmsRA = obsp->rmsRA  * arcsecrad;
    obsp->rmsDec = obsp->rmsDec * arcsecrad;

    // SATELLITE or ROVING
    if(optical->pos1 != NULL && optical->pos2 != NULL && optical->pos3 != NULL && optical->sys != NULL){

        _Bool isSatellite = strstr((char *) optical->sys, "_KM");
        _Bool isRoving = strstr((char *) optical->sys, "WGS84");

        // Scale factor = 1 / 1 AU in km.
        const double sf = 1 / 149.59787e6;

        double x = strtod((char *) optical->pos1, NULL);
        double y = strtod((char *) optical->pos2, NULL);
        double z = strtod((char *) optical->pos3, NULL);

        if (isRoving){

            double *pos = roving_position(x,y,z);
            x = pos[0];
            y = pos[1];
            z = pos[2];

            double p = sqrt(x*x+y*y+z*z);
            printf("p = %lf\n", p);
        }

        if (isSatellite || isRoving)  {
            x *= sf;
            y *= sf;
            z *= sf;
        }



        obsp->earth_observer[0] = x;
        obsp->earth_observer[1] = y;
        obsp->earth_observer[2] = z;
        obsp->spacebased = 1;
    }

    return 1;
}

/**
 * parse_nodes - A function that parses a set of XML nodes and extracts relevant information to create and maintain a tracklet data structure.
 * @optical_nodes: A pointer to a set of XML nodes.
 * Returns: A pointer to the final tracklet data structure.
 */
tracklet *parse_nodes(xmlXPathObjectPtr optical_nodes) {
    xmlNodePtr cur;
    observation obs1;
    tracklet *tk = NULL;

    int size = (optical_nodes->nodesetval) ? optical_nodes->nodesetval->nodeNr : 0;
    int i=0;
    while (i < size) {
        cur = optical_nodes->nodesetval->nodeTab[i];
        opticalPtr opt = parse_optical(cur);

        _Bool pGood = processOptical(opt, &obs1);

        if (pGood) {
            if (tk == NULL || tk->status == INVALID || strcmp((char *) opt->trkSub, tk->desig)) {
                if(tk != NULL)
                    eval(tk);
                tk = resetValid((char *) opt->trkSub, &obs1);
                tk->isAdes = 1;
            } else {
                continueValid(tk, (char *) opt->trkSub, &obs1);
            }
        } else if (tk == NULL || tk->status == INVALID) {
            if(tk == NULL) tk = resetInvalid();
            else continueInvalid(tk);
        } else {
            eval(tk);
            tk = resetInvalid();
            tk->isAdes = 1;
        }
        i++;

    }

    return tk;
}

/**
 * parse_ades - A function that parses an ADES XML document located at @filepath, and extracts relevant information to create and maintain a tracklet data structure.
 * @filepath: A file path to the XML document to be parsed
 * Returns: A pointer to the final tracklet data structure, or NULL if an error occurs during parsing or if no relevant nodes are found.
 */
tracklet *parse_ades(const char *filepath) {

    /* Load XML document */
    xmlDocPtr doc = xmlParseFile(filepath);
    if (doc == NULL) {
        fprintf(stderr, "Error: unable to parse file \"%s\"\n", filepath);
        return NULL;
    }

    xmlXPathContextPtr xpathCtx = xmlXPathNewContext(doc);
    xmlXPathObjectPtr optical_nodes = xmlXPathEvalExpression("//optical", xpathCtx);

    if (optical_nodes == NULL) {
        fprintf(stderr, "Error: Nothing found...");
        xmlXPathFreeContext(xpathCtx);
        xmlFreeDoc(doc);
        return NULL;
    }

    tracklet *tk = parse_nodes(optical_nodes);
    xmlXPathFreeContext(xpathCtx);
    xmlFreeDoc(doc);

    return tk;
}
