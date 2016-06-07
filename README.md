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
* ~~Add threading~~
* Make bottle WSGIRefServer
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
* Write a Wiki

## Design decisions

* Threading: who controls who?

    Main while loop in Client class start() function using dring.poll_events()

* Rewriting or Recycling D-Bus

* Encoding / decoding

    * Should the Unicode be decoded in the wrappers?

        Yes, to leverage the encoding / decoding steps in the API.

    * Only JSON encoding or mixed?

        For now, JSON but it can be anything.

* Callback to Javascript from RESTful API

* REST vs WebSockets

## Getting started

### Installation

#### Dependencies

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

#### Compiling

    cd ring_api; make; cd ../

### Running

There are two ways to interact with the Ring-daemon using the API. In both cases, you are using the client. You can either run a **Client script** located at project root called *client.py* that instantiates the Client class located in *ring_api/client.py* or import the *ring_api/client.py* in **Real-time** in a Python interpreter for example into [IPython](http://ipython.org/).

#### Client script

It is recommended that you start it with the *--rest* option to be able to interact with it.

    $ ./client.py -h
    Usage: client.py [options] arg1 arg2

    Options:
      -h, --help        show this help message and exit
      -v, --verbose     activate all of the verbose options
      -d, --debug       debug mode (more verbose)
      -c, --console     log in console (instead of syslog)
      -p, --persistent  stay alive after client quits
      -r, --rest        start with restful server api
      --port=PORT       restful server port
      --host=HOST       restful server host
      --auto-answer     force automatic answer to incoming call
      --dring-version   show Ring-daemon version
      --realtime        adapt threads for real-time interaction

##### Examples

    ./client.py -rv

List all of the API routes at http://127.0.0.1:8080/all_routes/.

###### Send a text message

In another terminal you can send a text message:

    curl -X POST http://127.0.0.1:8080/user/send/text/<account_id>/<to_ring_id>/<message>/

#### Real-time

It was tested using IPython.

    from ring_api import client

    (options, args) = client.options()
    options.verbose = True

    ring = client.Client(options)
    ring.start()

    account = ring.dring.config.accounts()[0]
    details = ring.dring.config.account_details(account)

    ring.dring.config.send_text_message(
        account, '<to_ring_id>', {'text/plain': 'hello'})

    # show accessible content
    dir(client)

    # show docstring of the method
    help(ring.dring.config.account_details)

## Contributing

### Style

Coding: [PEP 8](https://www.python.org/dev/peps/pep-0008/)

Docstring: [PEP 257](https://www.python.org/dev/peps/pep-0257/)

## License

The code is licensed under a GNU General Public License [GPLv3](http://www.gnu.org/licenses/gpl.html).

## Authors

Seva Ivanov mail@sevaivanov.com

