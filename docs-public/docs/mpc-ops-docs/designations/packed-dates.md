# Packed Dates

Dates of the form YYYYMMDD may be packed into five characters to conserve space.

The first two digits of the year are packed into a single character in column 1
(I = 18, J = 19, K = 20). Columns 2-3 contain the last two digits of the year.
Column 4 contains the month and column 5 contains the day, coded as detailed below:

```
   Month     Day      Character         Day      Character
                     in Col 4 or 5              in Col 4 or 5
   Jan.       1           1             17           H
   Feb.       2           2             18           I
   Mar.       3           3             19           J
   Apr.       4           4             20           K
   May        5           5             21           L
   June       6           6             22           M
   July       7           7             23           N
   Aug.       8           8             24           O
   Sept.      9           9             25           P
   Oct.      10           A             26           Q
   Nov.      11           B             27           R
   Dec.      12           C             28           S
             13           D             29           T
             14           E             30           U
             15           F             31           V
             16           G
```

Examples:

```
   1996 Jan. 1    = J9611
   1996 Jan. 10   = J961A
   1996 Sept.30   = J969U
   1996 Oct. 1    = J96A1
   2001 Oct. 22   = K01AM
```

This system can be extended to dates with non-integral days. The decimal fraction of the
day is simply appended to the five characters defined above.

Examples:

```
   1998 Jan. 18.73     = J981I73
   2001 Oct. 22.138303 = K01AM138303
```
