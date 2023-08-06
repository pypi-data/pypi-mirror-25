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
Provide support for using grpc with Spring Cloud Stream
"""
import collections
import logging
import sys
import time
import uuid
import springcloudstream.proto.message_pb2 as message_pb2
from springcloudstream.portability import long, __is_str_type__


FLOAT_MAX_VALUE = (2 - 2**-23) * 2**127
FLOAT_MIN_VALUE = 2**-149
INT_MAX_VALUE = 2**31 -1
INT_MIN_VALUE = -2**32

FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Python version %s" % str(sys.version_info) )


class MessageHeaders(collections.MutableMapping):
    """
     dict-like object to enforce Spring MessageHeaders compatibility.
    """

    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)
        self.__dict__['id'] = str(uuid.uuid4())
        self.__dict__['timestamp'] = long(round(time.time() * 1000))

    def copy(self, headers):
        for key, value in headers.items():
            if not key in ['id','timestamp']:
                self[key]=value

    # The next five methods are requirements of the ABC.
    def __setitem__(self, key, value):
        if key == 'id' or key == 'timestamp':
            raise KeyError("key '%s' cannot be updated" % key)
        __check_supported_type__(value)
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        if key == 'id' or key == 'timestamp':
            raise KeyError("key '%s' cannot be deleted" % key)
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    # The final two methods aren't required, but nice for demo purposes:
    def __str__(self):
        '''returns simple dict representation of the mapping'''
        return str(self.__dict__)

    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        return '{}, MessageHeaders({})'.format(super(MessageHeaders, self).__repr__(),
                                               self.__dict__)


class Message:
    '''
    Implementation of a Spring Message containing standard types.
    '''

    @classmethod
    def __from_protobuf_message__(cls, pb_message):
        """
        Creates a Message containing native types from a Protobuf Message containing Generic fields.
        Preserves original timestamp and id.

        :param pb_message: The Protobuf Message
        :return: a native message
        """

        headers = MessageHeaders()

        for key, value in pb_message.headers.items():
            '''Preserve timestamp and id here'''
            headers.__dict__[key] = __convert_from_generic__(value)

        return Message(__convert_from_generic__(pb_message.payload),headers)


    def __init__(self, payload, headers=MessageHeaders()):
        if payload is None:
            raise RuntimeError("'payload cannot be None.")
        __check_supported_type__(payload)

        clazz = type(MessageHeaders())
        if not type(headers) == clazz:
            raise TypeError("%s is an unsupported type for headers. Must be %s" % (type(headers), clazz))

        self.headers = headers
        self.payload = payload

    def __setattr__(self, key, value):
        if key == 'payload' or key == 'headers':
            try:
                self.__dict__[key]
                raise RuntimeError("Message is immutable")
            except KeyError:
                self.__dict__[key] = value
        else:
            raise RuntimeError("Attribute %s undefined" % value)

    def __to_protobuf_message__(self):
        pb_message = message_pb2.Message()
        __convert_to_generic__(pb_message.payload, self.payload)
        for key, value in self.headers.items():
            __convert_to_generic__(pb_message.headers[key] ,value)
        return pb_message


def __check_supported_type__(val):
    """
    Raises an Error if parameter is not a supported type (scalar, str, or bytearray).
    :param val: parameter of unknown type
    :return: None
    """
    if __is_str_type__(val):
        return True
    supported_types = [str, bool, bytes, float, int, long]
    if not supported_types.__contains__(type(val)):
        raise TypeError("%s is an unsupported type (%s)" % (type(val),val))

    return True


def __convert_to_generic__(generic, val):
    result = generic
    __check_supported_type__(val)
    if __is_str_type__(val):
        result.string = val
    elif type(val) == bytes:
        result.bytes = val
    elif type(val) == bool:
        result.bool = val
    elif type(val) == int:
        if val >= INT_MIN_VALUE and val <= INT_MAX_VALUE:
            result.int = val
        else:
            result.long = val
    elif type(val) == long:
        result.long = val
    elif type(val) == float:
        if val > FLOAT_MAX_VALUE or val < FLOAT_MIN_VALUE:
            result.double = val
        else:
            result.float = val

    return result


def __convert_from_generic__(val):
    return getattr(val, val.WhichOneof('type'))
