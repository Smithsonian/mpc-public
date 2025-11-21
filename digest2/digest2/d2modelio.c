// d2modelio.c
//
// Public domain.

// posix source added for fileno()
#define _POSIX_SOURCE

#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "digest2.h"

_Bool csvError(char *mod, char *class, int iq, int ie, int ii, char *heading)
{
  // printf("CSV error %s %s\n", mod, class);
  // printf("Q e i = %g %g %g\n", qpart[iq], epart[ie], ipart[ii]);
  // printf("%s field: \"%s\"\n", heading, field);
  sprintf(line, msgCSVData, fnCSV);
  return false;
}

// scans to ',' or end of string, copying to field as long as it fits.
// returns pointer to character of start that terminated the scan, ',' or
// the terminating null.  in the case where data would overflow field,
// nothing is copied and start is returned.
char *scanField(char *start)
{
  char *end = strchr(start, ',');
  if (!end) {
    end = strchr(start, 0);
  }
  int n = end - start;
  if (n > sizeof(field) - 1) {
    *field = 0;
    return start;
  }
  memcpy(field, start, n);
  field[n] = 0;
  return end;
}

_Bool
readCSVClass(FILE * fcsv, double pop[QX][EX][IX][HX], char *mod, char *class)
{
  char *t;
  double d;
  for (int iq = 0; iq < QX; iq++)
    for (int ie = 0; ie < EX; ie++)
      for (int ii = 0; ii < IX; ii++) {
        fgets(line, sizeof(line), fcsv);
        char *p = scanField(line);
        if (*p != ',' || strcmp(field, mod) != 0) {
          return csvError(mod, class, iq, ie, ii, "Model");
        }
        p = scanField(p + 1);
        if (*p != ',' || strcmp(field, class) != 0) {
          return csvError(mod, class, iq, ie, ii, "Class");
        }
        p = scanField(p + 1);
        if (*p != ',' || fabs(strtod(field, &t) - qpart[iq]) > 1e-9) {
          return csvError(mod, class, iq, ie, ii, "Q");
        }
        p = scanField(p + 1);
        if (*p != ',' || fabs(strtod(field, &t) - epart[ie]) > 1e-9) {
          return csvError(mod, class, iq, ie, ii, "e");
        }
        p = scanField(p + 1);
        if (*p != ',' || fabs(strtod(field, &t) - ipart[ii]) > 1e-9) {
          return csvError(mod, class, iq, ie, ii, "i");
        }
        for (int ih = 0; ih < HX; ih++) {
          p = scanField(p + 1);
          pop[iq][ie][ii][ih] = strtod(field, &t);
          if (*p == (ih < HX - 1 ? ',' : 0)) { // need delimiter
            if (t > field)
              continue;         // and either something parsed
            if (!*t || *t == '\n')
              continue;         // or empty field
          }
          // sprintf(line, "H%g", hpart[ih]);
          return csvError(mod, class, iq, ie, ii, line);
        }
      }
  return true;
}

void mheader()
{
  strcpy(line, "Model,Class,Q,e,i");
  int j = strlen(line);
  for (int i = 0; i < HX; i++) {
    j += sprintf(line + j, ",H%g", hpart[i]);
  }
  strcpy(line + j, "\n");
}

// on failure, global `line` will have a suitable error message.
_Bool readCSV(struct stat *buf)
{
  FILE *fcsv = openCP(fnCSV, 0, "r"); // 0 because no switch for this.
  if (!fcsv) {
    sprintf(line, msgOpen, fnCSV);
    return false;
  }

  mheader();
  char test_line[400];
  strcpy(test_line, line);
  fgets(line, sizeof(line), fcsv);
  if (strcmp(line, test_line)) {
    sprintf(line, msgCSVHeader, fnCSV);
    return false;
  }
  if (!readCSVClass(fcsv, modelAllSS, "All", "SS") ||
      !readCSVClass(fcsv, modelUnkSS, "Unk", "SS")) {
    sprintf(line, msgCSVData, fnCSV);
    return false;
  }
  for (int c = 0; c < D2CLASSES; c++) {
    if (!readCSVClass(fcsv, modelAllClass[c], "All", classAbbr[c])
        || !readCSVClass(fcsv, modelUnkClass[c], "Unk", classAbbr[c])) {
      sprintf(line, msgCSVData, fnCSV);
      return false;
    }
  }
  fstat(fileno(fcsv), buf);     // stat size and date for writeModel
  fclose(fcsv);
  return true;
}

void mustReadCSV(struct stat *buf)
{
  if (!readCSV(buf))
    fatal(line);
}

void writeModel(struct stat *csv)
{
    FILE *fp = fopen (fnModel, "r");
   if (fp)
     {
        fclose (fp);
        }
   else
     {
  FILE *fmod = openCP(fnModel, modelSpec, "w");
  if (!fmod ||
      !fwrite(&csv->st_size, sizeof(csv->st_size), 1, fmod) ||
      !fwrite(&csv->st_mtime, sizeof(csv->st_mtime), 1, fmod) ||
      !fwrite(modelAllSS, sizeof modelAllSS, 1, fmod) ||
      !fwrite(modelUnkSS, sizeof modelUnkSS, 1, fmod) ||
      !fwrite(modelAllClass, sizeof modelAllClass, 1, fmod) ||
      !fwrite(modelUnkClass, sizeof modelUnkClass, 1, fmod)) {
    // not fatal
    printf(msgWrite, fnModel);
  }
  fclose(fmod);
     }
}

_Bool readArrays(FILE * fmod)
{
  if (!fread(modelAllSS, sizeof modelAllSS, 1, fmod) ||
      !fread(modelUnkSS, sizeof modelUnkSS, 1, fmod) ||
      !fread(modelAllClass, sizeof modelAllClass, 1, fmod) ||
      !fread(modelUnkClass, sizeof modelUnkClass, 1, fmod)) {
    return false;
  }
  fclose(fmod);
  return true;
}

// read model from CSV, optionally with fmod as fallback.
// fatal if no model can be read.
// if csv read okay, attempt to write model.
// faliure to write model produces warning, not fatal.
void convertCSV(FILE * fmod)
{
  struct stat csv;
  if (!fmod) {
    mustReadCSV(&csv);          // with no fallback, this has to work
    writeModel(&csv);
    return;
  }
  if (!readCSV(&csv)) {
    if (!readArrays(fmod)) {    // if CSV fails, fallback must work
      fatal1(msgRead, fnCSV);
    }
    return;
  }
  // CSV okay. attempt model update.
  writeModel(&csv);
}

// read population model.
// prefer binary, with check that it matches the CSV.
void mustReadModelStatCSV()
{
  // start with binary, if it's not not there, options are limited.
  FILE *fmod = openCP(fnModel, modelSpec, "r");
  if (!fmod) {                  // no binary,
    convertCSV(0);              // try csv, with no binary fallback
    return;                     // success reading csv
  }
  // binary opened okay, read header
  struct stat mod;
  if (!fread(&mod.st_size, sizeof mod.st_size, 1, fmod) ||
      !fread(&mod.st_mtime, sizeof mod.st_mtime, 1, fmod)) {
    fclose(fmod);               // binary seems corrupt
    printf(msgReadInvalid, fnModel); // give warning message
    convertCSV(0);              // try replacing it, but with no binary fallback
    return;                     // success reading csv
  }
  // binary readable so far, stat csv and compare
  struct stat csv;
  int csv_stat_err = stat(CPspec(fnCSV, 0), &csv);
  if (csv_stat_err ||           // csv stat failed,
      csv.st_size != mod.st_size || // or size or time don't match
      csv.st_mtime != mod.st_mtime) {
    convertCSV(fmod);           // try replacing it, with fmod as fallback.
    return;                     // success reading csv
  }
  // at least no csv inconsistency, continue with binary
  _Bool bin_ok = readArrays(fmod);
  if (bin_ok) {
    return;                     // success reading binary
  }
  // last chance
  if (!csv_stat_err) {
    convertCSV(0);
    return;                     // whew, success reading csv
  }

  printf(msgReadInvalid, fnModel); // message about binary
  fatal1(msgRead, fnCSV);       // and ultimate failure
}

void mustReadModel()
{
  FILE *fmod = openCP(fnModel, modelSpec, "r");
  if (!fmod) {
    fatal1(msgOpen, fnModel);
  }
  struct stat mod;
  if (!fread(&mod.st_size, sizeof mod.st_size, 1, fmod) ||
      !fread(&mod.st_mtime, sizeof mod.st_mtime, 1, fmod) ||
      !readArrays(fmod)) {
    fatal1(msgRead, fnModel);
  }
}
