__copyright__ = """
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
"""
__author__ = 'David Turanski'

__version__ = '1.1.0'

"""
This module supports the use TCP sockets for communication between local processes.  
"""

import sys
import logging
import threading
import os
import socket

FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    from socketserver import BaseRequestHandler, TCPServer
else:
    from SocketServer import BaseRequestHandler, TCPServer


def launch_server(message_handler, options):
    """
    Launch a message server
    :param handler_function: The handler function to execute for each message
    :param options: Application options for TCP, etc.
    """
    logger = logging.getLogger(__name__)
    if (options.debug):
        logger.setLevel(logging.DEBUG)

    if not options.monitor_port:
        logger.warn(
            "Monitoring not enabled. No monitor-port option defined.")
    else:
        threading.Thread(target=launch_monitor_server, args=(options.host, options.monitor_port, logger)).start()

    # Create the server, binding to specified host on configured port

    logger.info(
        'Starting server on host %s port %d Python version %s.%s.%s' % ((options.host, options.port) + sys.version_info[:3]))
    server = TCPServer((options.host, options.port),
                       StreamHandler.create_handler(message_handler,
                                                    options.buffer_size,
                                                    logger))

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Ctrl-C, exiting...")
        os._exit(142)


def launch_monitor_server(host, port, logger):
    """
    Launch a monitor server
    :param port: the monitor port
    :param logger: the logger
    """
    logger.info('Starting monitor server on host %s port %d' % (host, port))
    server = TCPServer((host, port), MonitorHandler)
    server.serve_forever()

class StreamHandler(BaseRequestHandler):
    """
    A RequestHandler that waits for messages over its request socket until the socket is closed
     and delegates to a MessageHandler
    """

    @classmethod
    def create_handler(cls, message_handler, buffer_size, logger):
        """
        Class variables used here since the framework creates an instance for each connection

        :param message_handler: the MessageHandler used to process each message.
        :param buffer_size: the TCP buffer size.
        :param logger: the global logger.
        :return: this class.
        """
        cls.BUFFER_SIZE = buffer_size
        cls.message_handler = message_handler
        cls.logger = logger
        cls.message_handler.logger = logger
        return cls

    def handle(self):
        """
        The required handle method.
        """
        logger = StreamHandler.logger
        logger.debug("handling requests with message handler %s " % StreamHandler.message_handler.__class__.__name__)

        message_handler = StreamHandler.message_handler

        try:
            while True:
                logger.debug('waiting for more data')
                if not message_handler.handle(self.request, StreamHandler.BUFFER_SIZE):
                    break

            logger.warning("connection closed from %s" % (self.client_address[0]))
            self.request.close()
        except:
            logger.exception("connection closed from %s" % (self.client_address[0]))
        finally:
            self.request.close()


class MonitorHandler(BaseRequestHandler):
    """Starts a monitor server to allow external processes to check the status"""

    def handle(self):
        logger = logging.getLogger(__name__)
        try:
            while True:
                data = self.request.recv(80)
                if not data:
                    break
                logger.debug('got ping request %s' % data)
                self.request.sendall('alive\n'.encode('utf-8'));

            logger.warning("monitor connection closed  %s" % (self.client_address[0]))
        except Exception:
            logger.exception("connection closed from %s" % (self.client_address[0]))
        finally:
            self.request.close()
