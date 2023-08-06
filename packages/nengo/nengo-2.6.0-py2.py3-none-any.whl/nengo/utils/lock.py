import errno
import os
import os.path
import time

from nengo.exceptions import TimeoutError


class FileLock(object):
    def __init__(self, filename, timeout=10., poll=0.1):
        self.filename = filename
        self.timeout = timeout
        self.poll = poll
        self._fd = None

    def acquire(self):
        start = time.time()
        while True:
            try:
                self._fd = os.open(
                    self.filename, os.O_CREAT | os.O_RDWR | os.O_EXCL)
                return
            except OSError as err:
                if err.errno not in (errno.EEXIST, errno.EACCES):
                    raise
                elif time.time() - start >= self.timeout:
                    raise TimeoutError(
                        "Could not acquire lock '{filename}'.".format(
                            filename=self.filename))
                else:
                    time.sleep(self.poll)

    def release(self):
        if self._fd is not None:
            os.close(self._fd)
            os.remove(self.filename)
            self._fd = None

    @property
    def acquired(self):
        return self._fd is not None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def __del__(self):
        self.release()
