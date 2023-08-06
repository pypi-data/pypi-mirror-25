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

import optparse
class OptionsParser:
    """
    Encapsulates on OptionParser to handle command line options.
    """
    def __init__(self):
        self.parser = optparse.OptionParser()
        self.parser.usage = "%prog [options] --help for help"

    def add_option(self,*args, **kwargs):
        return self.parser.add_option(*args, **kwargs)

    def parse(self,args,validate=False):
        opts,args =  self.parser.parse_args(args)
        validate and self.validate(opts)
        return opts,args

    def validate(self,options):
        pass

