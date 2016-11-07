from logging import (
    Logger,
    INFO,
)

from unittest import TestResult

from testtools import TestCase
from testtools import ExtendedToStreamDecorator
from testtools.testresult.doubles import StreamResult

from systemfixtures import FakeTime

from subunit.test_results import AutoTimingTestResultDecorator

from subunitlogging import SubunitHandler


class SubunitHandlerTest(TestCase):

    def test_logging(self):
        """Tests can add log records to the subunit stream."""
        fixture = self.useFixture(FakeTime())
        fixture.set(seconds=1478383023.22)

        logger = Logger("test")
        logger.addHandler(SubunitHandler())
        logger.setLevel(INFO)

        class DummyTest(TestCase):

            def test(self):
                logger.info("hello")

        result = StreamResult()
        wrapper = AutoTimingTestResultDecorator(
            ExtendedToStreamDecorator(result))

        test = DummyTest(methodName="test")
        test(wrapper)
        self.assertTrue(wrapper.wasSuccessful())

        event = result._events[-2]

        self.assertEqual("status", event[0])
        self.assertEqual(1346236702, int(event[-1].strftime("%s")))

    def test_no_stream(self):
        """If no StreamResult is detected, the log record is dropped."""

        logger = Logger("test")
        logger.addHandler(SubunitHandler())
        logger.setLevel(INFO)

        class DummyTest(TestCase):

            def test(self):
                logger.info("hello")

        result = TestResult()

        test = DummyTest(methodName="test")
        test(result)
        self.assertTrue(result.wasSuccessful())
