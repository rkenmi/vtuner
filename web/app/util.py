import contextlib
import sys

def getfilesystemencoding():
    # get file system encoding, making sure never to return None
    return sys.getfilesystemencoding() or sys.getdefaultencoding()

@contextlib.contextmanager
def gobject_signals(obj, *signals):
    """Context manager to connect and disconnect GObject signals using a ``with``
    statement.
    """
    signal_ids = []
    try:
        for signal in signals:
            signal_ids.append(obj.connect(*signal))
        yield
    finally:
        for signal_id in signal_ids:
            obj.disconnect(signal_id)
