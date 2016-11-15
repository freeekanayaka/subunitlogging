import sys

from unittest import TestSuite

from logging import (
    DEBUG,
    StreamHandler,
)
from logging.handlers import MemoryHandler

from extras import safe_hasattr

from fixtures import LogHandler

from subunit.test_results import AutoTimingTestResultDecorator

from testlogging import SubunitHandler
from testlogging.result import ExtendedToSubunitHandlerDecorator


class LoggingSuite(TestSuite):

    def __init__(self, tests, name="", level=DEBUG, stdout=sys.stdout):
        super(LoggingSuite, self).__init__()
        self.handler = MemoryHandler(1)
        self._fixture = LogHandler(self.handler, name=name, level=level)
        self._stdout = stdout

        # Euristically figure out if we're being passed a single test/suite
        # or a list of tests. In particular, in case of a single suite we
        # don't want addTests() to unwrap it by iterating through its tests,
        # since that would prevent its run() method from being run and by-pass
        # possible custom logic (e.g. testresources.OptimisingTestSuite).
        if safe_hasattr(tests, "run"):
            add = self.addTest
        else:
            add = self.addTests
        add(tests)

    def run(self, result):
        self.handler.target, result = self._get_target_handler(result)
        self._fixture.setUp()
        try:
            super(LoggingSuite, self).run(result)
        finally:
            self._fixture.cleanUp()

    def _get_target_handler(self, result):
        if isinstance(result, AutoTimingTestResultDecorator):
            target = SubunitHandler()
            result = ExtendedToSubunitHandlerDecorator(result, target)
        else:
            target = StreamHandler(self._stdout)
        return target, result
