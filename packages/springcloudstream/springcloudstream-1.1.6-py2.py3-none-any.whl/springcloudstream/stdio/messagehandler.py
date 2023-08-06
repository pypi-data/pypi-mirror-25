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
Implementations of MessageHandler used by stream components.
"""

import struct
import logging
from array import array
from springcloudstream.component import StreamComponent, MessageHandler
from springcloudstream.portability import input, output, PYTHON3

if PYTHON3:
    from functools import reduce


    def getc():
        c, = input.read(1)
        return c


    def write_buffer(buf, encoding='utf-8'):
        if type(buf) == str:
            output.write(bytes(buf, encoding))
        else:
            output.write(buf)

else:
    def getc():
        c = input.read(1)
        if c:
            return ord(c)
        return None


    def write_buffer(buf, encoding='utf-8'):
        if type(buf) == str:
            output.write(unicode(str, encoding))
        else:
            output.write(buf)


class DefaultMessageHandler(MessageHandler):
    """
    Default Message Handler for str terminated by LF ('\n')
    """

    def __init__(self, handler_function, component_type, char_encoding='utf-8'):
        """
        :param handler_function: the handler function to execute for each message
        :param component_type: Processor, Sink, or Source
        """
        MessageHandler.__init__(self, handler_function, component_type, char_encoding)
        self.TERMINATOR = '\n'
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle(self):
        """
        Handle a message
        :return: True if success, False otherwise
        """

        if self.component_type == StreamComponent.SOURCE:
            msg = self.handler_function()
            return self.__send(msg)

        logger = self.logger
        data = self.__receive()
        if data is None:
            return False
        else:
            logger.debug("Calling %s " % self.handler_function)
            result = self.handler_function(data.decode(self.char_encoding))
            if self.component_type == StreamComponent.PROCESSOR:
                logger.debug("Sending p3:%s %s %s" % (PYTHON3, result, str(type(result))))
                if not self.__send(result):
                    return False
        return True

    def __receive(self):
        buf = bytearray()
        data = None
        while not data:
            c = getc()
            self.logger.debug("%d %s" % (c, str(type(c))))
            buf.append(c)

            if self.terminated(buf):
                self.logger.debug("message received %s %s" % (buf, array('B', buf)))
                data = self.decode(buf);

        return data

    def __send(self, msg):
        logger = self.logger
        msg = self.encode(msg)
        write_buffer(msg, self.char_encoding)

        logger.debug("message sent %s" % (msg))
        return True

    def terminated(self, buf):
        return chr(buf[-1]) == self.TERMINATOR

    def decode(self, buf):
        return buf[:-len(self.TERMINATOR)]

    def encode(self, msg):
        if msg[-len(self.TERMINATOR)] != self.TERMINATOR:
            msg += self.TERMINATOR
        return msg


class CrlfHandler(DefaultMessageHandler):
    """
    Message Handler for str terminated by CRLF ('\r\n')
    """

    def __init__(self, handler_function, component_type, char_encoding):
        """
        :param handler_function: the handler function to execute for each message
        :param component_type: Processor, Sink, or Source
        """
        MessageHandler.__init__(self, handler_function, component_type, char_encoding)
        self.TERMINATOR = '\r\n'
        self.logger = logging.getLogger(self.__class__.__name__)

    def terminated(self, buf):
        return reduce(lambda x, y: x + y, map(chr, list(buf[-len(self.TERMINATOR):]))) == self.TERMINATOR

    def decode(self, buf):
        return buf[:-len(self.TERMINATOR)]

    def encode(self, msg):
        if msg[-len(self.TERMINATOR)] != self.TERMINATOR:
            msg += self.TERMINATOR
        return msg


class StxEtxHandler(MessageHandler):
    """
    MessageHandler that encodes/decodes messages starting with STX(0x2) and ending with ETX(0x3)
    """
    ETX = 0x3
    STX = 0x2

    def __init__(self, handler_function, component_type):
        """
        :param header_size: the size of the message length header in bytes (1,2, or 4)
        :param handler_function: the handler function to execute for each message
        :param component_type: Processor, Sink, or Source
        """
        MessageHandler.__init__(self, handler_function, component_type)
        self.logger = logging.getLogger(self.__class__.__name__)

    def handle(self):
        """
        Handle a message starting with STX(0x2) and ending with ETX(0x3)
        :return: True if success, False otherwise
        """

        if self.component_type == StreamComponent.SOURCE:
            msg = self.handler_function()
            return self.__send(msg)

        logger = self.logger
        data = self.__receive()
        if data is None:
            return False
        else:
            #           for message in data.split(self.TERMINATOR)[:-1]:
            #               logger.debug(message)
            logger.debug("Calling %s " % self.handler_function)
            result = self.handler_function(data)
            if self.component_type == StreamComponent.PROCESSOR:
                logger.debug("Sending %s %s" % (result, str(type(result))))
                if not self.__send(result):
                    return False
        return True

    def __receive(self):
        data = None
        buf = bytearray()
        while not data:
            c = getc()
            if len(buf) == 0 and c != self.STX:
                raise RuntimeError(
                    'Expecting first byte of message (%d) to be %d' % (c, StxEtxHandler.STX))

            buf.append(c)
            if self.terminated(buf):
                self.logger.debug("message received %s %s" % (buf, array('B', buf)))
                data = self.decode(buf);
        return data

    def __send(self, msg):
        logger = self.logger
        msg = self.encode(msg)
        self.logger.debug("sending result p3: %s %s" % (PYTHON3, array('B', msg)))
        write_buffer(msg)
        logger.debug("message sent")
        return True

    def terminated(self, buf):
        return buf[-1] == self.ETX

    def decode(self, buf):
        return buf[1:-1]

    def encode(self, buf):
        if type(buf) != bytearray and type(buf) != bytes:
            raise TypeError('Expecting bytes-like object %s' % type(buf))
        result = bytearray(buf)
        result.insert(0, StxEtxHandler.STX)
        result.append(StxEtxHandler.ETX)
        return result


class HeaderLengthHandler(MessageHandler):
    def __init__(self, length, handler_function, component_type):
        MessageHandler.__init__(self, handler_function, component_type)
        self.logger = logging.getLogger(self.__class__.__name__)


class HeaderLengthHandler(MessageHandler):
    """
    MessageHandler that encodes/decodes using a message length header.
    """
    LONG = '!l'
    SHORT = '!H'
    BYTE = 'B'
    FORMATS = {4: LONG, 2: SHORT, 1: BYTE}

    def __init__(self, header_size, handler_function, component_type):
        """
        :param header_size: the size of the message length header in bytes (1,2, or 4)
        :param handler_function: the handler function to execute for each message
        :param component_type: Processor, Sink, or Source
        """
        MessageHandler.__init__(self, handler_function, component_type)
        self.logger = logging.getLogger(self.__class__.__name__)
        if not header_size in (1, 2, 4):
            raise RuntimeError('Invalid header_size. Valid values are 1, 2 and 4')
        self.HEADER_SIZE = header_size
        self.FORMAT = HeaderLengthHandler.FORMATS[header_size]

    def handle(self):
        """
        Handle a message
        :return: True if success, False otherwise
        """
        logger = self.logger
        msg = self.__receive()
        if msg is None:
            return False

        result = self.handler_function(msg)

        if self.component_type == StreamComponent.PROCESSOR:
            return self.__send(result)
        return True

    def __receive(self):
        logger = self.logger
        buf = bytearray()

        c = input.read(self.HEADER_SIZE)

        data_size = self.__data_size(c)
        logger.debug("data_size %d" % data_size)
        if data_size <= 0:
            logger.error("invalid data size.")
            return None

        for _ in range(data_size):
            c = getc()
            buf.append(c)
        logger.debug("returning %s" % buf)
        return buf

    def __send(self, msg):
        logger = self.logger
        logger.debug("sending result [%s]" % msg)
        write_buffer(self.__encode(msg))
        logger.debug("data sent")

        return True

    def __encode(self, data):
        ba = bytearray(struct.pack(self.FORMAT, len(data)))
        ba.extend(data)
        return ba

    def __data_size(self, header):
        data_size = struct.unpack(self.FORMAT, header)[0]
        if self.FORMAT == HeaderLengthHandler.BYTE:
            data_size = ord(header)
        return data_size
