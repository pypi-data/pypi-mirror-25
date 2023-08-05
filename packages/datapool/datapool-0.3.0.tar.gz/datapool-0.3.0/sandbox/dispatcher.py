# encoding: utf-8

import os
import signal
import subprocess
import sys
import threading
import time

import zmq

from logger import Logger


# for debugging: print stacktrace if SIGUSR1 is received:
import faulthandler
faulthandler.register(signal.SIGUSR1)


def run_worker(*args):
    # it is better to use absolution imports here, but for development this will not work
    # unless we implement a command line to start the dispatcher
    try:
        from . import worker
    except:
        import worker
    worker_path = os.path.abspath(worker.__file__)
    cmdline = [sys.executable, worker_path] + list(args)

    def preexec():
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    # here the argument preexec_fn avoids forwarding of KeyboardInterrupt to workers
    return subprocess.Popen(cmdline, bufsize=0, preexec_fn=preexec)


class Dispatcher:
    """ The dispatcher is receiving work from demo.py (aka the client) via 'inproc://client' (in-process communication)
    A poller is introduced, which watches both for incoming work and available workers (communicating via port 5555).
    If there is incoming work, a worker is popped from the list of available workers and the work is sent to that worker.
    When the worker is finished, it sends the message "READY" back to the poller; the worker is then added to the list of available workers again.

    
    At any time, log-info is sent to the logger which is sending the message to the log_receiver (port 5559)
    """

    def __init__(self, num_workers, context, worker_ip="127.0.0.1", worker_port=5555):
        self.num_workers = num_workers

        self.workers_connect_to = "tcp://%s:%d" % (worker_ip, worker_port)
        self.client_sends_to = "inproc://client"

        self.context = context
        self.logger = Logger(context, "dispatcher")

        self._start_workers()
        self._setup_client_queue()

        self.dispatch_thread = threading.Thread(target=self._dispatch_loop)
        # self.dispatch_thread.daemon = True  # else Ctrl-C will not work
        self.dispatch_thread.start()

    def _start_workers(self):
        procs = []
        for worker_index in range(self.num_workers):
            id_ = "worker_%d" % worker_index
            proc = run_worker(id_, self.workers_connect_to)
            procs.append((id_, proc))

        self.procs = procs

    def _setup_client_queue(self):
        self.queue_socket = self.context.socket(zmq.PUSH)
        self.queue_socket.connect(self.client_sends_to)

    def submit(self, data):
        self.queue_socket.send(b"PROCESS|%s" % data)

    def shutdown(self):
        self.queue_socket.send(b"DONE|")
        self.logger.info("wait for dispatch thread to join")
        #while self.dispatch_thread.isAlive():
        #    time.sleep(.001)

        # wait until all threads are finished
        self.dispatch_thread.join()
        self.queue_socket.close()

    def terminate_workers(self):
        for id_, p in self.procs:
            p.wait()
            self.logger.info("%s (pid=%d) finished" % (id_, p.pid))

    def _dispatch_loop(self):

        self.frontend = self.context.socket(zmq.PULL)
        self.frontend.bind(self.client_sends_to)

        self.backend = self.context.socket(zmq.ROUTER)
        self.backend.bind(self.workers_connect_to)

        poller = zmq.Poller()
        poller.register(self.backend, zmq.POLLIN)
        poller.register(self.frontend, zmq.POLLIN)

        available_workers = []
        self._wait_for_all_workers(available_workers, poller)
        self.logger.info("available workers: %d" % len(available_workers))

        self._dispatch_all_work(available_workers, poller)
        self._wait_until_all_workers_are_available(available_workers, poller)

        self._send_kill_to_all_workers(available_workers)
        self._terminate()

    def _wait_for_all_workers(self, available_workers, poller):
        missing = self.num_workers
        while missing:

            socks = dict(poller.poll())

            if socks.get(self.backend) == zmq.POLLIN:
                worker_id, empty, message = self.backend.recv_multipart()
                assert empty == b""
                assert message == b"READY"
                missing -= 1
                available_workers.append(worker_id)

        self.logger.info("all %d workers up" % len(available_workers))

    def _dispatch_all_work(self, available_workers, poller):

        while True:

            socks = dict(poller.poll())

            if socks.get(self.backend) == zmq.POLLIN:
                self._update_available_workers(available_workers)

            # we only check for data to process if we have at least one worker available:
            if socks.get(self.frontend) == zmq.POLLIN:
                if available_workers:
                    action, payload = self.frontend.recv().split(b"|", 1)
                    self.logger.info("dispatcher received: %s %r" % (action, payload))
                    if action == b"DONE":
                        break
                    else:
                        # send payload to be processed by one available worker:
                        worker_id = available_workers.pop()
                        msg = b"PROCESS|%s" % payload
                        self.backend.send_multipart([worker_id, b"", msg])
                else:
                    # got data but no worker available
                    time.sleep(.001)

    def _update_available_workers(self, available_workers):
        worker_id, empty, message = self.backend.recv_multipart()
        assert empty == b""
        assert message == b"READY"
        available_workers.append(worker_id)

    def _wait_until_all_workers_are_available(self, available_workers, poller):
        # we got KILL and wait until all workers are ready again:
        self.logger.info("num workers", self.num_workers)
        while len(available_workers) < self.num_workers:
            self.logger.info("avail workers", available_workers)
            socks = dict(poller.poll())
            if socks.get(self.backend) == zmq.POLLIN:
                self._update_available_workers(available_workers)
            else:
                time.sleep(.001)
        self.logger.info("all workers waiting")

    def _send_kill_to_all_workers(self, available_workers):

        while available_workers:
            worker_id = available_workers.pop()
            msg = b"KILL"
            self.backend.send_multipart([worker_id, b"", msg])
            self.logger.info("sent KILL to %s" % worker_id)

        self.logger.info("sent KILL to all workers")

    def _terminate(self):
        self.logger.info("terminate worker processes")
        self.terminate_workers()
        self.frontend.close()
        self.backend.close()
        self.logger.info("zmq frontend + backend closed")
