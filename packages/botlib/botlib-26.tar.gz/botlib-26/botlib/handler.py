# BOTLIB Framework to program bots
#
# botlib/handler.py
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

""" schedule events. """

from .error import ENOWORKER, ENOCOMMAND
from .object import Default, Object
from .register import Register
from .trace import get_exception, get_from

import importlib
import logging
import pkgutil
import queue
import time
import types

class Handler(Object):

    """
        A Handler handles events pushed to it. Handlers can be threaded,
        e.g. start a thread on every event received, or not threaded in which
        case the event is handeled in loop.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._booted = Object()
        self._cmnds = []
        self._handlers = Register()
        self._names = Register()
        self._queue = queue.Queue()
        self._running = False
        self._stopped = False
        self._threaded = False
        self._finished = Object()
        self._handlers = Register()
        self._names = Register()
        self._scanned = False
        self._stopped = False
        self._table = Object()
        self._time = Default(default=0)

    def direct(self, name, package=None):
        """ import a module directly, not storing it in the cache. """
        logging.debug("- direct %s from %s" % (name, get_from()))
        return importlib.import_module(name, package)

    def dispatch(self, *args, **kwargs):
        """ handle an event. """
        from .space import users
        event = args[0]
        if not event._parsed:
            event.parse()
        event._funcs = self.get_handlers(event._parsed.cmnd)
        for func in event._funcs:
            if "perm" in dir(func):
                if not users.allowed(event.origin, func.perm):
                    event.ready()
                    return
        if event._parsed.cmnd:
            logging.warn("# dispatch %s (%s)" % (event._parsed.cmnd, event.origin))
        event.dispatch()
        event.show()
        event.prompt()
        event.ready()
        return event

    def get_handlers(self, cmnd):
        """ search for a function registered by command. """
        from .space import alias, cfg
        oldcmnd = cmnd
        cmnd = alias.get(cmnd, cmnd)
        funcs = self._handlers.get(cmnd, [])
        if not funcs:
            funcs = self._handlers.get(oldcmnd, [])
            if not funcs:
                modnames = self._names.get(cmnd, [])
                for modname in modnames:
                    self.load(modname, True)
                    funcs = self._handlers.get(cmnd, [])
                    break
        return funcs

    def list(self, name):
        """ list all functions found in a module. """
        for modname in self.modules(name):
            mod = self.load(modname)
            for key in dir(mod):
                if key in ["init", "shutdown"]:
                    continue
                obj = getattr(mod, key, None)
                if obj and type(obj) == types.FunctionType:
                    if "event" in obj.__code__.co_varnames:
                        yield key

    def load(self, modname, force=False):
        """ load a module. """
        if force or modname not in self._table:
            self._table[modname] = self.direct(modname)
        elif modname in self._table:
            return self._table[modname]
        for key in dir(self._table[modname]):
            if key.startswith("_"):
                continue
            obj = getattr(self._table[modname], key, None)
            if obj and type(obj) == types.FunctionType:
                if "event" in obj.__code__.co_varnames:
                    self._names.register(key, modname)
                    if key not in ["init", "shutdown"]:
                        self._handlers.register(key, obj)
        return self._table[modname]

    def modules(self, name):
        """ return a list of modules in the named packages or cfg.packages if no module name is provided. """
        package = self.load(name)
        for pkg in pkgutil.walk_packages(package.__path__, name + "."):
            yield pkg[1]

    def scheduler(self):
        """ main loop of the Handler. """
        from .space import pool
        self._state.status = "run"
        self._time.latest = time.time()
        while not self._stopped:
            self._counter.nr += 1
            args, kwargs = self._queue.get()
            if not args:
                self._stopped = True
                break
            event = args[0]
            if not event:
                break
            try:
                pool.put(self.dispatch, event)
            except ENOWORKER:
                thr = self.launch(self.dispatch, event)
                event._thrs.append(thr)
            except Exception as ex:
                event.direct(get_exception())
                event.ready()
                event.prompt()
        self._state.status = "done"

    def prompt(self, *args, **kwargs):
        """ virtual handler to display a prompt. """
        pass

    def put(self, *args, **kwargs):
        """ put an event to the handler. """
        self._queue.put_nowait((args, kwargs))

    def register(self, key, val, force=False):
        """ register a handler. """
        self._handlers.register(key, val, force=force)

    def start(self, *args, **kwargs):
        """ give the start signal. """
        from .space import launcher
        self._stopped = False
        launcher.launch(self.scheduler)

    def stop(self):
        """ stop the handler. """
        self._stopped = True
        self._state.status = "stop"
        self._queue.put((None, None))

    def walk(self, name, init=False, force=False):
        """ return all modules in a package. """
        self._scanned = True
        for modname in sorted(list(self.modules(name))):
            self.load(modname, force)
