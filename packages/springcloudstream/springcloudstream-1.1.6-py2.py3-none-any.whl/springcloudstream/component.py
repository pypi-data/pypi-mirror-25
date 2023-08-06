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

from springcloudstream.encoders import Encoders
from optparse import OptionParser

class StreamComponent:
    components = range(3)
    PROCESSOR, SINK, SOURCE = components


class BaseStreamComponent:
    """
    The Base class for Stream Components.
    """
    def __init__(self, launch_server_function, message_handlers, options):
        """
        :param handler_function: The function to execute on each message
        :param message_handlers: a dictionary of MessageHandler keyed by encoder
        :param opts: command line options or list
        """

        self.options = options
        self.launch_server = launch_server_function
        self.message_handler = self.get_message_handler(message_handlers)

    def start(self):
        """
        Start the server and run forever.
        """
        self.launch_server(self.message_handler, self.options)

    def get_message_handler(self, message_handlers):
        """
        Create a MessageHandler for the configured Encoder
        :param message_handlers: a dictionart of MessageHandler keyed by encoder
        :return: a MessageHandler
        """
        encoder = self.options.encoder
        try:
            return message_handlers[encoder]
        except KeyError:
            raise NotImplementedError('No RequestHandler defined for given encoder (%s).' % encoder)


class MessageHandler:
    """
    Base Message Handler.
    Called by StreamHandler to encode/decode messages and invoke the handler_function.
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