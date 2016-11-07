from unittest import TestSuite

from testtools import ExtendedToOriginalDecorator


from fixtures import LogHandler

from subunitlogging import SubunitHandler


class SubunitLoggingSuite(TestSuite):

    def __init__(self, tests, name="", level=None):
        super(SubunitLoggingSuite, self).__init__(tests)
        self.handler = SubunitHandler()
        self._fixture = LogHandler(self.handler, name=name, level=level)

    def run(self, result):
        self._fixture.setUp()
        result = _SubunitLoggingConfigurator(result, self.handler)
        try:
            super(SubunitLoggingSuite, self).run(result)
        finally:
            self._fixture.cleanUp()


class _SubunitLoggingConfigurator(ExtendedToOriginalDecorator):

    def __init__(self, result, handler):
        super(_SubunitLoggingConfigurator, self).__init__(result)
        self._handler = handler
        self._handler.setResult(self)

    def startTest(self, test):
        super(_SubunitLoggingConfigurator, self).startTest(test)
        self._handler.setTestId(test.id())

    def stopTest(self, test):
        super(_SubunitLoggingConfigurator, self).stopTest(test)
        self._handler.setTestId(None)
