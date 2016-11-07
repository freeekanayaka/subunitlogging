#  testresources: extensions to python unittest to allow declaritive use
#  of resources by test cases.
#
#  Copyright (c) 2005-2010 Testresources Contributors
#
#  Licensed under either the Apache License, Version 2.0 or the BSD 3-clause
#  license at the users choice. A copy of both licenses are available in the
#  project source as Apache-2.0 and BSD. You may not use this file except in
#  compliance with one of these two licences.
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under these licenses is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
#  license you chose for the specific language governing permissions and
#  limitations under that license.

import inspect


def _get_result():
    """Find a TestResult in the stack.

    unittest hides the result. This forces us to look up the stack.
    The result is passed to a run() or a __call__ method 4 or more frames
    up: that method is what calls setUp and tearDown, and they call their
    parent setUp etc. Its not guaranteed that the parameter to run will
    be calls result as its not required to be a keyword parameter in
    TestCase. However, in practice, this works.
    """
    stack = inspect.stack()
    for frame in stack[2:]:
        if frame[3] in ('run', '__call__'):
            # Not all frames called 'run' will be unittest. It could be a
            # reactor in trial, for instance.
            result = frame[0].f_locals.get('result')
            if (result is not None and
                    getattr(result, 'startTest', None) is not None):
                return result
