from datetime import datetime

from logging import Handler

from six import b

from testtools.content_type import ContentType
from testtools.testresult.real import utc

from testlogging.result import get_stream_result


class SubunitHandler(Handler):

    def __init__(self):
        super(SubunitHandler, self).__init__()
        self._result = None
        self._file_name = "test.log"
        self._format = None
        self._test_id = None
        self._runnable = True

    def setResult(self, result):
        self._result = result

    def setFileName(self, file_name):
        self._file_name = file_name

    def setFormatter(self, fmt, name="custom"):
        super(SubunitHandler, self).setFormatter(fmt)
        self._format = name

    def setTestId(self, test_id, runnable=True):
        self._test_id = test_id
        self._runnable = runnable

    def emit(self, record):
        self._write(("%s\n" % self.format(record)).encode("utf-8"))

    def close(self):
        self._write(b(""), eof=True)

    def _write(self, file_bytes, eof=False):
        result = get_stream_result(self._result)
        result.status(
            test_id=self._test_id,
            runnable=self._runnable,
            file_name=self._file_name,
            file_bytes=file_bytes,
            eof=eof,
            mime_type=self._mime_type(),
            timestamp=datetime.now(utc))

    def _mime_type(self):
        """
        The MIME type parameters contain details specific to Python's logging
        system.

        This allows consumers to possibly parse back the log message.
        """
        parameters = {
            "charset": "utf8",
            "language": "python",
            "format": self._format or "default",
        }
        return repr(ContentType("text", "x-log", parameters))
