from collections import namedtuple

from testtools.testresult.doubles import StreamResult

StatusEvent = namedtuple(
    "StatusEvent", [
        "name", "test_id", "test_status", "test_tags", "runnable", "file_name",
        "file_bytes", "eof", "mime_type", "route_code", "timestamp"])


class StreamResultDouble(StreamResult):

    def getEvent(self, index):
        event = self._events[index]
        if event[0] == "status":
            return StatusEvent(*event)
