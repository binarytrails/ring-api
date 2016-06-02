# Ring-cython

## Roadmap

* ~~Initialize Ring~~
* ~~Start Ring~~
* ~~Parse arguments~~
* Register Callbacks

## Getting started

### Dependecies

1. [Ring-daemon](https://gerrit-ring.savoirfairelinux.com/#/admin/projects/ring-daemon) with [this patch](https://gerrit-ring.savoirfairelinux.com/#/c/4327/) written due to bug [#699](https://tuleap.ring.cx/plugins/tracker/?aid=699) that was blocking the generation of the shared library. As soon as it is merged applying it won't be necessary.

2. Python RESTful server

        pip --user install -r requierements.txt

## Compiling 

    make

## Running

    ./client.py -h

## Contributing

### Style

[PEP 8](https://www.python.org/dev/peps/pep-0008)

## License

The code is licensed under a GNU General Public License [GPLv3](http://www.gnu.org/licenses/gpl.html).

## Authors

Seva Ivanov mail@sevaivanov.com

