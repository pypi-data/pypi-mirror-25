# Pubkeeper Python Client

The Pubkeeper Python Client enables you to connect to a Pubkeeper Server instance, and to participate in the production and subscription of data topics.

## Quick Start

### Install From Wheels
#### Acquire

Since pubkeeper source is currently closed to a small subset of individuals, the quickest way to install Pubkeeper Python Client is from a set of wheel files.  Wheels are located in s3 under the Pubkeeper bucket.  For Pubkeeper Python Client you will need at least four wheels `pubkeeper-protocol`, `pubkeeper-communication`, `pubkeeper-communication-websocket`, and `pubkeeper-client` are all required.  The individual brew wheels are the pieces that enable the communication over a given protocol.  The three currently supported, and available, wheels are `pubkeeper-brew-zmq`, `pubkeeper-brew-websocket`, and `pubkeeper-brew-local`.

#### Install

Into your environment install the wheel files together:

```
pip install pubkeeper-protocol*.whl pubkeeper-comunication*.whl pubkeeper-client*.whl pubkeeper-brew*.whl
```

### Install From Source
#### Clone the repo

If you have access to the Pubkeeper project you may install directly from source for development purposes.

```
git clone git@github.com:pubkeeper/python-client
```

#### Install

Ensure the protocol, and communicaiton wheels are installed into your environment before installing the Pubkeeper Python Client and Brews.  Then you can install Pubkeeper Python Client and Brews into your own virtualenv.

```
pip3 install -e /path/to/where/you/cloned/python-client
```

### Using the Pubkeeper Python Client
#### Authentication Tokens

Pubkeeper Server handles client authentication with JWT.  As such you will need to acquire a token from the server you are going to be connecting to.

#### Running

In the most basic example, we will connect to the Pubkeeper Server, and register a single Brewer and publish a string.  Note that the client sits upon a Tornado IOLoop, as such it runs inside of its own thread, and will need to be gracefilly shutdown when your program ends.  This example assumes you are running an unsecured Pubkeeper Server, and Websocket Server on your localhost.  You will need to replace these with actual values.

```py
from pubkeeper.client import PubkeeperClient
from pubkeeper.brewer import Brewer
from pubkeeper.communication.websocket import WebsocketClientCommunication
from pubkeeper.brew.websocket.brew import WebsocketBrew
from time import sleep

server_comm = WebsocketClientCommunication({
    'host': 'localhost',
    'port': 9898,
    'secure': False
})
client = PubkeeperClient(jwt='your-auth-token', server_comm=server_comm)

websocket_brew = WebsocketBrew()
websocket_brew.configure({
    'ws_host': 'localhost',
    'ws_port': 8000,
    'ws_secure': False
})

client.add_brew(websocket_brew)
client.start_brews()

try:
    brewer = Brewer('demo.topic')
    client.add_brewer(brewer)

    while True:
        brewer.brew(b'data')
        time.sleep(1)
except KeyboardInterrupt:
    client.shutdown()
```

## Complete Documentation

A more complete documentation of the Pubkeeper Python Client, and Pubkeeper System may be found at: [docs.pubkeeper.com](http://docs.pubkeeper.com)


