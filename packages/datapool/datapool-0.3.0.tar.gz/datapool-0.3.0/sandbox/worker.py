# encoding: utf-8
from __future__ import print_function, division, absolute_import

import os
import random
import sys
import time

import zmq

from logger import Logger


def process(logger, pay_load):
    logger.info("process %r" % pay_load)
    time.sleep(1 + 2 * random.random())
    logger.info("processed %r" % pay_load)


def echo(logger, pay_load):
    logger.info("ECHO FROM process %d" % os.getpid())


def fuzz(logger, pay_load):
    min_, max_ = map(float, pay_load.split(b","))
    to_sleep = min_ + random.random() * (max_ - min_)
    logger.debug("fuzz says: sleep %.2f seconds" % to_sleep)
    time.sleep(to_sleep)
    logger.debug("fuzz says: I'm back to live")


handlers = {
    b"PROCESS": process,
    b"ECHO": echo,
    b"FUZZ": fuzz,
    }


class Worker:

    """
    Protocol: the worker sends "READY" after startup and waits for message.

    messages are "PROCESS|PROCESSOR|data" or "KILL". In the first case the payload
    is processed, in the latter case the worker stops and the process terminates.
    """

    def __init__(self, id_, client_url, handlers=handlers):
        self.id_ = id_
        self.set_connection(client_url)
        self.handlers = handlers

    def set_connection(self, client_url):
        self.client_url = client_url

    def start(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.IDENTITY, bytes(self.id_, "ascii"))
        self.socket.connect(self.client_url)
        self.logger = Logger(self.context, self.id_)
        self.logger.info("setup finnished, now loop")

        try:
            self._loop()
        except zmq.ZMQError as zerr:
            # context terminated so quit silently
            if zerr.strerror == 'Context was terminated':
                return
            else:
                raise zerr

        except KeyboardInterrupt:
            pass
        self.logger.info("%s done" % (self.id_,))

    def _loop(self):

        while True:
            self.socket.send(b"READY")
            self.logger.info("%s sent READY AND WAITS" % self.id_)
            message = self.socket.recv()
            self.logger.info("%s gets %r" % (self.id_, message))
            if message == b"KILL":
                break
            action, __, payload = message.partition(b"|")
            assert action == b"PROCESS", action
            processor, __, data = payload.partition(b"|")
            if processor in self.handlers:
                self.handlers[processor](self.logger, data)
            else:
                self.logger.error("worker %s does not know how to to handle %r" % (self.id_,
                                                                                   message))

if __name__ == "__main__":
    Worker(sys.argv[1], sys.argv[2]).start()
