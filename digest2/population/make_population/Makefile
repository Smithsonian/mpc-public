# Public domain.

d2dir  = ../digest2
s3msrc = s3mbin.c $(d2dir)/d2model.c
muksrc = muk.c $(d2dir)/d2model.c

muk: $(muksrc) $(d2dir)/d2model.h
	gcc -o muk -std=c11 -I$(d2dir) $(muksrc) -lm

s3mbin: $(s3msrc) $(d2dir)/d2model.h
	gcc -o s3mbin -std=c11 -I$(d2dir) $(s3msrc) -lm
