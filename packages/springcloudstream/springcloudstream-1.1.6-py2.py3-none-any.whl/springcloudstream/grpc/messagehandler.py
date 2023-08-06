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
Implementations of MessageHandler used by stream components.
"""
import logging
import time
from concurrent import futures

import grpc

import springcloudstream.proto.processor_pb2 as processor_pb2
import springcloudstream.proto.processor_pb2_grpc as processor_pb2_grpc
from springcloudstream.grpc.message import Message, MessageHeaders
from springcloudstream.portability import getfullargspec
from springcloudstream.component import StreamComponent

__ONE_DAY_IN_SECONDS__ = 60*60*24

FORMAT = '%(asctime)s - %(name)s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


class MessageHandler(processor_pb2_grpc.ProcessorServicer):
    """
    Message Handler for Grpc
    """

    def __init__(self, handler_function, component_type):
        """
         Translate the Protobuf Message and invoke the handler_function.
        :param handler_function: the handler function to execute for each message.
        """
        self.handler_function = handler_function
        if not component_type in StreamComponent.components:
            raise NotImplementedError("component type %s is not implemented" % component_type)

        self.component_type = component_type

    def Ping(self, request, context):
        """
        Invoke the Server health endpoint
        :param request: Empty
        :param context: the request context
        :return: Status message 'alive'
        """
        status =  processor_pb2.Status()
        status.message='alive'
        return status

    def Process(self, request, context):
        """
        Invoke the Grpc Processor, delegating to the handler_function. If the handler_function has a single argument,
        pass the Message payload. If two arguments, pass the payload and headers as positional arguments:
        handler_function(payload, headers). If the handler function return is not of type(Message), create a new Message using
        the original header values (new id and timestamp).

        :param request: the message
        :param context: the request context
        :return: response message
        """
        logger.debug(request)
        message = Message.__from_protobuf_message__(request)
        sig = getfullargspec(self.handler_function)
        if len(sig.args) == 2:
            result = self.handler_function(message.payload, message.headers)
        elif len(sig.args) == 1:
            result = self.handler_function(message.payload)
        else:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('wrong number of arguments for handler function - must be 1 or 2')
            raise RuntimeError('wrong number of arguments for handler function - must be 1 or 2')

        if self.component_type == StreamComponent.PROCESSOR:
            if type(result) == Message:
                return result.__to_protobuf_message__()
            else:
                headers = MessageHeaders()
                headers.copy(message.headers)
                return Message(result, headers).__to_protobuf_message__()




logger = logging.getLogger(__name__)

class Server:
    """
    gRPC Server
    """

    def start(self, options, handler_function, component_type):

        if options.debug:
            logger.setLevel(logging.DEBUG)

        logger.info("starting server %s" % options)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=options.thread_pool_size),maximum_concurrent_rpcs=options.max_concurrent_rpcs)
        processor_pb2.add_ProcessorServicer_to_server(MessageHandler(handler_function, component_type), server)
        host = options.host if (options.host) else '[::]'
        server.add_insecure_port('%s:%d' % (host, options.port))
        server.start()
        logger.info("server started %s" % options)

        try:
            while True:
                time.sleep(__ONE_DAY_IN_SECONDS__)
        except KeyboardInterrupt:
            server.stop(0)