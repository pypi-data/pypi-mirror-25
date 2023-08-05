__copyright__ = '''
Copyright 2017 the original author or authors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

__author__ = 'David Turanski'

__version__ = '1.0.0'

"""
This module contains stream components to act as the main entry point for this library. The stream components are
Processor - supports receive/send messaging
Sink - support receive only messaging
Source - supports send only messaging

Each stream component requires a handler function: 
For a Processor,  a two argument( payload, header) function that returns a Message or payload
For a Sink, a two argument(payload, header) function, the return value is ignored.
For a Source, a no argument function that returns a Message or payload.
"""

import logging
import sys
from optparse import OptionParser

from springcloudstream.grpc.messagehandler import Server
from springcloudstream.component import StreamComponent

FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

logger = logging.getLogger(__name__)

class Options:
    """
    Encapsulates on OptionParser to handle options for BaseStreamComponent. Supported options include:

    -h, --help            show this help message and exit
    -p PORT, --port=PORT  the socket port to use (required)
    -d, --debug           turn on debug logging
    """
    def __init__(self, args):
        self.parser = OptionParser()

        self.parser.usage = "%prog [options] --help for help"

        self.parser.add_option('-p', '--port',
                               type='int',
                               help='the socket port to use',
                               dest='port')
        self.parser.add_option('', '--host',
                               help='the hostname or IP to use for the server - default is [::]',
                               dest='host')

        self.parser.add_option('-t', '--thread-pool-size',
                               type='int',
                               help='the thread pool size',
                               default=10,
                               dest='thread_pool_size')

        self.parser.add_option('-m', '--max-concurrent-rpcs',
                               type='int',
                               help='the max concurrent RPCs',
                               default=None,
                               dest='max_concurrent_rpcs')

        self.parser.add_option('-d', '--debug',
                               action='store_true',
                               help='turn on debug logging',
                               default=False,
                               dest='debug')

        self.options, arguments = self.parser.parse_args(args)

    def validate(self):
        """
        Validate the options or exit()
        """
        if not self.options.port:
            print("'port' is required")
            sys.exit(2)


class BaseStreamComponent:
    """
    The Base class for Stream Components.
    """
    def __init__(self, handler_function, args=[]):
        """
        :param handler_function: The function to execute on each message
        :param args: command line options or list representing as sys.argv
        """
        opts = Options(args)
        opts.validate()
        self.options = opts.options
        self.handler_function = handler_function

    def start(self):
        """
        Start the server and run forever.
        """
        Server().start(self.options,self.handler_function, self.__class__.component_type)


class Processor(BaseStreamComponent):
    """Stream Processor - receives and sends messages."""
    component_type = StreamComponent.PROCESSOR

    def __init__(self, handler_function, args=[]):
        """
        :param handler_function: a two argument function that returns a value
        :param args: See Options
        """
        BaseStreamComponent.__init__(self, handler_function, args)


class Sink(BaseStreamComponent):
    """Stream Sink - recieves messages only"""
    component_type = StreamComponent.SINK

    def __init__(self, handler_function, args=[]):
        """
        :param handler_function: a single argument function that does not return a value
        :param args: See Options
        """
        BaseStreamComponent.__init__(self, handler_function, args)


class Source(BaseStreamComponent):
    """Stream Source - sends messages from an external source """
    component_type = StreamComponent.SOURCE

    def __init__(self, handler_function, args=[]):
        """
        :param handler_function: a no argument function that returns a value (a pollable or event source)
        :param args: See Options
        """
        BaseStreamComponent.__init__(self, handler_function, args)

