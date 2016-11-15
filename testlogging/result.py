from extras import safe_hasattr

from testtools import ExtendedToOriginalDecorator


class ExtendedToSubunitHandlerDecorator(ExtendedToOriginalDecorator):

    def __init__(self, result, handler):
        super(ExtendedToSubunitHandlerDecorator, self).__init__(result)
        self._handler = handler
        self._handler.setResult(self)

    def startMakeResource(self, resource):
        self.status(
            test_id="resource", test_status="inprogress", runnable=False)
        self._handler.setTestId("resource", runnable=False)

    def stopMakeResource(self, resource):
        self.status(test_id="resource", test_status="success", runnable=False)
        self._handler.setTestId(None)

    def startCleanResource(self, resource):
        self.status(
            test_id="resource", test_status="inprogress", runnable=False)
        self._handler.setTestId("resource", runnable=False)

    def stopCleanResource(self, resource):
        self.status(test_id="resource", test_status="success", runnable=False)
        self._handler.setTestId(None)

    def startTest(self, test):
        super(ExtendedToSubunitHandlerDecorator, self).startTest(test)
        self._handler.setTestId(test.id())

    def stopTest(self, test):
        super(ExtendedToSubunitHandlerDecorator, self).stopTest(test)
        self._handler.setTestId(None)


def get_stream_result(result):
    """Extract a StreamResult-like result object from the given result.

    This function will Figure out if the given result object implements the
    StreamResult API (i.e. the 'status' method), and if not, try to see
    if the result object is actually a decorator, directly or indirectly
    wrapping a StreamResult.

    It's needed because since testtools decorates and nests result objects, we
    in order to find and use the status() API, we have to traverse the
    decoration, until we either find a StreamResult-like decorated result, or
    we reach the bottom.
    """
    while not safe_hasattr(result, "status"):
        decorated = getattr(result, "decorated", None)
        if decorated:
            result = decorated
            continue
        raise RuntimeError("Not a stream result")
    return result
