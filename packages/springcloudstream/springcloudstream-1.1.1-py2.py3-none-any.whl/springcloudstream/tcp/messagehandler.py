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
from array import array
from springcloudstream.component import StreamComponent


def rindex(iterable, value):
    try:
        return len(iterable) - next(i for i, val in enumerate(reversed(iterable)) if val == value) - 1
    except StopIteration:
        raise ValueError


def split_array(lst, val):
    splits = []
    ind = 0
    l = lst
    done = False
    while not done:
        try:
            ind = l.index(val)
            if ind > 0:
                splits.append(l[:ind])
            l = l[ind+1:]
        except ValueError:
            if len(l) > 0:
                splits.append(l)
            done = True

    return splits


class MessageHandler:
    """
    Base Message Handler.
    Called by StreamHandler to encode/decode socket message and invoke the handler_function.
    """

    def __init__(self, handler_function, component_type, char_encoding='utf-8'):
        """
        :param handler_function: the handler function to execute for each message.
        """
        self.handler_function = handler_function
        self.char_encoding = char_encoding
        if not component_type in StreamComponent.components:
            raise NotImplementedError("component type %s is not implemented" % component_type)

        self.component_type = component_type


class DefaultMessageHandler(MessageHandler):
    """
    Default Message Handler for str terminated by LF ('\n')
    """

    def __init__(self, handler_function, component_type, char_encoding='utf-8'):
        MessageHandler.__init__(self, handler_function, component_type, char_encoding)
        self.TERMINATOR = '\n'

    def handle(self, request, buffer_size):
        """
        Handle a message
        :param request: the request socket.
        :param buffer_size: the buffer size.
        :return: True if success, False otherwise
        """

        if self.component_type == StreamComponent.SOURCE:
            msg = self.handler_function()
            return self.__send(request, msg)

        logger = self.logger

        data = self.__receive(request, buffer_size)
        if data is None:
            return False
        else:
            logger.debug(data.split(self.TERMINATOR))
            for message in data.split(self.TERMINATOR)[:-1]:
                logger.debug(message)
                result = self.handler_function(message)
                if self.component_type == StreamComponent.PROCESSOR:
                    if not self.__send(request, result):
                        return False
        return True

    def __receive(self, request, buffer_size):
        logger = self.logger
        buf = bytearray(buffer_size)
        received_data = bytearray()
        receive_complete = False
        data = None

        while not receive_complete:
            nbytes = request.recv_into(buf, buffer_size)
            if nbytes > 0:
                logger.debug("received %d bytes " % nbytes)
                received_data.extend(buf[:nbytes])
                receive_complete = (
                    received_data.rfind(self.TERMINATOR.encode(self.char_encoding)) == len(received_data) - len(
                        self.TERMINATOR))

                if receive_complete:
                    data = received_data.decode(self.char_encoding)
                    logger.debug('message received [%s]' % data)
            else:
                break

        return data

    def __send(self, request, msg):
        logger = self.logger

        logger.debug("sending result [%s]" % msg)

        if msg.find(self.TERMINATOR) != len(msg) - len(self.TERMINATOR):
            msg += self.TERMINATOR

        request.sendall(msg.encode(self.char_encoding))
        logger.debug("data sent %s" % msg)

        return True


class StxEtxHandler(MessageHandler):
    """
    MessageHandler using STX/ETX encoding. Each message starts with STX (0x2) and ends with ETX (0x3)
    """
    STX = 0x2
    ETX = 0x3

    def handle(self, request, buffer_size):
        """
        Handle a message
        :param request: the request socket.
        :param buffer_size: the buffer size.
        :return: True if success, False otherwise
        """
        logger = self.logger

        data = self.__receive(request, buffer_size)
        if data is None:
            return False
        else:
            arr = array('B',data)
            for message in split_array(arr,StxEtxHandler.ETX):
                if (message[0] == StxEtxHandler.STX):
                    message = message[1:]
                logger.debug(message)
                result = self.handler_function(bytearray(message))
                if self.component_type == StreamComponent.PROCESSOR:
                    if not self.__send(request, result):
                        return False
        return True

    def __receive(self, request, buffer_size):
        logger = self.logger
        buf = bytearray(buffer_size)
        received_data = bytearray()
        receive_complete = False
        data = None

        stx = bytearray(1)
        nbytes = request.recv_into(stx, 1)
        if nbytes > 0:
            if stx[0] != StxEtxHandler.STX:
                raise RuntimeError(
                    'Expecting first byte of message (%s) to be %s' % (stx[0], StxEtxHandler.STX))
            while not receive_complete:
                nbytes = request.recv_into(buf, buffer_size)
                if nbytes > 0:
                    logger.debug("received %d bytes " % nbytes)
                    received_data.extend(buf[:nbytes])
                    receive_complete = received_data[-1] == StxEtxHandler.ETX

                    if receive_complete:
                        data = received_data
                        logger.debug('message received [%s]' % received_data)
                else:
                    break

        return data

    def __send(self, request, msg):
        logger = self.logger

        logger.debug("sending result [%s]" % msg)

        result =bytearray(msg)
        result.insert(0,StxEtxHandler.STX)
        result.append(StxEtxHandler.ETX)

        request.sendall(result)
        logger.debug("data sent %s" % result)
        return True


class CrlfHandler(DefaultMessageHandler):
    """
    Message Handler for str terminated by CRLF ('\r\n')
    """

    def __init__(self, handler_function, component_type, char_encoding='utf-8'):
        DefaultMessageHandler.__init__(self, handler_function, component_type, char_encoding)
        self.TERMINATOR = '\r\n'


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
        """
        MessageHandler.__init__(self, handler_function, component_type)
        if not header_size in (1, 2, 4):
            raise RuntimeError('Invalid header_size. Valid values are 1, 2 and 4')
        self.HEADER_SIZE = header_size
        self.FORMAT = HeaderLengthHandler.FORMATS[header_size]

    def handle(self, request, buffer_size):
        """
        Handle a message
        :param request: the request socket.
        :param buffer_size: the buffer size.
        :return: True if success, False otherwise
        """
        logger = self.logger
        msg = self.__receive(request, buffer_size)
        if msg is None:
            return False

        result = self.handler_function(msg)

        if self.component_type == StreamComponent.PROCESSOR:
            return self.__send(request, result)
        return True

    def __receive(self, request, buffer_size):
        logger = self.logger
        buf = bytearray(buffer_size)
        header = bytearray(self.HEADER_SIZE)
        received_data = bytearray()
        receive_complete = False
        data = None

        while not receive_complete:
            nbytes = request.recv_into(header, self.HEADER_SIZE)
            if nbytes > 0:
                data_size = self.__data_size(header)
                remaining_bytes = data_size
                while remaining_bytes > 0:
                    nbytes = request.recv_into(buf, min(data_size, buffer_size))
                    if nbytes > 0:
                        logger.debug("received %d bytes " % nbytes)
                        received_data.extend(buf[:nbytes])
                        remaining_bytes -= nbytes

                receive_complete = True
                data = received_data
                logger.debug('message received [%s]' % data)
            else:
                break

        return data

    def __send(self, request, msg):
        logger = self.logger
        logger.debug("sending result [%s]" % msg)


        request.sendall(self.__encode(msg))
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