//! C99

// s3mtest.c

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "d2model.h"

#define LINE_SIZE 300

_Bool isTrojan(double q, double e, double i);
// structure of binned population model

int s3m[D2CLASSES][HX];
int aod[D2CLASSES][HX];

void binS3m(char *fn, _Bool clipNeo)
{
    puts(fn);
    FILE *fmodel = fopen(fn, "r");
    if (!fmodel) {
        printf("Open %s failed.\n", fn);
        exit(-1);
    }

    char line[LINE_SIZE];
    do
        if (!fgets(line, LINE_SIZE, fmodel)) {
            printf("Read %s failed.\n", fn);
            fclose(fmodel);
            exit(-1);
        }
    while (line[0] == '!' && line[1] == '!');

    int hEnd = -1;
    sscanf(line, "%*s %*s %*f %*f %*f %*f %*f %*f %*f%n", &hEnd);
    if (hEnd == -1) {
        puts("Unexpected format:");
        puts(line);
        fclose(fmodel);
        exit(-1);
    }

    double q, e, i, h;
    do {
        if (sscanf(line, "%*s %*s %lf %lf %lf %*f %*f %*f %lf",
                   &q, &e, &i, &h) != 4 ||
            q <= 0. || e < 0. || e > 1. || i < 0. || i >= 180.) {
//         printf("Unexpected q e i h: %s\n", line);
            continue;
        }

        if (clipNeo && q < 1.3) {
//         printf("Unexpected NEO orbit: %s\n", line);
            continue;
        }

        if (q < 1.3 && h < 6) {
            printf("%f %f\n", q, h);
            puts(line);
            exit(-1);
        }
        int bin[4];
        if (!qeihToBin(q, e, i, h, bin))
            continue;

        int ih = bin[3];

        for (int c = 0; c < D2CLASSES; c++)
            if ((*isClass[c]) (q, e, i, h)) {
                s3m[c][ih]++;
            }
    }
    while (fgets(line, LINE_SIZE, fmodel));

    fclose(fmodel);
}

int main()
{
    binS3m("../../s3m/S0.s3m", 0);      // NEO
    binS3m("../../s3m/SJ.s3m", 1);      // JFC
//   binS3m("../s3m/SL.s3m", 1);    // LPC
    binS3m("../../s3m/SR.s3m", 1);      // SPC
    binS3m("../../s3m/SS.s3m", 1);      // SDO
    binS3m("../../s3m/ST.s3m", 1);      // TNO
    binS3m("../../s3m/St5.s3m", 1);     // Jupiter Trojan
    binS3m("../../s3m/S1_00.s3m", 1);   // MB
    binS3m("../../s3m/S1_01.s3m", 1);
    binS3m("../../s3m/S1_02.s3m", 1);
    binS3m("../../s3m/S1_03.s3m", 1);
    binS3m("../../s3m/S1_04.s3m", 1);
    binS3m("../../s3m/S1_05.s3m", 1);
    binS3m("../../s3m/S1_06.s3m", 1);
    binS3m("../../s3m/S1_07.s3m", 1);
    binS3m("../../s3m/S1_08.s3m", 1);
    binS3m("../../s3m/S1_09.s3m", 1);
    binS3m("../../s3m/S1_10.s3m", 1);
    binS3m("../../s3m/S1_11.s3m", 1);
    binS3m("../../s3m/S1_12.s3m", 1);
    binS3m("../../s3m/S1_13.s3m", 1);

    char *fn = "astorb.dat";
    char line[300];
    printf("Reading %s:\n", fn);
    FILE *forb = fopen(fn, "r");
    if (!forb) {
        printf("Open %s failed.\n", fn);
        return (-1);
    }

    if (!fgets(line, LINE_SIZE, forb)) {
        printf("Read %s failed.\n", fn);
        fclose(forb);
        return (-1);
    }

    int lines = 0;
    int good = 0;
    int decpeuy_fails = 0;
    int decpeu_rejects = 0;
    int parsefails = 0;
    int outofmodel = 0;
    do {
        lines++;
        line[246] = 0;          /* ok to step on month */
        int decpeuy = atoi(line + 242);
        if (errno || decpeuy < 2000) {
            decpeuy_fails++;
            continue;
        }
        line[241] = 0;          /* ok, this is just a space */
        double decpeu = atof(line + 234);
        if (errno || decpeu > 60.) {
            decpeu_rejects++;
            continue;
        }
        line[181] = 0;          /* just a space */
        double a = atof(line + 169);
        if (errno) {
            parsefails++;
            continue;
        }
        line[168] = 0;
        double e = atof(line + 158);
        if (errno) {
            parsefails++;
            continue;
        }
        line[157] = 0;
        double i = atof(line + 147);
        if (errno) {
            parsefails++;
            continue;
        }
        line[47] = 0;
        double h = atof(line + 42);
        if (errno) {
            parsefails++;
            continue;
        }

        double q = a * (1 - e);
        int bin[4];
        if (!qeihToBin(q, e, i, h, bin)) {
            outofmodel++;
            continue;
        }

        good++;
        int ih = bin[3];

        for (int c = 0; c < D2CLASSES; c++)
            if ((*isClass[c]) (q, e, i, h))
                aod[c][ih]++;
    }
    while (fgets(line, LINE_SIZE, forb));
    fclose(forb);

    for (int c = 1; c < D2CLASSES; c++) {
        puts(classHeading[c]);
        puts(" H        S3M  astorb.dat   %");
        for (int ih = 0; ih < HX; ih++) {
            double p = s3m[c][ih]
                ? 100. * (double) aod[c][ih] / (double) s3m[c][ih]
                : -1;
            printf("%4.1f%9d%9d%7.0f\n", hpart[ih], s3m[c][ih], aod[c][ih],
                   p);
        }
        puts("");
    }
}
