# Ring-cython

## Roadmap

* ~~Initialize Ring~~
* ~~Start Ring~~
* ~~Parse arguments~~
* ~~Get account info~~
* Register callbacks
* Add threading
* Rewrite interfaces
* Call client from --without-dbus
* Add unitests

## Design choices

* Should the UTF-8 be decoded in dring.pxd?

## Getting started

### Dependencies

1. [Ring-daemon](https://gerrit-ring.savoirfairelinux.com/#/admin/projects/ring-daemon) with [this patch](https://gerrit-ring.savoirfairelinux.com/#/c/4327/) written due to bug [#699](https://tuleap.ring.cx/plugins/tracker/?aid=699) that was blocking the generation of the shared library. As soon as it is merged applying it won't be necessary.

2. Python RESTful server

        pip --user install -r requierements.txt

## Compiling 

    make

## Client

    $ ./client.py -h
    Usage: client.py [options] arg1 arg2

    Options:
    -h, --help        show this help message and exit
    -v, --version     show Ring-daemon version
    -d, --debug       debug mode (more verbose)
    -c, --console     log in console (instead of syslog)
    -p, --persistent  stay alive after client quits
    --auto-answer     force automatic answer to incoming call

## Real-time

    from dring import Dring

    dring = Dring()

    bitflags = (dring.FLAG_CONSOLE_LOG | dring.FLAG_DEBUG)
    dring.init_library(bitflags)

    dring.start()

    accounts = dring.config.accounts()
    dring.config.account_details(accounts[0])

## Contributing

### Style

[PEP 8](https://www.python.org/dev/peps/pep-0008)

## License

The code is licensed under a GNU General Public License [GPLv3](http://www.gnu.org/licenses/gpl.html).

## Authors

Seva Ivanov mail@sevaivanov.com

