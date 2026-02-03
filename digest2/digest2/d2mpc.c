// d2mpc.c
//
//
// Update Oct. 7, 2021: added band conversion 'u' and CMOS 'B', by Peter Veres
// Public domain.

#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "digest2.h"
#include <math.h>
#define OCD_URL "https://minorplanetcenter.net/iau/lists/ObsCodes.html"

// functions
//-----------------------------------------------------------------------------

/* parseCod3

convert 3 character MPC obscode to integer

Returns:
   0-3599 on successful parse. (3599 = obscodeNamespaceSize - 1)
   -1 on failure.
*/
//int parseCod3(char *cod3)
//{
//  int hp;
//
//  if (isdigit(*cod3))
//    hp = *cod3 - '0';
//  else if (*cod3 >= 'A' && *cod3 <= 'Z')
//    hp = *cod3 - 'A' + 10;
//  else
//    return -1;
//
//  if (isdigit(cod3[1]) && isdigit(cod3[2]))
//    return hp * 100 + (cod3[1] - '0') * 10 + cod3[2] - '0';
//
//  return -1;
//}

/* mustStrtod

for required fields.  a version of atof that sets errno on blank input.
also allows whitespace after sign
*/
//double mustStrtod(char *str)
//{
//  char *endp;
//  _Bool neg = *str == '-';
//  if (neg || *str == '+')
//    str++;
//  double result = strtod(str, &endp);
//  if (!errno && endp == str)
//    errno = EINVAL;
//  return neg ? -result : result;
//}

///* mustStrtoi
//
//returns int but actually disallows negatives.
//*/
//int mustStrtoi(char *str)
//{
//  char *endp;
//  long result = strtol(str, &endp, 10);
//  if (!errno)
//    if (endp == str || result < 0 || result > INT_MAX)
//      errno = EINVAL;
//  return result;
//}

/* readOCD()

read obscode.dat into memory.

Notes:
   On file error, leaves error message in line and returns false.

   Units of rho sin/cos phi in obscode.dat are equatorial radii
   of the Earth.  Converted to AU here for easier use later.
   Units of longitude are degrees, 
   Converted here to circles for easier use later.
*/
_Bool readOCD(void)
{
  FILE *focd = openCP(fnOCD, ocdSpec, "r");
  if (!focd) {
    sprintf(line, msgOpen, fnOCD);
    return false;
  }

  if (!fgets(line, sizeof(line), focd)) {
    sprintf(line, msgRead, fnOCD);
    return false;
  }

  site *psite = siteTable;
  for (int i = 0; i < obscodeNamespaceSize; i++, psite++) {
    psite->obsErr = -1;         // means unspecified
  }
  // Scale factor = earth radius in m / 1 AU in m.
  const double sf = 6.37814e6 / 149.59787e9;

  do {
    int idx = parseCod3(line);
    if (idx < 0)
      continue;

    double lon, rcos, rsin;
    errno = 0;
    line[30] = 0;
    rsin = mustStrtod(line + 21);
    line[21] = 0;
    rcos = mustStrtod(line + 13);
    line[13] = 0;
    lon = mustStrtod(line + 4);
    if (errno)
      continue;

    site *ps = siteTable + idx;
    ps->longitude = lon / 360.;
    ps->rhoCosPhi = rcos * sf;
    ps->rhoSinPhi = rsin * sf;
  }
  while (fgets(line, LINE_SIZE, focd));

  fclose(focd);
  return true;
}

void mustReadOCD(void)
{
  if (!readOCD()) {
    fatal(line);
  }
}

_Bool getOCD()
{
  FILE *fp = fopen (fnOCD, "r");
  if (fp)
    {
      fclose (fp);
      return false;
      }
  else
    {
  sprintf(line, "curl %s -o %s", OCD_URL, CPspec(fnOCD, ocdSpec));
  if (system(line) != 0) {
    fprintf(stderr, msgAccess, OCD_URL);
    return false;
  }
    return true;
    }
  return true;
}

void mustReadGetOCD()
{
  if (readOCD()) {
    return;
  }
  if (!getOCD()) {
    exit(-1);
  }
  mustReadOCD();
}

/* parseMpc80

parse an observation line.

Returns:
   success or failure.

Side effect on passed observation line:
   line is perforated by zeros as part of  parsing process.
   if function returns success, line will be zero-terminated
   after the 12-character designation field.

Side effect on passed observation struct:
   on successful parse, observation struct is updated
   with parsed values.
*/
_Bool parseMpc80(char *line, observation * obsp)
{
  if (line[14] != 'C' && line[14] != 'S' && line[14] != 'B')
    return 0;

  // parse right to left so we can punch line with zeros as needed
  int site = parseCod3(line + 77);
  if (site < 0)
    return 0;
  char band = line[70];
  line[70] = 0;
  errno = 0;
  // strtod meets our needs here to return 0 without error on blank input
  double mag = strtod(line + 65, 0);
  line[56] = 0;
  // other fields are required.  use mustStrtod.
  double decs = mustStrtod(line + 51);
  line[50] = 0;
  int decm = mustStrtoi(line + 48);
  line[47] = 0;
  int decd = mustStrtoi(line + 45);
  char decg = line[44];
  line[44] = 0;
  double ras = mustStrtod(line + 38);
  line[37] = 0;
  int ram = mustStrtoi(line + 35);
  line[34] = 0;
  int rah = mustStrtoi(line + 32);
  line[32] = 0;
  double day = mustStrtod(line + 23);
  line[22] = 0;
  int month = mustStrtoi(line + 20);
  line[19] = 0;
  int year = mustStrtoi(line + 15);
  line[12] = 0;
  if (errno)
    return 0;

  static int flookup[] =
    { 0, 306, 337, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275 };

  int z = year + (month - 14) / 12;
  int m = flookup[month] + 365 * z + z / 4 - z / 100 + z / 400 - 678882;
  obsp->mjd = m + day;
  obsp->ra = ((rah * 60 + ram) * 60 + ras) * M_PI / (12 * 3600);
  double dec = ((decd * 60 + decm) * 60 + decs) * M_PI / (180 * 3600);
  obsp->dec = decg == '-' ? -dec : dec;

  obsp->vmag = updateMagnitude(band, mag);
  obsp->site = site;
  obsp->spacebased = 0;

  return 1;
}

_Bool parseMpcRoving(char *line, observation * obsp){
    // Scale factor = 1 / 1 AU in km.
    const double sf = 1 / 149.59787e6;

//    TODO: Ask Peter if this is needed.
//    if (parseCod3(line + 77) != obsp->site)
//        return 0;
    errno = 0;
    line[69] = 0;
    double z = mustStrtod(line + 58);
    line[57] = 0;
    double y = mustStrtod(line + 46);
    line[45] = 0;
    double x = mustStrtod(line + 34);
    if (errno)
        return 0;

    double *pos = roving_position(x,y,z);
    x = pos[0];
    y = pos[1];
    z = pos[2];

    double p = sqrt(x*x+y*y+z*z);
    printf("p = %lf\n", p);

    x *= sf;
    y *= sf;
    z *= sf;

    obsp->earth_observer[0] = x;
    obsp->earth_observer[1] = y;
    obsp->earth_observer[2] = z;
    obsp->spacebased = 1;
    return 1;
}

_Bool parseMpcSat(char *line, observation * obsp)
{
  // Scale factor = 1 / 1 AU in km.
  const double sf = 1 / 149.59787e6;

  if (parseCod3(line + 77) != obsp->site)
    return 0;
  errno = 0;
  line[69] = 0;
  double z = mustStrtod(line + 58);
  line[57] = 0;
  double y = mustStrtod(line + 46);
  line[45] = 0;
  double x = mustStrtod(line + 34);
  if (errno)
    return 0;
  if (line[32] == '1') {
    x *= sf;
    y *= sf;
    z *= sf;
  }
  obsp->earth_observer[0] = x;
  obsp->earth_observer[1] = y;
  obsp->earth_observer[2] = z;
  obsp->spacebased = 1;
  return 1;
}
