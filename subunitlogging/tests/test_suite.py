import logging

from unittest import TestSuite

from six import b

from testtools import TestCase
from testtools import ExtendedToStreamDecorator
from testtools.testresult.doubles import StreamResult

from subunitlogging import SubunitLoggingSuite


class SubunitLoggingSuiteTest(TestCase):

    def setUp(self):
        super(SubunitLoggingSuiteTest, self).setUp()
        self.result = StreamResult()
        self.suite = SubunitLoggingSuite(TestSuite(), level=logging.INFO)

    def test_run(self):

        class DummyTest(TestCase):

            def test(self):
                logging.info("hello")

        test = DummyTest(methodName="test")
        self.suite.addTest(test)
        self.suite.run(ExtendedToStreamDecorator(self.result))
        event = self.result._events[2]
        self.assertIn("DummyTest.test", event[1])
        self.assertEqual(b("hello\n"), event[6])
