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
	python setup.py clean --all
	rm -rf ring_api/*$(LIB_EXT) ring_api/wrappers/*{h,.cpp}

