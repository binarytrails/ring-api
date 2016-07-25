# Ring API

The documentation is located in the [Wiki](https://github.com/sevaivanov/ring-api/wiki).

Status: Ongoing Refactoring ~~Tested and stable at [f8cd8fa](https://github.com/sevaivanov/ring-api/commit/f8cd8fabc9ed2973fe4ca9935b423012e56c70bf).~~

## Roadmap

* ~~Initialize Ring~~
* ~~Start Ring~~
* ~~Parse arguments~~
* ~~Get account info for demonstration~~
* ~~Implement RESTful API skeleton~~
* ~~Implement encoding / decoding protocols~~
* ~~Implement the Python package architecture~~
* ~~Add threading~~
* ~~Register callbacks~~
* ~~Define python callbacks API~~
* Segment wrappers into multiple files
* ~~Decide whether to use REST + WebSockets or only WebSockets~~
* ~~Select multi-threaded RESTful server~~
* ~~Define RESTful API standards~~
* ~~Define RESTful API in json~~
* ~~Implement RESTful API using Flask-REST~~
* ~~Implement WebSockets structure for server initiated callbacks~~
* ~~Write a wiki base~~
* Wiki: write how it works with and draw a diagram
* Wiki: document the server and WebSockets software choices
* Add unit tests
* Add integration tests
* Integrate the project to Ring-daemon Autotools (GNU Build System) using the *--without-dbus* option

    See: *Learning Cython Programming* by Philip Herron, page 32.

* Implement the functionalities:

    **It considered done when it's implement in both Cython and the RESTful server.**

    - ~~possibility to talk to the REST http interface of the daemon (the framework that you've written so far)~~
    - ~~control the "static" configuration of the daemon: add/remove an account, modify properties, enable/disable them~~
    - ~~be able to listen to the changes from the daemon (framework for signals)~~
    - execute dynamic features:
      - ~~receive a message text (IM) out-of-call~~
      - ~~send an IM out-of-call~~
      - be able to accept/refuse an incoming call
      - be able to display the status of a call and stop a call
      - tx/rx IM in-call
      - ~~display video, in-call and preview for camera setup (audio is fully controlled by the daemon)~~
      - add full call controls (media pause, transfer, audio controls, conferences, ...)
      - add full "smartInfo" features
      - ~~certificates controls~~

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

        pip install --user -r requirements.txt

3. Cython shared library

Install Cython and generate the ring_api library:

    cd ring_api; make; cd ../

### Running

There are two ways to interact with the Ring-daemon using the API. In both cases, you are using the client. You can either run a **Client script** located at project root called *client.py* that instantiates the Client class located in *ring_api/client.py* or import the *ring_api/client.py* in **Interpreter** mode to a Python interpreter (for example into [IPython](http://ipython.org/)).

#### Client script

It is recommended that you start it with the *--rest* option to be able to interact with it.

    $ ./client.py -h
    Usage: client.py [options] arg1 arg2

    Options:
      -h, --help         show this help message and exit
      -v, --verbose      activate all of the verbose options
      -d, --debug        debug mode (more verbose)
      -c, --console      log in console (instead of syslog)
      -p, --persistent   stay alive after client quits
      -r, --rest         start with restful server api
      --port=HTTP_PORT   server http port for rest
      --ws-port=WS_PORT  server websocket port for callbacks
      --host=HOST        restful server host
      --auto-answer      force automatic answer to incoming call
      --dring-version    show Ring-daemon version
      --interpreter      adapt threads for interpreter interaction

##### Examples

Start the backend using client in verbose and with REST server:

    ./client.py -rv

###### Send a text message using cURL

1. Get the available accounts

        curl http://127.0.0.1:8080/accounts/

2. To get the destination Ring Id, just text the server's Ring Id and copy-paste it from the console's output.

3. Send an account message:

    The data is in JSON string format.

        curl -X POST -d '{"ring_id":"<ring_id>","message":"curling","mime_type":"text/plain"}' http://127.0.0.1:8080/accounts/<account_id>/message/

4. Get the message status:

        curl http://127.0.0.1:8080/message/<message_id>/

#### Interpreter

It was tested using IPython. **It wasn't designed to be run with the REST Server.**

    from ring_api import client

    # Options
    (options, args) = client.options()
    options.verbose = True
    options.interpreter = True

    # initialize the client
    ring = client.Client(options)

    # Callbacks
    cbs = ring.dring.callbacks_to_register()

    # i.e. define a simple callback
    from ring_api.callbacks import cb_api

    def on_text(account_id, from_ring_id, content):
        print(account_id, from_ring_id, content)

    # i.e. register this callback
    cbs['account_message'] = on_text
    ring.dring.register_callbacks(cbs)

    ring.start()

    # i.e. interogate the daemon
    account = ring.dring.config.accounts()[0]
    details = ring.dring.config.account_details(account)

    # i.e. send a text message
    ring.dring.config.send_account_message(
        account, '<to_ring_id>', {'text/plain': 'hello'})

    # Extra

    # show accessible content
    dir(client)
    dir(cb_api)

    # show documentation of some method
    help(ring.dring.config.account_details)

    # show callbacks documentation
    help(cb_api.account_message)

#### Ring Node

At the moment, the Node has an EchoBot which stores and forwards the account messages using a bot-like *!bang* syntax. It is important to understand that this Node never leaves the Ring over OpenDHT network.

    $ ./node.py -h
    usage: node.py [-h] [-v] -c CLIENTS

    Ring API node using bots

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose
      -c CLIENTS, --clients CLIENTS
                            Clients as JSON string of '{"alias": "ring_id"}'

The advantage of using aliases as secrets associated with your Ring Ids is that it very simple to remember and write. The requester will get all of the messages from all contacts which makes it simple to pull everything associated with your slave machine Ring Id at once.

1. Start the node using the Ring API on your slave machine which will act as a replier.

        ./node.py -vc '{"roger":"<ring_id>"}'

2. From any other device -- text your slave machine which will enqueue messages.

    From a third or same as previous (i.e. cellphone) device -- text the slave machine to forward all of the messages to the 'Ring Id' associated with 'roger' alias:

        !echo roger reply

    The slave machine will display that:

        [Ring node is listening]
        [Received    ] '!echo roger reply' : rerouting all messages to '<ring_id>'
        [Forwarding  ] '[2016-07-23 13:39:40.351862 : <ring_id>] : Did you know'
        [Forwarding  ] '[2016-07-23 13:39:42.346681 : <ring_id>] : that I like ..'
        [Forwarding  ] '[2016-07-23 13:39:44.717613 : <ring_id>] : waffles?'

    The device from which you requested it will display the messages in order under this form:

        [<date time> : <ring_id_dest>] : <message>

This a quick practical example. The exhaustive documentation is comming soon.

## Contributing

### Style

Coding: [PEP 8](https://www.python.org/dev/peps/pep-0008/)

Docstring: [PEP 257](https://www.python.org/dev/peps/pep-0257/)

## License

The code is licensed under a GNU General Public License [GPLv3](http://www.gnu.org/licenses/gpl.html).

## Authors

Seva Ivanov seva.ivanov@savoirfairelinux.com

Simon Zeni  simon.zeni@savoirfairelinux.com
