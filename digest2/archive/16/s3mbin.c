//! C99

// s3mbin.c

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "d2model.h"

#define LINE_SIZE 300

// structure of binned population model

double all_ss[QX][EX][IX][HX];
double all_class[D2CLASSES][QX][EX][IX][HX];

int nAll, nOrbits;
int nClass[D2CLASSES];

void binS3m(char *fn, _Bool clipNeo)
{
    puts(fn);
    char line[LINE_SIZE];
    if (snprintf(line, LINE_SIZE, "../../s3m/%s", fn) >= LINE_SIZE) {
        puts("Path buffer overflow");
        exit(-1);
    }
    char *qfn = malloc(strlen(line) + 1);
    if (!qfn) {
        puts("Memory allocation failed");
        exit(-1);
    }
    strcpy(qfn, line);
    FILE *fmodel = fopen(qfn, "r");
    if (!fmodel) {
        printf("Open %s failed.\n", qfn);
        exit(-1);
    }

    do
        if (!fgets(line, LINE_SIZE, fmodel)) {
            printf("Read %s failed.\n", qfn);
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
            q <= 0. || e < 0. || e > 1.1 || i < 0. || i >= 180.) {
//         printf("Unexpected q e i h: %s\n", line);
            continue;
        }
        nOrbits++;

        if (clipNeo && q < 1.3) {
//         printf("Unexpected NEO orbit: %s\n", line+qStart);
            continue;
        }

        int bin[4];
        if (!qeihToBin(q, e, i, h, bin))
            continue;

        nAll++;
        int iq = bin[0];
        int ie = bin[1];
        int ii = bin[2];
        int ih = bin[3];
        all_ss[iq][ie][ii][ih]++;

        for (int c = 0; c < D2CLASSES; c++)
            if ((*isClass[c]) (q, e, i, h)) {
                nClass[c]++;
                all_class[c][iq][ie][ii][ih]++;
            }
    }
    while (fgets(line, LINE_SIZE, fmodel));

    fclose(fmodel);
}

int main()
{
    binS3m("S0.s3m", 0);        // NEO
    binS3m("SJ.s3m", 1);        // JFC
//   binS3m("SL.s3m", 1);    // LPC
    binS3m("SR.s3m", 1);        // SPC
    binS3m("SS.s3m", 1);        // SDO
    binS3m("ST.s3m", 1);        // TNO
    binS3m("St5.s3m", 1);       // Jupiter Trojan
    binS3m("S1_00.s3m", 1);     // MB
    binS3m("S1_01.s3m", 1);
    binS3m("S1_02.s3m", 1);
    binS3m("S1_03.s3m", 1);
    binS3m("S1_04.s3m", 1);
    binS3m("S1_05.s3m", 1);
    binS3m("S1_06.s3m", 1);
    binS3m("S1_07.s3m", 1);
    binS3m("S1_08.s3m", 1);
    binS3m("S1_09.s3m", 1);
    binS3m("S1_10.s3m", 1);
    binS3m("S1_11.s3m", 1);
    binS3m("S1_12.s3m", 1);
    binS3m("S1_13.s3m", 1);

    printf("%d orbits\n", nOrbits);
    printf("%d in model\n", nAll);

    char *fn = "s3m.dat";
    FILE *fbin = fopen(fn, "w");
    if (!fbin) {
        printf("Create %s failed", fn);
        return (-1);
    }

    fputs("S3M binned\n", fbin);

    fputs("q", fbin);
    for (int ix = 0; ix < QX; ix++)
        fprintf(fbin, " %g", qpart[ix]);
    fputs("\ne", fbin);
    for (int ix = 0; ix < EX; ix++)
        fprintf(fbin, " %g", epart[ix]);
    fputs("\ni", fbin);
    for (int ix = 0; ix < IX; ix++)
        fprintf(fbin, " %g", ipart[ix]);
    fputs("\nh", fbin);
    for (int ix = 0; ix < HX; ix++)
        fprintf(fbin, " %g", hpart[ix]);
    fputs("\n", fbin);

    for (int iq = 0; iq < QX; iq++) {
        for (int ie = 0; ie < EX; ie++) {
            for (int ii = 0; ii < IX; ii++) {
                for (int ih = 0; ih < HX; ih++) {
                    fprintf(fbin, "%g ", all_ss[iq][ie][ii][ih]);
                }
                fprintf(fbin, "\n");
            }
        }
    }
    for (int c = 0; c < D2CLASSES; c++) {
        fprintf(fbin, "%s\n", classHeading[c]);

        for (int iq = 0; iq < QX; iq++) {
            for (int ie = 0; ie < EX; ie++) {
                for (int ii = 0; ii < IX; ii++) {
                    for (int ih = 0; ih < HX; ih++) {
                        fprintf(fbin, "%g ", all_class[c][iq][ie][ii][ih]);
                    }
                    fprintf(fbin, "\n");
                }
            }
        }
    }

    fclose(fbin);
}
