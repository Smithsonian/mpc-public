CC = gcc
CFLAGS = -std=c99 -O2 -pthread -I/usr/include/libxml2
LDFLAGS = -lm -lxml2
SRC = digest2.c d2cli.c d2math.c d2model.c d2modelio.c d2mpc.c d2ades.c common.c
OBJ = $(SRC:.c=.o)
EXEC = digest2

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

debug: CFLAGS = -std=c99 -ggdb -pthread -I/usr/include/libxml2
debug: clean $(EXEC)

clean:
	rm -f $(OBJ) $(EXEC)

indent:
	indent *.c *.h
	rm *.c~ *.h~

.PHONY: all clean debug indent
