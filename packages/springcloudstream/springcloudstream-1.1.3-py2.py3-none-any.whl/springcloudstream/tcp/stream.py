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

import sys
from optparse import OptionParser
import codecs
import socket
from springcloudstream.component import StreamComponent


from springcloudstream.tcp.tcp import launch_server
from springcloudstream.tcp.messagehandler import *

class Encoders:
    """Named identifiers to determine which RequestHandler to use.
       CRLF - messages are terminated by '\r\n'
       LF - The default - messages are terminated by '\n'
       L4 - Messages include a 4 byte header containing the length of the message (max length = 2**31 - 1)
       L2 - Messages include a 2 byte unsigned short header containing the length of the message (max length = 2**16)
       L1 - Messages include a 1 byte header containing the length of the message (max length = 255)
       STXETX - Messages begin with stx '0x2' and end with etx '0x3'
    """
    CRLF, LF, STXETX, L4, L2, L1 = range(6)

    @classmethod
    def value(cls, name):
        return cls.__dict__[name]

class Options:
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
    def __init__(self, args):
        self.parser = OptionParser()

        self.parser.usage = "%prog [options] --help for help"

        self.parser.add_option('-p', '--port',
                               type='int',
                               help='the socket port to use',
                               dest='port')
        self.parser.add_option('-m', '--monitor-port',
                               type='int',
                               help='the socket to use for the monitoring server',
                               dest='monitor_port')

        self.parser.add_option('', '--host',
                               help='the hostname or IP to use for the server - default is socket.socket.gethostname()',
                               dest='host')

        self.parser.add_option('-s', '--buffer-size',
                               help='the tcp buffer size',
                               type='int',
                               default=2048,
                               dest='buffer_size')

        self.parser.add_option('-d', '--debug',
                               action='store_true',
                               help='turn on debug logging',
                               default=False,
                               dest='debug')

        self.parser.add_option('-c', '--char-encoding',
                               help='character encoding',
                               default='utf-8',
                               dest='char_encoding')

        self.parser.add_option('-e', '--encoder',
                               type="choice",
                               choices=['LF', 'CRLF', 'STXETX', 'L4', 'L2', 'L1'],
                               help='The name of the encoder to use for delimiting messages',
                               default='LF',
                               dest='encoder')

        self.options, arguments = self.parser.parse_args(args)

    def validate(self):
        """
        Validate the options or exit()
        """
        if not self.options.port:
            print("'port' is required")
            sys.exit(2)
        if self.options.port == self.options.monitor_port:
            print("'port' and 'monitor-port' must not be the same.")
            sys.exit(2)
        if self.options.buffer_size <= 0:
            print("'buffer_size' must be > 0.")
            sys.exit(2)
        try:
            codecs.getencoder(self.options.char_encoding)
        except LookupError:
            print("invalid 'char-encoding' %s" % self.options.char_encoding)
            sys.exit(2)

        if not self.options.host:
           self.options.host = socket.gethostname()


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
        self.message_handler = self.create_message_handler(handler_function)

    def start(self):
        """
        Start the server and run forever.
        """
        launch_server(self.message_handler, self.options)

    def create_message_handler(self,handler_function):
        """
        Create a MessageHandler for the configured Encoder
        :param handler_function: The function to execute on each message
        :return: a MessageHandler
        """
        encoder = Encoders.value(self.options.encoder)
        component_type = self.__class__.component_type
        if encoder == None or encoder == Encoders.LF:
            return DefaultMessageHandler(handler_function, component_type, self.options.char_encoding)
        elif encoder == Encoders.STXETX:
            return StxEtxHandler(handler_function, component_type)
        elif encoder == Encoders.CRLF:
            return CrlfHandler(handler_function, component_type)
        elif encoder == Encoders.L4:
            return HeaderLengthHandler(4, handler_function, component_type)
        elif encoder == Encoders.L2:
            return HeaderLengthHandler(2, handler_function, component_type)
        elif encoder == Encoders.L1:
            return HeaderLengthHandler(1, handler_function, component_type)
        else:
            raise NotImplementedError('No RequestHandler defined for given encoder (%s).' % self.options.encoder)



class Processor(BaseStreamComponent):
    """Stream Processor - receives and sends messages."""
    component_type = StreamComponent.PROCESSOR

    def __init__(self, handler_function, args=[]):
        """
        :param handler_function: a single argument function that returns a value
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
