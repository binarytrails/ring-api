.PHONY: all install clean

UNAME := $(shell uname)

ifeq ($(UNAME), Darwin) 
    LIB_EXT := .dylib
else
    LIB_EXT := .so
endif

all:
	python setup.py build_ext --inplace
	python setup.py build

cython:
	python setup.py build_ext --inplace

sdist:
	python setup.py sdist # source distribution -> dist/

install:
	pip install --user -r requirements.txt
	python setup.py install --user --record files.txt

uninstall:
	pip uninstall -y -r requirements.txt
	pip uninstall -y ring_api

contrib:
	mkdir -p contrib/
	pip download -r requirements.txt -d contrib/

clean:
	python setup.py clean --all
	rm -rf dist/ build/ contrib/ ring_api.egg-info/ files.txt \
		ring_api/*$(LIB_EXT) ring_api/wrappers/*{h,.cpp}

