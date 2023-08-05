# encoding: utf-8
from __future__ import print_function, division, absolute_import

from datetime import datetime as dt
from functools import partial

import zmq


class Logger:
    """This is sending signals to the log_receiver via port 5559 (using zmq)
    """

    def __init__(self, context, id_=""):
        self.id_ = id_
        self.sender = context.socket(zmq.PUSH)
        self.sender.connect("tcp://127.0.0.1:5559")

        self.debug = partial(self._log, "debug")
        self.info = partial(self._log, "info")
        self.warn = partial(self._log, "warn")
        self.error = partial(self._log, "error")

    def shutdown(self):
        self.sender.send(b"KILL|")

    def _log(self, level, *a):
        text = " ".join(map(str, a))
        #text = "%-12s: %s" % (self.prefix, text)
        message = "%s|%s|%s|%s" % (level, dt.now(), self.id_, text)
        self.sender.send(message.encode("utf-8"), flags=zmq.NOBLOCK)
