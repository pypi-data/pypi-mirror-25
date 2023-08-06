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


import sys
import inspect

PYTHON3 = sys.version_info >= (3, 0)

if PYTHON3:
    long = int
    getfullargspec = inspect.getfullargspec
    def __is_str_type__(val):
        return isinstance(val,str)

    input = sys.stdin.buffer

    # nosetests reassigns sys.stdout and breaks without this check
    output =  sys.stdout if sys.stdout.__class__.__name__ == 'StringIO' else sys.stdout.buffer
else:
    long = long
    getfullargspec = inspect.getargspec
    def __is_str_type__(val):
        return isinstance(val, basestring)

    # Python 2 on Windows opens sys.stdin in text mode, and
    # binary data that read from it becomes corrupted on \r\n
    #if sys.platform == "win32":
    #    # set sys.stdin to binary mode
    #    import os, msvcrt
    #    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    input = sys.stdin
    output = sys.stdout

