from search_adapters import classify_exception


def test_classify_exception_timeout():
    exc = TimeoutError("timed out")
    assert classify_exception(exc) == "timeout"


def test_classify_exception_connection():
    exc = ConnectionError("connection reset")
    assert classify_exception(exc) == "connection_error"
