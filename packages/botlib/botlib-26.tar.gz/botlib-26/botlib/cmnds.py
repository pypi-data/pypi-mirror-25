# BOTLIB Framework to program bots
#
# botlib/cmnds.py
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

""" botlib basic commands. """

from .clock import Timer
from .compose import compose
from .db import Db
from .event import Event
from .object import Config, Object
from .space import runtime, users, set_space
from .space import kernel as _kernel
from .space import fleet as _fleet
from .template import template
from .trace import get_exception
from .utils import day, elapsed, now, to_date, to_day, to_time, parse_time
from .utils import sname

import botlib.space
import _thread
import logging
import mailbox
import time
import json
import sys
import os

psformat = "%-4s %-8s %-24s %-4s %6s %6s"

starttime = time.time()

def shutdown(event):
    """ close commands plugins. """
    pass

class Email(Object):
    """ email object. """
    pass

class Entry(Object):
    """ data entry class . """
    pass

class Log(Entry):
    """ a log entry to log what is happening on the day. """
    pass


class Rss(Entry):
    """ rss entry """
    pass

class Shop(Entry):
    """ shopping item for the wife to shop. """
    pass

class Todo(Entry):
    """ todo entry """
    pass

class Tomorrow(Entry):
    """ todo for tomorrow to be done. """
    pass

class Watch(Entry):
    """ files to watch. """
    pass

def license(event):
    """ display BOTLIB license. """
    from botlib import __license__
    event.reply(__license__)

license.perm = "USER"

def alias(event):
    """ key, value alias. """
    try:
        cmnd, value = event._parsed.rest.split(" ", 1)
    except ValueError:
        event.reply('alias <cmnd> <aliased>')
        return
    if value not in _kernel._names:
        event.reply("only commands can be aliased.")
        return
    botlib.space.alias[cmnd] = value
    botlib.space.alias.save()
    event.ok(cmnd)

alias.perm = "USER"

def announce(event):
    """ announce text on all channels in fleet. """
    _kernel.announce(event._parsed.rest)

announce.perm = "ANNOUNCE"

def begin(event):
    """ begin stopwatch. """
    t = to_time(now())
    event.reply("time is %s" % time.ctime(t))

begin.perm = "USER"

def cfg(event):
    """ edit config files. """
    args = event._parsed.args
    if not args:
        event.reply(botlib.space.cfg)
        return
    name = args[0]
    if name not in template.keys():
        event.reply("%s config doesn't exist" % name)
        return
    obj = Config()
    obj.fromdisk(name)
    try:
        key = args[1]
    except IndexError:
        event.reply(obj)
        return
    if key not in obj:
        event.reply("EKEY %s" % key)
        return
    val = ""
    if len(args) > 3:
        val = args[2:]
    elif len(args) == 3:
        val = args[2]
    elif key in obj:
        event.reply("%s: %s" % (key, obj[key]))
        return
    else:
        event.reply("EKEY %s" % key)
    try:
        val = int(val)
    except:
        try:
            val = float(val)
        except:
            pass
    if type(val) == list:
        obj[key] = list(val)
    elif val in ["True", "true"]:
        obj[key] = True
    elif val in ["False", "false"]:
        obj[key] = False
    else:
        try:
            val = '"%s"' % val
            obj[key] = json.loads(val)
        except (SyntaxError, ValueError) as ex:
            event.reply("%s: %s" % (str(ex), val))
            return
    if key == "user" and "@" in obj[key]:
        obj["username"], obj["server"] = obj[key].split("@")
    obj.sync(os.path.join(botlib.space.cfg.workdir, "config", name))
    event.ok(key)

cfg.perm = "CFG"

def edit(event):
    """ edit and save objects. """
    args = event._parsed.args
    if not args:
        event.reply(",".join(botlib.space.__all__))
        return
    name = args[0]
    if name not in botlib.space.__all__:
        event.reply("%s is not an object in botlib.space." % name)
        return
    obj = getattr(botlib.space, name)
    try:
        key = args[1]
    except IndexError:
        event.reply(obj)
        return
    value = obj.get(key, None)
    if not value:
        event.reply("no value set")
        return
    if len(args) > 3:
        val = args[2:]
    elif len(args) == 3:
        val = args[2]
    else:
        event.reply("%s: %s" % (key, value))
        return
    set_space(name, key, val)
    event.ok(key, value)

edit.perm = "EDIT"

def cmnds(event):
    """ show list of commands. """
    res = sorted(set([cmnd for cmnd, mod in _kernel._names.items() if event._parsed.rest in str(mod)]))
    event.reply(",".join(res) or "no modules loaded.")

cmnds.perm = "USER"

def deleted(event):
    """ show deleted records. """
    event.nodel = True
    nr = 0
    db = Db()
    for obj in db.selected(event):
        nr += 1
        event.display(obj, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")

deleted.perm = "USER"

def delperm(event):
    """ delete permissions of an user. """
    try:
        nick, *perms = event._parsed.args
    except:
        event.reply("delperm <origin> <perm>")
        return
    origin = _fleet.get_origin(nick)
    user = users.delete(origin, perms)
    if not user:
        event.reply("can't find a user matching %s" % origin)
        return
    event.ok(origin, perms)

delperm.perm = "OPER"

def dump(event):
    """ dump objects matching the given criteria. """
    nr = 0
    db = Db()
    for obj in db.selected(event):
        nr += 1
        event.reply(obj.nice())
    if not nr:
        event.reply("no results")

dump.perm = "USER"

def end(event):
    """ stop stopwatch. """
    diff = time.time() - starttime
    if diff:
        event.reply("time elapsed is %s" % elapsed(diff))

end.perm = "USER"

def exit(event):
    """ stop the bot. """
    _thread.interrupt_main()

exit.perm = "EXIT"

def fetcher(event):
    """ fetch all rss feeds. """
    from .space import launcher
    clients = runtime.get("RSS", [])
    for client in clients:
        c = compose(client)
        thrs = c.fetcher()
        res = launcher.waiter(thrs)
        if res:
            event.reply("fetched %s" % ",".join(res))

fetcher._threaded = True
fetcher.perm = "RSS"

def fix(event):
    """ fix a object by loading and saving it. """
    fn = event._parsed.rest
    if not fn:
        event.reply("fix <path>")
        return
    if not os.path.isfile(fn):
        event.reply("%s is not a file" % fn)
        return
    o = Object()
    o.load(event._parsed.rest)
    p = o.save()
    event.reply("saved %s" % p)

fix.perm = "OPER"

def find(event):
    """ present a list of objects based on prompt input. """
    nr = 0
    db = Db()
    for obj in db.selected(event):
        event.display(obj, event._parsed.args, str(nr), direct=True)
        nr += 1
    if not nr:
        event.reply("no results")

find.perm = "USER"

def first(event):
    """ show the first record matching the given criteria. """
    db = Db()
    obj = db.first(*event._parsed.args)
    if obj:
        event.reply(obj.nice())
    else:
        event.reply("no result")

first.permn = "USER"

def last(event):
    """ show last objectect matching the criteria. """
    if not event._parsed.args:
        event.reply("last <prefix> <value>")
        return
    db = Db()
    obj = db.last(*event._parsed.args)
    if obj:
        event.reply(obj.nice())
    else:
        event.reply("no result")

last.perm = "USER"

def load(event):
    """ force a plugin reload. """
    if not event._parsed.rest:
        event.reply(",".join([x.split(".")[-1] for x in _kernel.modules("botlib")]))
        return
    for modname in _kernel.modules("botlib"):
        if event._parsed.rest not in modname:
            continue
        try:
            event.reply("load %s" % _kernel.reload(modname, True))
        except (AttributeError, KeyError) as ex:
            event.reply("%s %s" % (modname, str(ex)))

load.perm = "LOAD"

def log(event):
    """ log some text. """
    if not event._parsed.rest:
        event.reply("log <item>")
        return
    o = Log()
    o.log = event._parsed.rest
    o.save()
    event.ok(1)

log.perm = "USER"

def loglevel(event):
    """ set loglevel. """
    from botlib.log import loglevel as _loglevel
    level = event._parsed.rest
    if not level:
        event.reply("loglevel is %s" % botlib.space.cfg.loglevel)
        return
    oldlevel = botlib.space.cfg.loglevel
    botlib.space.loglevel = level
    _kernel.sync(os.path.join(botlib.space.cfg.workdir, "runtime", "kernel"))
    try:
        _loglevel(level)
    except ValueError:
        try:
            _loglevel(oldlevel)
        except ValueError:
            pass

loglevel.perm = "LOGLEVEL"

def loud(event):
    """ disable silent mode of a bot. """
    for bot in _fleet:
        if event.id() == bot.id():
            bot.cfg.silent = False
            bot.cfg.sync()
            event.reply("silent mode disabled.")

loud.perm = "LOUD"

def ls(event):
    """ show subdirs in working directory. """
    event.reply(" ".join(os.listdir(botlib.space.cfg.workdir)))

ls.perm = "USER"

def mbox(event):
    """ convert emails to botlib objects. """
    if not event._parsed.rest:
        event.reply("mbox <path>")
        return
    fn = os.path.expanduser(event._parsed.args[0])
    event.reply("reading from %s" % fn)
    nr = 0
    if os.path.isdir(fn):
        thing = mailbox.Maildir(fn, create=False)
    elif os.path.isfile(fn):
        thing = mailbox.mbox(fn, create=False)
    else:
        event.reply("need a mbox or maildir.")
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for m in thing:
        try:
            o = Email()
            o.update(m.items())
            try:
                sdate = os.sep.join(to_date(o.Date).split())
            except AttributeError:
                sdate = None
            o.text = ""
            for payload in m.walk():
                if payload.get_content_type() == 'text/plain':
                    o.text += payload.get_payload()
            o.text = o.text.replace("\\n", "\n")
            if sdate:
                o.save(stime=sdate)
            else:
                o.save()
            nr += 1
        except:
            logging.error(get_exception())
    if nr:
        event.ok(nr)

mbox._threaded = True
mbox.perm = "MBOX"

def nick(event):
    """ change bot nick on IRC. """
    from .space import fleet
    bots = fleet.get_bot(event.id())
    for bot in bots:
        bot.donick(event._parsed.args[0])

nick.perm = "OPER"

def pid(event):
    """ show pid of the BOTLIB bot. """
    event.reply(str(os.getpid()))

pid.perm = "USER"

def permissions(event):
    """ show permissions granted to a user. """
    from .space import kernel
    for name, funcs in kernel._handlers.items():
        if event._parsed.rest in name:
            event.reply("permissions are %s" % ",".join([str(x.perm) for x in funcs if "perm" in dir(x)]))

permissions.perm = "USER"

def ps(event):
    """ show running threads. """
    from .space import launcher
    from .utils import name
    k = _kernel
    up = elapsed(int(time.time() - k._time.start))
    result = []
    for thr in sorted(launcher.running(), key=lambda x: name(x)):
        obj = Object(vars(thr))
        if "sleep" in obj:
            up = obj.sleep - int(time.time() - obj._time.latest)
        else:
            up = int(time.time() - obj._time.start)
        thrname = name(thr)[1:] + ")"
        result.append((up, thrname, obj))
    nr = 0
    for up, thrname, obj in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = psformat % (nr, elapsed(up), thrname[:30], obj._state.printable(nokeys=True), obj._counter.printable(reverse=False), obj._error.printable(nokeys=True))
        event.reply(res.rstrip())

ps.perm = "USER"

def meet(event):
    """ create an user record. """
    try:
        origin = event._parsed.rest
    except:
        event.reply("meet <nick> [<perm1> <perm2>]")
        return
    orig = _fleet.get_origin(origin)
    if not orig:
        orig = origin
    u = users.meet(orig)
    if u:
        event.reply("user %s created" % origin)
    else:
        event.reply("%s is already introduced." % origin)

meet.perm = "MEET"

def perm(event):
    """ add/change permissions of an user. """
    try:
        nick, perms = event._parsed.args
    except:
        event.reply("perm <origin> <perm>")
        return
    origin = _fleet.get_origin(nick)
    if not origin:
        origin = nick
    u = users.set(origin, perms)
    if not u:
        event.reply("can't find a user matching %s" % origin)
        return
    event.ok(origin)

perm.perm = "OPER"

def perms(event):
    u = users.fetch(event.origin)
    if u:
        event.reply("permissions are %s" % ",".join(u.perms))

perms.perm = "USER"

def real_reboot():
    """ actual reboot. """
    from .space import save as _save
    from .utils import reset
    _save()
    _kernel.shutdown(write=True)
    _kernel.wait()
    reset()
    os.execl(sys.argv[0], *(sys.argv + ["-r", "-z"]))

real_reboot.perm = "OPER"

def reboot(event):
    """ reboot the bot, allowing statefull reboot (keeping connections alive). """
    if not botlib.space.cfg.reboot:
        event.reply("# reboot is not enabled.")
        return
    event.announce("rebooting")
    real_reboot()

reboot.perm = "OPER"

def reload(event):
    """ reload a plugin. """
    if not event._parsed.rest:
        event.reply(",".join([x.split(".")[-1] for x in _kernel.modules("botlib")]))
        return
    for modname in _kernel.modules("botlib"):
        if event._parsed.rest not in modname:
            continue
        try:
            event.reply(_kernel.reload(modname, False))
        except (AttributeError, KeyError) as ex:
            event.reply("%s %s" % (modname, str(ex)))

reload.perm = "RELOAD"

def restore(event):
    """ set deleted=False in selected records. """
    db = Db()
    nr = 0
    event.nodel = True
    for obj in db.selected(event):
        obj.deleted = False
        obj.sync()
        nr += 1
    if not nr:
        event.reply("no results")
    event.ok(nr)

restore.perm = "RESTORE"

def rm(event):
    """ set deleted flag on objects. """
    db = Db()
    nr = 0
    for obj in db.selected(event):
        obj.deleted = True
        obj.sync()
        nr += 1
    event.ok(nr)

rm.perm = "RM"

def rss(event):
    """ add a rss url. """
    if not event._parsed.rest:
        event.reply("rss <item>")
        return
    o = Rss()
    o.rss = event._parsed.rest
    o.service = "rss"
    o.save()
    event.ok(1)

rss.perm = "USER"

def silent(event):
    """ put a bot into silent mode. """
    for bot in _fleet:
        if event.id() == bot.id():
            bot.cfg.silent = True
            bot.cfg.sync()
            event.reply("silent mode enabled.")

silent.perm = "SILENT"

def shop(event):
    """ add a shopitem to the shopping list. """
    if not event._parsed.rest:
        event.reply("shop <item>")
        return
    o = Shop()
    o.shop = event._parsed.rest
    o.save()
    event.ok(1)

shop.perm = "USER"

def show(event):
    """ show dumps of basic objects. """
    if not event._parsed.rest:
        event.reply("choose one of alias, db, cfg, exceptions, fleet, kernel, launcher, partyline, runtime, seen or users")
        return
    try:
        item, value = event._parsed.rest.split(" ", 1)
    except:
        item = event._parsed.rest
        value = None
    if item == "bot":
        bots = _fleet.get_bot(event.id())
        for bot in bots:
            event.reply(bot)
        return
    if item == "fleet":
        for bot in _fleet:
            if value:
                val = getattr(bot, value, None)
                event.reply("%s=%s" % (value, val))
            else:
                event.reply(bot)
        return
    obj = getattr(botlib.space, item, None)
    if value:
        val = getattr(obj, value, None)
        event.reply("%s: %s" % (value, val))
    else:
        event.reply(obj)

show.perm = "SHOW"

def save(event):
    """ make a kernel dump. """
    from .space import save as _save
    _save()
    event.reply("saved")

save.perm = "SAVE"

def start(event):
    """ start a plugin. """
    modnames = _kernel.modules("botlib")
    if not event._parsed.rest:
        res = set([x.split(".")[-1] for x in modnames])
        event.reply("choose one of %s" % ",".join(sorted(res)))
        return
    modname = event._parsed.args[0]
    name = "botlib.%s" % modname
    if name not in modnames:
        event.reply("no %s module found." % name)
        return
    mod = _kernel.load(name, force=True)
    if "init" in dir(mod):
        mod.init(event)
    event.ok(sname(mod).lower())

start.perm = "START"
start._threaded = True

def stop(event):
    """ stop a plugin. """
    if not event._parsed.rest:
        event.reply("stop what ?")
        return
    name = "botlib.%s" % event._parsed.args[0]
    try:
        mod = _kernel._table[name]
    except KeyError:
        event.reply("no %s module available." % name)
        return
    if "shutdown" in dir(mod):
        mod.shutdown(event)
    event.ok(event.txt)

stop._threaded = True
stop.perm = "STOP"

def synchronize(event):
    """ synchronize rss feeds (fetch but don't show). """
    clients = runtime.get("RSS", [])
    for client in clients:
        c = compose(client)
        seen = c.synchronize()
        event.reply("%s urls updated" % len(seen.urls))

synchronize.perm = "SYNCHRONIZE"

def test(event):
    """ echo origin. """
    from .utils import stripped
    event.reply("hello %s" % stripped(event.origin))

test.perm = "USER"

def timer(event):
    """ timer command to schedule a text to be printed on a given time. stopwatch to measure elapsed time. """
    if not event._parsed.rest:
        event.reply("timer <string with time>")
        return
    seconds = 0
    line = ""
    try:
        target = parse_time(event._parsed.rest)
    except ValueError:
        event.reply("can't detect time")
        return
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    e = Event(event)
    e.services = "clock"
    e._prefix = "timer"
    e.txt = event._parsed.rest
    e.time = target
    e.done = False
    e.save()
    t = Timer(target - time.time(), e.direct, e.txt)
    _kernel.launch(t.start)
    event.ok(time.ctime(target))

timer.perm = "USER"

def today(event):
    """ show last week's logged objects. """
    db = Db()
    event._parsed.start = to_day(day())
    event._parsed.end = time.time()
    nr = 0
    for obj in db.selected(event):
        nr += 1
        event.display(obj, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")

today.perm = "USER"

def todo(event):
    """ log a todo item. """
    if not event._parsed.rest:
        event.reply("todo <item>")
        return
    o = Todo()
    o.todo = event._parsed.rest
    o.save()
    event.ok(1)

todo.perm = "USER"

def tomorrow(event):
    """ show todo items for tomorrow. """
    if not event._parsed.rest:
        event.reply("tomorrow <item>")
        return
    o = Tomorrow()
    o.tomorrow = event.txt.replace("tomorrow", "").strip()
    o.save()
    event.ok(1)

tomorrow.perm = "USER"

def u(event):
    """ show user selected by userhost. """
    if not event._parsed.rest:
        event.reply("u <origin>")
        return
    nick = event._parsed.args[0]
    origin = _fleet.get_origin(nick)
    u = users.fetch(origin)
    if u:
        event.reply(u)

u.perm = "USER"

def w(event):
    """ show user data. """
    u = users.fetch(event.origin)
    if u:
        event.reply("user: %s" % u)
    else:
        event.reply("no matching user found.")

w.perm = "USER"

def uptime(event):
    """ show uptime. """
    event.reply("uptime is %s" % elapsed(time.time() - botlib._starttime))

uptime.perm = "USER"

def version(event):
    """ show version. """
    from botlib import __version__, __txt__
    event.reply("BOTLIB #%s - %s" % (__version__, __txt__))

version.perm = "USER"

def watch(event):
    """ add a file to watch (monitor and relay to channel). """
    if not event._parsed.rest:
        event.reply("watch <item>")
        return
    o = Watch()
    o.watch = event._parsed.rest
    o.save()
    event.ok(1)

watch.perm = "WATCH"

def week(event):
    """ show last week's logged objects. """
    db = Db()
    event._parsed.start = to_day(day()) - 7 * 24 * 60 * 60
    event._parsed.end = time.time()
    nr = 0
    for obj in db.selected(event):
        nr += 1
        event.display(obj, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")

week.perm = "USER"

def whoami(event):
    """ show origin. """
    event.reply("you have origin %s" % event.origin)

whoami.perm = "USER"

def yesterday(event):
    """ show last week's logged objects. """
    db = Db()
    event._parsed.start = to_day(day()) - 24 * 60 * 60
    event._parsed.end = to_day(day())
    nr = 0
    for obj in db.selected(event):
        nr += 1
        event.display(obj, event._parsed.args, str(nr))
    if not nr:
        event.reply("no results")

yesterday.perm = "USER"

