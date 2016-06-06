# Ring API

Traditionally [Ring-daemon](https://gerrit-ring.savoirfairelinux.com/#/admin/projects/ring-daemon) was implemented using D-Bus client for communication. However, it is not present on any platform other than Gnu / Linux. Thus, the daemon *dring* has to be statistically compiled with the top layers using it. The purpose of Ring-cython is to externalize the Ring-daemon functionality to enable direct communication with its process.

## Why not do a C++ RESTful server?

A research of possible libraries was performed in the [ring-for-the-web](https://github.com/sevaivanov/ring-for-the-web#using-existing-libraries) repository. It turns out that there are not many possibilities. Nevertheless, Restbed seemed the most promising one, but would it be on the long run? The disadvantage of using Cython is that it takes more time to rewrite the interfaces to wrap them with Python but once it is done, the maintenance is minimal and the adjustments are made very quickly. Cython was created 8 years ago (2007) and Python in 1991. They are therefore certainly more mature than our best choices of C++ frameworks. It makes it a lot less probable that everything would go south on the internals. Fast-development opens the door to a lot of possibilities. For instance, unit and intergration tests could be implemented to test the core of the Ring project with complex User Stories in no time. Benchmarks using build-in Python timing libraries are also there. What about the flexibility? Implementing in a High-Level language wouldn't make changing a REST framework a whole new mission. It would be also possible to write custom APIs of all kinds for different requirements. Finally, Cython allows to externalize parts of code directly in C / C++ which provides strictly objectively the best of both worlds.

## Roadmap

* ~~Initialize Ring~~
* ~~Start Ring~~
* ~~Parse arguments~~
* ~~Get account info for demonstration~~
* ~~Implement RESTful API skeleton~~
* ~~Implement encoding / decoding protocols~~
* ~~Implement the Python package architecture~~
* Add threading
* Register callbacks
* Rewrite interfaces definitions from */usr/include/dring/*:
    * In Progress

            configurationmanager_interface.h    ->    configuration_manager.pxd
            dring.h                             ->    dring.pxd

    * To do

            account_const.h
            call_const.h
            callmanager_interface.h
            media_const.h
            presencemanager_interface.h
            security_const.h
            videomanager_interface.h

* Add unit tests
* Write how call client from Ring-daemon with -*-without-dbus* option
* Write "How it works?" with diagrams

## Design decisions

* Rewriting or Recycling D-Bus

* Encoding / decoding

    * Should the Unicode be decoded in the wrappers?

        Yes, to leverage the encoding / decoding steps in the API.

    * Only JSON encoding or mixed?

        For now, JSON but it can be anything.

* Callback to Javascript from RESTful API

@TODO

* REST vs WebSockets

@TODO related to previous

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

        pip --user install bottle

        # or use the freezed version
        pip --user install -r requierements.txt

## Compiling 

    cd ring_api; make; cd ../

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

    from ring_api.dring import Dring

    dring = Dring()

    bitflags = (dring.FLAG_CONSOLE_LOG | dring.FLAG_DEBUG)
    dring.init_library(bitflags) # default is silent

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

