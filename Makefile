.PHONY: clean

UNAME := $(shell uname)

ifeq ($(UNAME), Darwin) 
    LIB_EXT := .dylib
else
    LIB_EXT := .so
endif

all:
	python setup.py build_ext --inplace

clean:
	rm -rf *$(LIB_EXT) dring.cpp *.out {*,api/*}.pyc {,api/}__pycache__/ build/

