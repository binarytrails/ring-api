# Ring API

Traditionally [Ring-daemon](https://gerrit-ring.savoirfairelinux.com/#/admin/projects/ring-daemon) was implemented using D-Bus client for communication. However, it is not present on any platform other than Gnu / Linux. Thus, the daemon *dring* has to be statistically compiled with the top layers using it. The purpose of Ring-cython is to externalize the Ring-daemon functionality to enable direct communication with its process.

## Roadmap

* ~~Initialize Ring~~
* ~~Start Ring~~
* ~~Parse arguments~~
* ~~Get account info~~
* Add threading
* Implement RESTful API skeleton
* Implement encoding / decoding protocols
* Register callbacks
* Rewrite interfaces definitions from */usr/include/dring/*:
    * account_const.h
    * call_const.h
    * callmanager_interface.h
    * configurationmanager_interface.h
    * dring.h
    * media_const.h
    * presencemanager_interface.h
    * security_const.h
    * videomanager_interface.h
* Add unitests
* Write how call client from Ring-daemon with -*-without-dbus* option
* Write "How it works?" with diagrams

## Design decisions

* Encoding / decoding

    * Should the UTF-8 be decoded in wrappers?

    * Only Json encoding or mixed?

* Callback to Javascript from RESTful API

* REST vs WebSockets

## Getting started

### Dependencies

1. Ring-daemon with [this patch](https://gerrit-ring.savoirfairelinux.com/#/c/4327/) written due to bug [#699](https://tuleap.ring.cx/plugins/tracker/?aid=699) that was blocking the generation of the shared library. As soon as it is merged, applying it won't be necessary.

    1. Download the Ring-daemon

        git clone https://gerrit-ring.savoirfairelinux.com/ring-daemon

    2. Apply the patch by going to its url, clicking on *Download* and copy-pasting the *Checkout* line in the *ring-daemon* directory. You can verify it was applied with *git log*.

    3. Build the shared library

        cd contrib; mkdir build; cd build
        ../bootstrap
        make; make .opendht
        cd ../../
        ./autogen.sh
        ./configure --prefix=/usr
        make
        make install

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

