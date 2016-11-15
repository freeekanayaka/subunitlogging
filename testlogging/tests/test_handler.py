import time

from testtools import TestResult

from logging import (
    Formatter,
    Logger,
    INFO,
)

from six import b

from mimeparse import parse_mime_type

from testtools import TestCase

from testlogging import SubunitHandler
from testlogging.testing import StreamResultDouble


class SubunitHandlerTest(TestCase):

    def setUp(self):
        super(SubunitHandlerTest, self).setUp()
        self.result = StreamResultDouble()
        self.handler = SubunitHandler()
        self.handler.setResult(self.result)
        self.logger = Logger("test")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(INFO)

    def test_default(self):
        """The handler has sane defaults."""
        self.logger.info("hello")

        event = self.result.getEvent(0)
        self.assertEqual("status", event.name)
        self.assertIsNone(event.test_id)
        self.assertEqual("test.log", event.file_name)
        self.assertEqual(b("hello\n"), event.file_bytes)
        _, _, parameters = parse_mime_type(event.mime_type)
        self.assertEqual("python", parameters["language"])
        self.assertEqual("default", parameters["format"])
        self.assertAlmostEqual(
            time.time(), time.mktime(event.timestamp.timetuple()), delta=5)

    def test_decorated(self):
        self.addCleanup(self.handler.setResult, self.result)
        self.handler.setResult(TestResult())
        error = self.assertRaises(RuntimeError, self.logger.info, "hello")
        self.assertEqual("Not a stream result", str(error))

    def test_format(self):
        """A custom formatter and format name can be specified."""
        formatter = Formatter("[%(name)s:%(levelname)s] %(message)s")
        self.handler.setFormatter(formatter, "myformat")

        self.logger.info("hello")

        event = self.result.getEvent(0)
        self.assertEqual(b("[test:INFO] hello\n"), event.file_bytes)
        _, _, parameters = parse_mime_type(event.mime_type)
        self.assertEqual("python", parameters["language"])
        self.assertEqual("myformat", parameters["format"])

    def test_file_name(self):
        """A custom file name can be specified."""
        self.handler.setFileName("my.log")

        self.logger.info("hello")

        event = self.result.getEvent(0)
        self.assertEqual("my.log", event.file_name)

    def test_test_id(self):
        """A custom test ID can be specified."""
        self.handler.setTestId("my.test")

        self.logger.info("hello")

        event = self.result.getEvent(0)
        self.assertEqual("my.test", event.test_id)

    def test_close(self):
        """
        When the handler is closed, an EOF packet is written.
        """
        self.handler.close()
        event = self.result.getEvent(0)
        self.assertEqual(b(""), event.file_bytes)
        self.assertTrue(event.eof)
