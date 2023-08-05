# encoding: utf-8
from __future__ import print_function, division, absolute_import

import logging
import signal
import threading
import random
import time

import zmq

from dispatcher import Dispatcher
from logger import Logger
from log_receiver import LogReceiver


def main():
    """Demo program to show how ZeroMQ (zmq) in action.
    At the beginning, the dispatcher is started (using 5 workers). Then, work is submitted from the dispatcher
    via port 5555 to the workers. When all work is finished, the shutdown is initiated (dispatcher.shutdown)

    Next to the work-dispatcher there is a logger.py and its counterpart, the log_receiver.py. The logger works independent
    from the dispatcher and communicates via port 5559 with the log_receiver.

    Pressing CTRL-C does not immediately kill the running processes. Instead, the workers and loggers are safely terminated.
    """
    context = zmq.Context()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(dt)s - %(levelname)-7s - %(id_)-10s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    """
    todo: wait until all workers are ready before we dispatch.
        write function for setup
        find path of worker.py for dispatching
    """

    log_receiver = LogReceiver(context, logger)
    log_thread = threading.Thread(target=log_receiver.loop)
    log_thread.start()

    logger = Logger(context, "main")
    logger.info("MAIN STARTED")

    # start the dispatcher with 5 workers.
    dispatcher = Dispatcher(5, context)

    try:
        # the main "work" which is sent to the dispatcher
        for i in range(10):
            logger.info("submit HELLO%d" % i)
            dispatcher.submit(b"PROCESS|HELLO%i" % i)
            dispatcher.submit(b"ECHO")
            dispatcher.submit(b"FUZZ|0.5,2.0")
            time.sleep(random.random() * 2)

    except KeyboardInterrupt:
        # keyboard interrupt is forwared to workers, they finish current job and
        # then exit.
        logger.warn("got KeyboardInterrupt")

        def shutdown(*a):
            logger.warn("no futher KeyboardInterrupt accepted, be patient for shutdown")
        # avoid further interruption, just log a message:
        signal.signal(signal.SIGINT, shutdown)
    finally:

        logger.info("MAIN DONE")
        # proper shutdown of the workers (by sending them a "DONE" message).
        dispatcher.shutdown()
        logger.shutdown()
        log_thread.join()


if __name__ == "__main__":
    main()
