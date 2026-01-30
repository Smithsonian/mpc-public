#!/usr/bin/gmake -f
#
# Makefile
#
# Copyright (c) 2010 Sonia Keys
#
# See external file LICENSE, distributed with this software.

.PHONY: all
all: digest2 digest2.model digest2.obscodes

# digest2 executable
d2src = digest2.c d2model.c d2math.c d2mpc.c

digest2: $(d2src) digest2.h d2model.h
	gcc -o digest2 -std=c99 -Wall -pthread -lm $(d2src)

# data file needed by digest2
digest2.model: muk s3m.dat astorb.dat
	muk

# muk executable
muksrc = muk.c d2model.c

muk: $(muksrc) d2model.h
	gcc -o muk -std=c99 -Wall -lm $(muksrc)

# astorb.dat
astorb.dat:
	wget "ftp://ftp.lowell.edu/pub/elgb/astorb.dat.gz"
	gunzip "astorb.dat.gz"

# mpc.obscodes
digest2.obscodes:
	wget "http://www.cfa.harvard.edu/iau/lists/ObsCodes.html"
	sed '1d;$$d' ObsCodes.html >digest2.obscodes
