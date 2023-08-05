# BOTLIB Framework to program bots
#
# botlib/worker.py
#
# Copyright 2017 B.H.J Thate
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" worker thread that handles submitted jobs through Worker.put(func, args, kwargs). """

from .object import Default, Object
from .clock import Repeater
from .error import ENOWORKER, EBUSY
from .event import Event
from .launcher import Launcher
from .task import Task
from .trace import get_exception
from .utils import name as _name
from .utils import locked

import logging
import queue
import random
import threading
import time

class Worker(threading.Thread):

    """ Task are adapted Threads. """

    def __init__(self, *args, **kwargs):
        super().__init__(None, None, "", (), {})
        self._args = args
        self._kwargs = kwargs
        self._busy = False
        self._counter = Default(default=0)
        self._error = Default()
        self._end = time.time()
        self._name = kwargs.get("name", "")
        self._queue = queue.Queue()
        self._stopped = False
        self._results = []
        self._running = False
        self._state = Default()
        self._time = Default(default=0.0)
        self._time.begin = time.time()
        self._time.end = time.time()
        self._time.start = time.time()
        self.once = False

    def __iter__(self):
        """ return self as an iterator. """
        return self

    def __next__(self):
        """ yield next value. """
        for k in dir(self):
            yield k

    def since(self):
        """ show how many seconds till last function executed. """
        return time.time() - self._end

    def put(self, *args, **kwargs):
        """ put a func(args, kwargs) to work. """
        self._queue.put_nowait((args, kwargs))

    def run(self):
        """ run a loop that handles jobs. """
        from .space import profiler
        self._running = True
        while not self._stopped:
            args, kwargs = self._queue.get()
            if self._stopped:
                break
            self._busy = True
            func = args[0]
            self._name = _name(func)
            self.setName(self._name)
            args = args[1:]
            if args:
                event = args[0]
                if not event._parsed:
                    event.parse()
                self._error.cmnd = event._parsed.cmnd
            else:
                event = None
            self._counter.run += 1
            self._begin = time.time()
            self._state.status = "run"
            try:
                result = func(*args, **kwargs)
            except Exception as ex:
                logging.error(get_exception())
            self._state.status = "wait"
            self._end = time.time()
            self._elapsed = self._begin - self._end
            if self._elapsed > 5.0:
                profiler[self._error.cmnd] = self._elapsed
            self._error.cmnd = ""
            self._busy = False
        self._state.status = "stopped"

    def stop(self):
        """ stop this worker. """
        self._stopped = True
        self.put((None, None))

class Pool(Launcher):

    """ Pool of workers, default to 10 instances. """

    def __init__(self, nr=10):
        super().__init__()
        self._long = []
        self._workers = []
        self._nr = nr

    def cleanup(self):
        """" cleanup idle workers. """
        for worker in self._workers:
            if worker._state.status == "wait":
                worker.stop()
                self._workers.remove(worker)

    def get_worker(self):
        """ return a worker from pool. """
        self.cleanup()
        worker = self.get_free()
        if worker:
            return worker
        prev = 10000
        w = None
        for worker in self._workers:
            s = worker._queue.qsize()
            if s < prev:
                prev = s
                w = worker
        if len(self._workers) < self._nr:
            worker = Worker()
            worker.start()
            self._workers.append(worker)
            return worker
        return w
     
    def get_free(self):
        from .space import profiler
        for worker in self._workers:
            if worker._queue.empty():
                if not worker._busy:
                    return worker
                if worker._name not in profiler:
                    return worker

    def put(self, *args, **kwargs):
        """ dispatch to the next idle worker thread. """
        from .space import profiler, kernel, launcher
        func = args[0]
        if len(args) > 1 and type(args[1]) in [Event, ]:
            event = args[1]
            event.parse()
            event.prep()
            for func in event._funcs:
                if "_threaded" in dir(func) and func._threaded:
                    event._threaded = True
            if event._threaded or event._parsed.cmnd in profiler:
                thr = launcher.launch(*args, **kwargs)
                event._thrs.append(thr)
                return
        worker = self.get_worker()
        if worker:
            event = worker.put(*args, **kwargs)
            return event
        raise ENOWORKER
