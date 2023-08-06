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