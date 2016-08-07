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
	python setup.py clean
	rm -rf *$(LIB_EXT) *.out ring_api/wrappers/*{h,.cpp}

