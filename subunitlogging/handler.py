from datetime import datetime

from logging import Handler
from extras import safe_hasattr

from six import b

from testtools.content_type import ContentType
from testtools.testresult.real import utc


class SubunitHandler(Handler):

    def __init__(self):
        super(SubunitHandler, self).__init__()
        self._result = None
        self._file_name = "test.log"
        self._format = None
        self._test_id = None

    def setResult(self, result):
        self._result = result

    def setFileName(self, file_name):
        self._file_name = file_name

    def setFormatter(self, fmt, name="custom"):
        super(SubunitHandler, self).setFormatter(fmt)
        self._format = name

    def setTestId(self, test_id):
        self._test_id = test_id

    def emit(self, record):
        self._write(("%s\n" % self.format(record)).encode("utf-8"))

    def close(self):
        self._write(b(""), eof=True)

    def _write(self, file_bytes, eof=False):

        # Figure out is our result object implements the StreamResult API (i.e.
        # the 'status' method). Since testtools decorates and nests result
        # objects, we need to traverse the decoration, until we either find
        # a StreamResult-like decorated result, or we reach the bottom.
        result = self._result
        while not safe_hasattr(result, "status"):
            decorated = getattr(result, "decorated", None)
            if decorated:
                result = decorated
                continue
            return

        timestamp = datetime.now(utc)

        result.status(
            test_id=self._test_id,
            timestamp=timestamp,
            file_name=self._file_name, mime_type=self._mime_type(),
            file_bytes=file_bytes,
            eof=eof)

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
