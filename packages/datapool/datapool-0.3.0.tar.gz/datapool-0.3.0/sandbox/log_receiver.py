# encoding: utf-8
from __future__ import print_function, division, absolute_import

from collections import defaultdict
import zmq


class LogReceiver:
    """listens to a specific port (5559) to receive messages
    """

    def __init__(self, context, logger):
        self.receiver = context.socket(zmq.PULL)
        self.receiver.bind("tcp://127.0.0.1:5559")
        self.log_functions = defaultdict(lambda: logger.critical)
        for level in ("debug", "info", "warn", "error"):
            self.log_functions[level] = getattr(logger, level)

    def loop(self):

        while True:
            try:
                message = str(self.receiver.recv(), "utf-8")
            except zmq.ZMQError as zerr:
                # context terminated so quit silently
                if zerr.strerror == 'Context was terminated':
                    raise zerr
                else:
                    raise zerr
            if message.startswith("KILL|"):
                break

            level, dt, id_, text = message.split("|", 3)
            self.log_functions[level](text, extra=dict(id_=id_, dt=dt))
