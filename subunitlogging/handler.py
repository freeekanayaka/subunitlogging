from logging import Handler
from datetime import datetime

from testtools.content_type import ContentType

from subunitlogging.result import _get_result

LOG = ContentType("foo", "bar", {"charset": "uft-8"})


class SubunitHandler(Handler):

    def emit(self, record):

        result = _get_result()
        decorated = getattr(result, "decorated", None)
        if not decorated or not hasattr(decorated, "status"):
            return

        timestamp = datetime.fromtimestamp(1346236702)

        decorated.status(
            timestamp=timestamp,
            file_name=record.name, mime_type=repr(LOG),
            file_bytes=(record.msg + "\n").encode("utf-8"), eof=True)
