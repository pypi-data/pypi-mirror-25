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

import os
import codecs
import time
from springcloudstream.options import OptionsParser
from springcloudstream.component import BaseStreamComponent
from springcloudstream.stdio.messagehandler import *
import logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logger = logging.getLogger(__name__)

class StdioOptionsParser(OptionsParser):
    """
    Encapsulates on OptionParser to handle options for BaseStreamComponent. Supported options include:

    -h, --help            show this help message and exit

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

       # self.add_option('-s', '--buffer-size',
       #                 help='the tcp buffer size',
       #                 type='int',
       #                 default=2048,
       #                 dest='buffer_size')

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

        self.add_option('-d', '--debug',
                        action='store_true',
                        help='turn on debug logging',
                        default=False,
                        dest='debug')

    def validate(self, options):
        """
        Validate the options or exit()
        """
        #if options.buffer_size <= 0:
        #    self.parser.error("'buffer_size' must be > 0.")
        try:
            codecs.getencoder(options.char_encoding)
        except LookupError:
            self.parser.error("invalid 'char-encoding' %s" % options.char_encoding)

options_parser = StdioOptionsParser()

def launch_server(message_handler, options):
    """
    Launch a message server
    :param handler_function: The handler function to execute for each message
    :param options: Application options for TCP, etc.
    """
    logger = logging.getLogger(__name__)
 #   if (options.debug):
 #       logger.setLevel(logging.DEBUG)

#    if not options.monitor_port:
#        logger.warning(
#            "Monitoring not enabled. No monitor-port option defined.")
#    else:
#        threading.Thread(target=launch_monitor_server, args=(options.host, options.monitor_port, logger)).start()

    # Create the server, binding to specified host on configured port

#   logger.info(
#        'Starting server on host %s port %d Python version %s.%s.%s' % ((options.host, options.port) + sys.version_info[:3]))
#    server = ThreadedTCPServer((options.host, options.port),

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        while True:
            logger.debug('waiting for more data')
            if not message_handler.handle():
                break
        logger.warning("I/O stream closed from client")

    except KeyboardInterrupt:
        logger.info("I/O stream closed from client exiting...")
        os._exit(142)

    except:
        logger.exception("Error encountered handling message")


class BaseIOEncodingComponent:

    def __init__(self, args, options):
        """
        :param args: command line arguments (sys.argv) or valid options as a list
        """
        self.options,args = options_parser.parse(args, validate=True)
        if self.options.debug:
            logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename="debug-%d.log" % int(time.time()))

    def message_handlers(self, handler_function):
        component_type = self.__class__.component_type

        return {
                'LF': DefaultMessageHandler(handler_function, component_type, self.options.char_encoding),
                'CRLF': CrlfHandler(handler_function, component_type, self.options.char_encoding),
                'STXETX': StxEtxHandler(handler_function, component_type),
                'L4': HeaderLengthHandler(4, handler_function, component_type),
                'L2': HeaderLengthHandler(2, handler_function, component_type),
                'L1': HeaderLengthHandler(1, handler_function, component_type)}


class Processor(BaseIOEncodingComponent, BaseStreamComponent):
    """Stream Processor - receives and sends messages."""
    component_type = StreamComponent.PROCESSOR

    def __init__(self, handler_function, args=[], options=None):
        """
        :param handler_function: a single argument function that returns a value
        :param args: arguments containing options
        :param options: parsed options if not None, args will be ignored
        """
        BaseIOEncodingComponent.__init__(self, args, options)
        BaseStreamComponent.__init__(self, launch_server, self.message_handlers(handler_function), self.options)


class Sink(BaseIOEncodingComponent, BaseStreamComponent):
    """Stream Sink - recieves messages only"""
    component_type = StreamComponent.SINK

    def __init__(self, handler_function, args=[], options=None):
        """
        :param handler_function: a single argument function that returns a value
        :param args: arguments containing options
        :param options: parsed options if not None, args will be ignored
        """
        BaseIOEncodingComponent.__init__(self, args, options)
        BaseStreamComponent.__init__(self, launch_server, self.message_handlers(handler_function), self.options)


class Source(BaseIOEncodingComponent, BaseStreamComponent):
    """Stream Source - sends messages from an external source """
    component_type = StreamComponent.SOURCE

    def __init__(self, handler_function, args=[], options=None):
        """
        :param handler_function: a single argument function that returns a value
        :param args: arguments containing options
        :param options: parsed options if not None, args will be ignored
        """
        BaseIOEncodingComponent.__init__(self, args, options)
        BaseStreamComponent.__init__(self, launch_server, self.message_handlers(handler_function), self.options)