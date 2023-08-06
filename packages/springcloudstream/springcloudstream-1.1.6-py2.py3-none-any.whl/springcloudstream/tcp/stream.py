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

__version__ = '1.1.0'

"""
This module contains stream components to act as the main entry point for this library. The stream components are
Processor - supports receive/send messaging
Sink - support receive only messaging
Source - supports send only messaging

Each stream component requires a handler function: 
For a Processor,  a single argument(<str>, or bytes-like) function that returns a value (<str>, or bytes-like).
For a Sink, a single argument(<str>, or bytes-like) function, the return value is ignored
For a Source, a no argument function that returns a value (<str>, or bytes-like).
"""
import codecs
import socket
from springcloudstream.options import OptionsParser
from springcloudstream.component import BaseStreamComponent
from springcloudstream.tcp.tcp import launch_server
from springcloudstream.tcp.messagehandler import *


class TCPOptionsParser(OptionsParser):
    """
    Encapsulates on OptionParser to handle options for BaseStreamComponent. Supported options include:

    -h, --help            show this help message and exit
    -p PORT, --port=PORT  the socket port to use (required)
    -m MONITOR_PORT, --monitor-port=MONITOR_PORT (strongly advised)
                        the socket to use for the monitoring server
    -s BUFFER_SIZE, --buffer-size=BUFFER_SIZE (optional, default is 2048)
                        the tcp buffer size
    -d, --debug           turn on debug logging
    -c CHAR_ENCODING, --char-encoding=CHAR_ENCODING (optional, default is 'utf-8')
                        character encoding
    -e ENCODER, --encoder=ENCODER (optional, default is 'CR')
                        The name of the encoder to use for delimiting messages
    """
    def __init__(self):
        OptionsParser.__init__(self)

        self.add_option('-p', '--port',
                               type='int',
                               help='the socket port to use',
                               dest='port')
        self.add_option('-m', '--monitor-port',
                               type='int',
                               help='the socket to use for the monitoring server',
                               dest='monitor_port')

        self.add_option('', '--host',
                               help='the hostname or IP to use for the server - default is socket.socket.gethostname()',
                               dest='host')

        self.add_option('-s', '--buffer-size',
                               help='the socket receive buffer size',
                               type='int',
                               default=2048,
                               dest='buffer_size')

        self.add_option('-d', '--debug',
                               action='store_true',
                               help='turn on debug logging',
                               default=False,
                               dest='debug')

        self.add_option('-c', '--char-encoding',
                               help='character encoding',
                               default='utf-8',
                               dest='char_encoding')

        self.add_option('-e', '--encoder',
                               type="choice",
                               choices=['LF', 'CRLF', 'STXETX', 'L4', 'L2', 'L1'],
                               help='The name of the encoder to use for delimiting messages',
                               default='LF',
                               dest='encoder')

    def validate(self,options):
        """
        Validate the options or exit()
        """
        if not options.port:
            self.parser.error("'port' is required")
        if options.port == options.monitor_port:
            self.parser.error("'port' and 'monitor-port' must not be the same.")
        if options.buffer_size <= 0:
            self.parser.error("'buffer_size' must be > 0.")
        try:
            codecs.getencoder(options.char_encoding)
        except LookupError:
            self.parser.error("invalid 'char-encoding' %s" % options.char_encoding)

        if not options.host:
           options.host = socket.gethostname()


options_parser = TCPOptionsParser()


class BaseTCPEncodingComponent:

    def __init__(self, args, options):
        """
        :param args: command line arguments (sys.argv) or valid options as a list
        """

        self.options,args = options_parser.parse(args, validate=True)

    def message_handlers(self, handler_function):
        component_type = self.__class__.component_type

        return {
                'LF': DefaultMessageHandler(handler_function, component_type, self.options.char_encoding),
                'CRLF': CrlfHandler(handler_function, component_type),
                'STXETX': StxEtxHandler(handler_function, component_type),
                'L4': HeaderLengthHandler(4, handler_function, component_type),
                'L2': HeaderLengthHandler(2, handler_function, component_type),
                'L1': HeaderLengthHandler(1, handler_function, component_type)}


class Processor(BaseTCPEncodingComponent, BaseStreamComponent):
    """Stream Processor - receives and sends messages."""
    component_type = StreamComponent.PROCESSOR

    def __init__(self, handler_function, args=[], options=None):
        """
        :param handler_function: a single argument function that returns a value
        :param args: arguments containing options
        :param options: parsed options if not None, args will be ignored
        """
        BaseTCPEncodingComponent.__init__(self, args, options)
        BaseStreamComponent.__init__(self, launch_server, self.message_handlers(handler_function), self.options)


class Sink(BaseTCPEncodingComponent, BaseStreamComponent):
    """Stream Sink - recieves messages only"""
    component_type = StreamComponent.SINK

    def __init__(self, handler_function, args=[], options=None):
        """
        :param handler_function: a single argument function that returns a value
        :param args: arguments containing options
        :param options: parsed options if not None, args will be ignored
        """
        BaseTCPEncodingComponent.__init__(self, args, options)
        BaseStreamComponent.__init__(self, launch_server, self.message_handlers(handler_function), self.options)


class Source(BaseTCPEncodingComponent, BaseStreamComponent):
    """Stream Source - sends messages from an external source """
    component_type = StreamComponent.SOURCE

    def __init__(self, handler_function, args=[], options=None):
        """
        :param handler_function: a single argument function that returns a value
        :param args: arguments containing options
        :param options: parsed options if not None, args will be ignored
        """
        BaseTCPEncodingComponent.__init__(self, args, options)
        BaseStreamComponent.__init__(self, launch_server, self.message_handlers(handler_function), self.options)