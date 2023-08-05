# Sample Test passing with nose and pytest

from .context import FD

def test_fd():
    fd = FD()
    assert True, "dummy sample test"
