from testtools import TestCase
from testtools import ExtendedToStreamDecorator

from testlogging import SubunitHandler
from testlogging.result import ExtendedToSubunitHandlerDecorator
from testlogging.testing import StreamResultDouble


class ExtendedToSubunitHandlerDecoratorTest(TestCase):

    def setUp(self):
        super(ExtendedToSubunitHandlerDecoratorTest, self).setUp()
        self.stream = StreamResultDouble()
        self.handler = SubunitHandler()
        self.result = ExtendedToSubunitHandlerDecorator(
            self.stream, self.handler)

    def test_startMakeResource(self):
        self.result.startMakeResource(None)
        event = self.stream.getEvent(0)
        self.assertEqual("resource", event.test_id)
        self.assertEqual("inprogress", event.test_status)

    def test_stopMakeResource(self):
        self.result.stopMakeResource(None)
        event = self.stream.getEvent(0)
        self.assertEqual("resource", event.test_id)
        self.assertEqual("success", event.test_status)

    def test_startCleanResource(self):
        self.result.startCleanResource(None)
        event = self.stream.getEvent(0)
        self.assertEqual("resource", event.test_id)
        self.assertEqual("inprogress", event.test_status)

    def test_stopCleanResource(self):
        self.result.stopCleanResource(None)
        event = self.stream.getEvent(0)
        self.assertEqual("resource", event.test_id)
        self.assertEqual("success", event.test_status)

    def test_startTest(self):

        self.stream.startTest = lambda test: None

        class SampleTest(TestCase):
            pass

        self.result.startTest(SampleTest(methodName="run"))
        self.assertIn("SampleTest.run", self.handler._test_id)

    def test_stopTest(self):

        self.stream.stopTest = lambda test: None

        class SampleTest(TestCase):
            pass

        self.result.stopTest(SampleTest(methodName="run"))
        self.assertIs(None, self.handler._test_id)
