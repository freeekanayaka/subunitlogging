import logging

from unittest import (
    TestSuite,
    TestResult,
)

from six import (
    b,
    StringIO,
)

from subunit.test_results import AutoTimingTestResultDecorator

from testtools import TestCase
from testtools import ExtendedToStreamDecorator
from testtools.testresult.doubles import StreamResult

from testlogging import LoggingSuite


class LoggingSuiteTest(TestCase):

    def test_subunit(self):

        suite = LoggingSuite(TestSuite())

        class DummyTest(TestCase):

            def test(self):
                logging.info("hello")

        test = DummyTest(methodName="test")
        suite.addTest(test)
        result = StreamResult()
        suite.run(
            AutoTimingTestResultDecorator(ExtendedToStreamDecorator(result)))
        event = result._events[2]
        self.assertIn("DummyTest.test", event[1])
        self.assertEqual(b("hello\n"), event[6])

    def test_unittest(self):
        stdout = StringIO()
        suite = LoggingSuite(TestSuite(), stdout=stdout)

        class DummyTest(TestCase):

            def test(self):
                logging.info("hello")

        test = DummyTest(methodName="test")
        suite.addTest(test)
        result = TestResult()
        suite.run(result)
        self.assertEqual("hello\n", stdout.getvalue())

    def test_add_tests(self):

        class DummyTest(TestCase):

            def test(self):
                logging.info("hello")

        suite = LoggingSuite([DummyTest(methodName="test")])
        result = StreamResult()
        suite.run(
            AutoTimingTestResultDecorator(ExtendedToStreamDecorator(result)))
        event = result._events[2]
        self.assertIn("DummyTest.test", event[1])
        self.assertEqual(b("hello\n"), event[6])
