//
// Created by Richard Cloete on 9/1/22.
//
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include "common.h"

/* parseCod3

convert 3 character MPC obscode to integer

Returns:
   0-3599 on successful parse. (3599 = obscodeNamespaceSize - 1)
   -1 on failure.
*/
int parseCod3(char *cod3)
{
    int hp;

    if (isdigit(*cod3))
        hp = *cod3 - '0';
    else if (*cod3 >= 'A' && *cod3 <= 'Z')
        hp = *cod3 - 'A' + 10;
    else
        return -1;

    if (isdigit(cod3[1]) && isdigit(cod3[2]))
        return hp * 100 + (cod3[1] - '0') * 10 + cod3[2] - '0';

    return -1;
}

/* mustStrtod

for required fields.  a version of atof that sets errno on blank input.
also allows whitespace after sign
*/
double mustStrtod(char *str)
{
    char *endp;
    _Bool neg = *str == '-';
    if (neg || *str == '+')
        str++;
    double result = strtod(str, &endp);
    if (!errno && endp == str)
        errno = EINVAL;
    return neg ? -result : result;
}

/* mustStrtoi

returns int but actually disallows negatives.
*/
int mustStrtoi(char *str)
{
    char *endp;
    long result = strtol(str, &endp, 10);
    if (!errno)
        if (endp == str || result < 0 || result > INT_MAX)
            errno = EINVAL;
    return result;
}

double updateMagnitude(char band, double mag){
    if (mag > 0) {
        switch (band) {
            case 'V':
                break;
            case 'B':
                mag -= .8;
                break;
            case 'U':
                mag -= 1.3;
                break;
            case 'g':
                mag -= 0.35;
                break;
            case 'r':
                mag += 0.14;
                break;
            case 'R':
                mag += 0.4;
                break;
            case 'C':
                mag += 0.4;
                break;
            case 'W':
                mag += 0.4;
                break;
            case 'i':
                mag += 0.32;
                break;
            case 'z':
                mag += 0.26;
                break;
            case 'I':
                mag += 0.8;
                break;
            case 'J':
                mag += 1.2;
                break;
            case 'w':
                mag -= 0.13;
                break;
            case 'y':
                mag += 0.32;
                break;
            case 'L':
                mag += 0.2;
                break;
            case 'H':
                mag += 1.4;
                break;
            case 'K':
                mag += 1.7;
                break;
            case 'Y':
                mag += 0.7;
                break;
            case 'G':
                mag += 0.28;
                break;
            case 'v':
                mag += 0;
                break;
            case 'c':
                mag -= 0.05;
                break;
            case 'o':
                mag += 0.33;
                break;
            case 'u':
                mag += 2.5;
                break;
            default:
                mag += .4;
                break;
        }
    }
    return mag;
}

