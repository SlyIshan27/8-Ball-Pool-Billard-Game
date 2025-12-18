# Makefile for SWIG + Python module
CC = clang
CFLAGS = -Wall -pedantic -fPIC -std=c99
PYTHON_INCLUDE = /usr/include/python3.11
LIBS = -lm

all: _phylib.so

# Compile the C library
phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

# Generate Python wrapper
phylib_wrap.c: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -I$(PYTHON_INCLUDE) -c phylib_wrap.c -o phylib_wrap.o

# Build the Python module
_phylib.so: phylib.o phylib_wrap.o
	$(CC) -shared phylib.o phylib_wrap.o -o _phylib.so -lm

# Optional: clean
clean:
	rm -f *.o *.so phylib_wrap.c phylib.py
