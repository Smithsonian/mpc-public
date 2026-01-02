// d2cli.c
//
// Public domain.

#include <assert.h>
#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "digest2.h"

char msgVersion[] =
  "Digest2 version 0.19 -- Released August 16, 2017 -- Compiled %s\n";
char msgCopyright[] = "Public domain.";

// stuff used for parsing command line
//-----------------------------------------------------------------------------
char line[LINE_SIZE];
char field[FIELD_SIZE];
char sOpt[] = "hvc:m:o:p:u:l:";
struct option lOpt[] = {
  {"help", no_argument, 0, 'h'},
  {"version", no_argument, 0, 'v'},
  {"config", required_argument, 0, 'c'},
  {"model", required_argument, 0, 'm'},
  {"obscodes", required_argument, 0, 'o'},
  {"config-path", required_argument, 0, 'p'},
  {"cpu", required_argument, 0, 'u'},
  {"limit", required_argument, 0, 'l'},
  {0, 0, 0, 0}
};

_Bool configSpec = 0;
_Bool modelSpec = 0;
_Bool ocdSpec = 0;
_Bool pathSpec = 0;
_Bool cpuSpec = 0;
_Bool limitSpec = 0;
_Bool classPossible;
_Bool raw, noid;
_Bool headings, rms, repeatable;
int nClassCompute;
int nClassColumns;
int classCompute[D2CLASSES];
int classColumn[D2CLASSES];
int limitClass;
_Bool limitRaw;
int limit;

// "constant" global data
//-----------------------------------------------------------------------------
// global data that is constant, at least after being initialized, and so
// can be shared by threads.

char *fnConfig = "digest2.config";
char *fnModel = "digest2.model";
char *fnCSV = "digest2.model.csv";
char *fnOCD = "digest2.obscodes";
char *fpConfig = "";

char msgAccess[] = "Cannot access URL %s\n";
char msgCSVHeader[] = "Invalid CSV header:  %s\n";
char msgCSVData[] = "Invalid CSV data:  %s\n";
char msgCSVStat[] = "%s:         %d bytes %s"; // file name, size, date
char msgConfig[] = "Unrecognized line in config file:  %s\n";
char msgMemory[] = "Memory allocation failed.\n";
char msgMissing[] = "%s not present.\n";
char msgModelBasis[] = "%s source data: %d bytes %s";
char msgOpen[] = "Open %s failed.\n";
char msgRead[] = "Read %s failed.\n";
char msgWrite[] = "Write %s failed.\n";
char msgReadInvalid[] = "Read %s failed, contents invalid.\n";
char msgStatus[] = "Internal error:  Unexpected tracklet status.\n";
char msgThread[] = "Thread creation failed.\n";
char msgOption[] = "Unknown option: %s\n";
char msgObsErr[] = "%s\nConfig file line: %s\n";
char msgLimit[] = "--limit invalid syntax: %s\n";
char msgLimitClass[] = "--limit invalid orbit class: %s (see digest2 -h)\n";
char msgLimitLimit[] = "--limit value must be in range [1,100]: %s\n";
char msgLimitClassNotConfig[] = "--limit orbit class not configured\n";
char msgLimitScoreNotConfig[] = "--limit score not configured\n";
char msgUsage[] = "\
Usage: digest2 [options] <obs file>    score observations in file\n\
       digest2 [options] -             score observations from stdin\n\
       digest2 -m <binary model file>  generate binary model from CSV\n\
       digest2 -h or --help            display help and quick reference\n\
       digest2 -v or --version         display program version and model date\n\
\n\
Options:\n\
       -c or --config <config file>\n\
       -m or --model <binary model file>\n\
       -o or --obscodes <obscode file>\n\
       -p or --config-path <path>\n\
       -u or --cpu <n-cores>\n\
       -l or --limit <class>/<score>=<limit>\n";

// functions
//-----------------------------------------------------------------------------

/* fatal

print message to stdout and terminate program.
*/
void fatal(char *msg)
{
  fputs(msg, stderr);
  exit(-1);
}

void fatal1(char *msg, char *arg)
{
  fprintf(stderr, msg, arg);
  exit(-1);
}

void fatal2(char *msg, char *arg1, char *arg2)
{
  fprintf(stderr, msg, arg1, arg2);
  exit(-1);
}

char *CPspec(char *fn, _Bool spec)
{
  if (spec || !pathSpec) {
    return fn;
  }
  char *p = malloc(strlen(fpConfig) + strlen(fn) + 2);
  sprintf(p, "%s/%s", fpConfig, fn);
  return p;
}

// Note this function can return null.
// The result must be checked for null before use.
FILE *openCP(char *fn, _Bool spec, char *mode)
{
  return fopen(CPspec(fn, spec), mode);
}

char *parseObsErr(char *s)
{
  regmatch_t ss[3];
  int r = regexec(&rxObsErr, s, 3, ss, 0);
  if (r == REG_ESPACE)
    fatal(msgMemory);
  if (r == REG_NOMATCH)
    return "Invalid format for obserr.";
  char *endp;
  errno = 0;
  double oe = strtod(s + ss[2].rm_so, &endp);
  if (errno != 0 || endp != s + ss[2].rm_eo)
    return "Invalid obserr value.";
  if (oe > 10)
    return "Observational error > 10 arc seconds not allowed.";
  if (ss[1].rm_eo == ss[1].rm_so) {
    obsErr = oe * arcsecrad;
    return 0;
  }
  int oc = parseCod3(s + ss[1].rm_so);
  if (oc < 0)
    return "Obscode not recognized.";
  siteTable[oc].obsErr = oe * arcsecrad;
  return 0;
}

void readConfig()
{
  FILE *fcfg = openCP(fnConfig, configSpec, "r");

  if (!fcfg) {
    if (!configSpec)
      // config file not required to exist unless a config file name
      // is specified on the command line
      return;

    fatal1(msgOpen, fnConfig);
  }

  char line[20];
  if (!fgets(line, sizeof(line), fcfg)) {
    fprintf(stderr, msgRead, fnConfig);
    if (!configSpec)
      return;
    exit(-1);
  }

  _Bool rawSpec = 0;
  _Bool classSpec = 0;
  do {
    if (line[strlen(line) - 1] == '\n')
      line[strlen(line) - 1] = 0;

    if (*line == 0 || *line == '#')
      continue;                 // skip empty lines and comments

    if (!strcmp(line, "headings")) {
      headings = 1;
      continue;
    }
    if (!strcmp(line, "noheadings")) {
      headings = 0;
      continue;
    }
    if (!strcmp(line, "rms")) {
      rms = 1;
      continue;
    }
    if (!strcmp(line, "norms")) {
      rms = 0;
      continue;
    }
    if (!strcmp(line, "raw")) {
      if (!rawSpec) {
        rawSpec = 1;
        noid = 0;
      }
      raw = 1;
      continue;
    }
    if (!strcmp(line, "noid")) {
      if (!rawSpec) {
        rawSpec = 1;
        raw = 0;
      }
      noid = 1;
      continue;
    }
    if (!strcmp(line, "poss")) {
      if (!classSpec) {
        classSpec = 1;
        nClassColumns = 0;
      }
      classPossible = 1;
      continue;
    }
    if (!strcmp(line, "repeatable")) {
      repeatable = 1;
      continue;
    }
    if (!strcmp(line, "random")) {
      repeatable = 0;
      continue;
    }
    if (!strncmp(line, "obserr", 6)) {
      char *errStr = parseObsErr(line + 6);
      if (errStr)
        fatal2(msgObsErr, errStr, line);
      continue;
    }
    for (int c = 0;; c++) {
      if (c == D2CLASSES)
        fatal1(msgConfig, line);
      if (!strcmp(line, classHeading[c]) || !strcmp(line, classAbbr[c])) {
        if (!classSpec) {
          classSpec = 1;
          nClassColumns = 0;
          classPossible = 0;
        }
        classColumn[nClassColumns++] = c;
        break;
      }
    }
  }
  while (fgets(line, sizeof(line), fcfg));

  // by default, we were going to compute all classes, but if classes
  // have been specified here and poss was not specified, then only
  // the specified classes need to be computed.
  if (classSpec && !classPossible)
    for (nClassCompute = 0; nClassCompute < nClassColumns; nClassCompute++)
      classCompute[nClassCompute] = classColumn[nClassCompute];
}

void printVersion()
{
  printf(msgVersion, __DATE__);
  puts(msgCopyright);

  // attempt date/size of csv
  struct stat csv;
  int csv_stat_err = stat(CPspec(fnCSV, 0), &csv);
  if (csv_stat_err) {           // csv stat failed
    printf(msgMissing, fnCSV);
  } else {
    printf(msgCSVStat, fnCSV, csv.st_size, ctime(&csv.st_mtime));
  }

  // attempt read model header
  struct stat mod;
  FILE *fmod = openCP(fnModel, modelSpec, "r");
  if (!fmod) {                  // no binary,
    printf(msgMissing, fnModel);
    return;
  }
  if (!fread(&mod.st_size, sizeof mod.st_size, 1, fmod) ||
      !fread(&mod.st_mtime, sizeof mod.st_mtime, 1, fmod)) {
    fclose(fmod);               // binary seems corrupt
    printf(msgRead, fnModel);
    return;
  }
  printf(msgModelBasis, fnModel, mod.st_size, ctime(&mod.st_mtime));
}

void mustParseLimit(char *optarg)
{
  regex_t rxLimit;
  assert(regcomp(&rxLimit, "^(.+)/(raw|noid)=([0-9]+)$", REG_EXTENDED) == 0);
  regmatch_t ss[4];
  int r = regexec(&rxLimit, optarg, 4, ss, 0);
  if (r == REG_ESPACE)
    fatal(msgMemory);
  if (r == REG_NOMATCH)
    fatal1(msgLimit, optarg);

  // set limitClass
  for (int c = 0;; c++) {
    if (c == D2CLASSES)
      fatal1(msgLimitClass, optarg);
    if (!strncmp(optarg, classHeading[c], ss[1].rm_eo)
        || !strncmp(optarg, classAbbr[c], ss[1].rm_eo)) {
      limitClass = c;
      break;
    }
  }

  // set limitRaw
  limitRaw = optarg[ss[2].rm_so] == 'r'; // (we know it matched raw or noid)

  // set limit
  limit = atoi(optarg + ss[3].rm_so);
  if (limit < 1 || limit > 100) {
    fatal1(msgLimitLimit, optarg);
  }
}

// returns obs file specified on command line.  this can be null, "-",
// or a filespec.
char *parseCl(int argc, char **argv)
{
  while (1) {
    int ox;
    int oc = getopt_long(argc, argv, sOpt, lOpt, &ox);

    switch (oc) {
    case 'h':
      puts("\
Digest2 help\n\
\n\
Digest2 uses statistical ranging techniques on short arc astrometry to\n\
compute probabilities that observed objects are of various orbit classes.\n\
Input is a file of 80 column MPC-format observations, with at least two\n\
observations per object.  Output is orbit class scores for each object.\n\
\n\
Config file keywords:\n\
   headings\n\
   noheadings\n\
   rms\n\
   norms\n\
   raw\n\
   noid\n\
   repeatable\n\
   random\n\
   poss\n\
   obserr\n\
\n\
Orbit classes:");
      for (int c = 0; c < D2CLASSES; c++)
        printf("   %-5s %-15s\n", classAbbr[c], classHeading[c]);
      puts("\nSee README for additional information.");
      exit(0);
    case 'v':
      printVersion();
      exit(0);
    case 'c':
      fnConfig = optarg;
      configSpec = 1;
      break;
    case 'm':
      fnModel = optarg;
      modelSpec = 1;
      break;
    case 'o':
      fnOCD = optarg;
      ocdSpec = 1;
      break;
    case 'p':
      fpConfig = optarg;
      pathSpec = 1;
      int last = strlen(fpConfig) - 1;
      if (fpConfig[last] == '/')
        fpConfig[last] = 0;
      break;
    case 'u':
      cores = atoi(optarg);
      cpuSpec = 1;
      break;
    case 'l':
      mustParseLimit(optarg);
      limitSpec = 1;
      break;
    case -1:
      // typcally one arg should be left, the input observation file.
      // it can be "-", meaning read from stdin.
      // if no args remain, -m or -o is required.
      if (optind == argc && (modelSpec || ocdSpec)) {
        return 0;
      }
      char *fnObs = argv[optind];
      if (optind == argc - 1 && (fnObs[0] != '-' || fnObs[1] == 0)) {
        return fnObs;
      }
      // else fall through
    default:
      fatal(msgUsage);
    }
  }
}
