# BOTLIB Framework to program bots
#
# botlib/xmpp.py
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

""" XMPP bot class. """

from .bot import Bot
from .event import Event
from .object import Default, Object
from .utils import stripped
from .space import cfg, fleet, launcher
from .trace import get_exception

import os
import logging
import ssl
import time

def init(*args, **kwargs):
    """ initialize the xmpp bot. """
    bot = XMPP()
    bot.start()
    return bot

def stop(event):
    """ stop the xmpp bot. """
    for bot in fleet.get_type("xmpp"):
        bot.stop()
    launcher.kill("XMPP")

class XMPP(Bot):

    """" XMPP bot based on sleekxmpp. """

    cc = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._threaded = False
        self.channels = []
        if cfg.channel:
            self.channels.append(cfg.channel)
            
    def _connect(self, user, pw):
        """ connect to the xmpp server. """
        self._makeclient(user, pw)
        self.client.reconnect_max_attempts = 3
        logging.info("! connect %s" % self.cfg.user)
        if self.cfg.noresolver:
            self.client.configure_dns(None)
        if self.cfg.openfire:
            self.client.connect(use_ssl=True)
        else:
            self.client.connect()

    def _makeclient(self, jid, password):
        """ create a sleekxmpp client to use. """
        try:
            import sleekxmpp.clientxmpp
            import sleekxmpp
        except ImportError:
            logging.warn("# sleekxmpp is not installed")
            return
        self.client = sleekxmpp.clientxmpp.ClientXMPP(jid, password)
        self.client._counter = Default(default=0)
        self.client._error = Object()
        self.client._state = Object()
        self.client._state.status = "running"
        self.client._time = Default(default=0)
        self.client._time.start = time.time()
        self.client.use_ipv6 = cfg.use_ipv6
        if cfg.no_certs:
            #self.client.ca_certs = ssl.CERT_NONE
            self.client.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
        self.client.register_plugin(u'xep_0030')  # Service Discovery
        self.client.register_plugin(u'xep_0045')  # Multi-User Chat
        self.client.register_plugin(u'xep_0199')  # XMPP Ping
        self.client.register_plugin(u'xep_0203')  # XMPP Delayed messages
        self.client.add_event_handler("session_start", self.session_start)
        self.client.add_event_handler("message", self.messaged)
        self.client.add_event_handler("iq", self.iqed)
        self.client.add_event_handler("ssl_invalid_cert", self.invalid_cert)
        self.client.add_event_handler('disconnected', self.disconnected)
        self.client.add_event_handler('connected', self.connected)
        self.client.add_event_handler('presence_available', self.presenced)
        self.client.add_event_handler('presence_dnd', self.presenced)
        self.client.add_event_handler('presence_xa', self.presenced)
        self.client.add_event_handler('presence_chat', self.presenced)
        self.client.add_event_handler('presence_away', self.presenced)
        self.client.add_event_handler('presence_unavailable', self.presenced)
        self.client.add_event_handler('presence_subscribe', self.presenced)
        self.client.add_event_handler('presence_subscribed', self.presenced)
        self.client.add_event_handler('presence_unsubscribe', self.presenced)
        self.client.add_event_handler('presence_unsubscribed', self.presenced)
        #self.client.add_event_handler('groupchat_message', self.messaged)
        self.client.add_event_handler('groupchat_presence', self.presenced)
        self.client.add_event_handler('groupchat_subject', self.presenced)
        self.client.add_event_handler('failed_auth', self.failedauth)
        self.client.exception = self.exception
        self.client.use_signals()

    def announce(self, txt):
        """ announce text on the joined channels. """
        for channel in self.channels:
            self.say(channel, txt)

    def connect(self, user):
        """ connect to the xmpp server. """
        fn = os.path.expanduser("~/.sleekpass")
        pww = ""
        f = open(fn, "r")
        pww = f.read()
        f.close()
        self.user = user
        self.passwd = pww.strip()
        self._connect(self.user, self.passwd)
        
    def connected(self, data):
        """ called when the bot is connected to the server. """
        self._connected.ready()
        self.joinall()
        self.ready()
 
    def disconnected(self, data):
        """ disconnedted callback. """
        pass

    def event(self):
        """" generate an event from the data in _queue. """
        e = self._queue.get()
        if e:
            e.btype = self.type
        return e

    def exception(self, data):
        """ exception callback. """
        self._error = data

    def failedauth(self, data):
        """ failedauth callback. """
        logging.info("! failed auth %s" % data)

    def failure(self, data):
        """ failure callback. """
        logging.info("! failure %s" % data)
        self._error = data

    def invalid_cert(self, data):
        """ invalid certifcate callback. """
        logging.info("! invalid cert")

    def iqed(self, data):
        """ iq callback. """
        logging.info("! iq %s:%s %s" % (self.cfg.server, self.cfg.port, data))

    def join(self, room):
        self.client.plugin['xep_0045'].joinMUC(room,
                                    self.cfg.nick,
                                    wait=False)

    def messaged(self, data):
        """ function to handle messages from server. """
        from .space import kernel
        m = Event()
        m.update(data)
        if m.type == "error":
            logging.error("^ %s" % m.error)
            return
        if m.type == "groupchat":
            m.cc = "!"
            m.element = "groupchat"
        else:
            m.cc = ""
            m.element = "message"
        m["from"] = str(m["from"])
        if self.cfg.user in m["from"]:
            logging.debug("ignore %s %s" % (m.type, m["from"]))
            return
        m.origin = m["from"]
        m.btype = self.type
        m.server = self.cfg.server
        m.channel = m.origin
        m.to = m.origin
        m.txt = m["body"]
        if '<delay xmlns="urn:xmpp:delay"' in str(data):
            logging.info("! ignore %s" % m.origin)
            return
        logging.info("! %s %s" % (m.channel, m.txt))
        kernel.put(m)

    def pinged(self, event):
        """ ping callback. """
        pass

    def presenced(self, data):
        """ function to handle presences. """
        from .space import kernel
        o = Event()
        o.cc = ""
        o.update(data)
        o.id = self.id()
        o.origin = o["from"]
        if "txt" not in o:
            o.txt = ""
        o.element = "presence"
        username = stripped(o.origin)
        if o.type == 'subscribe':
            pres = Event({'to': o["from"], 'type': 'subscribed'})
            self.client.send_presence(dict(pres))
            pres = Event({'to': o["from"], 'type': 'subscribe'})
            self.client.send_presence(dict(pres))
        elif o.type == "unavailable" and username != self.cfg.username and username in self.channels:
            self.channels.remove(username)
        elif o.origin != self.cfg.user and username != self.cfg.username and username not in self.channels:
            self.channels.append(username)
        o.txt = o.type
        kernel.put(o)

    def resume(self):
        """ method called when resuming the bot. """
        pass

    def say(self, jid, txt):
        """ say test to xmpp user. """
        txt = str(txt)
        s = stripped(jid)
        logging.debug("%s %s" % (s, txt))
        if s in self.channels:
            self.say_muc(s, txt)
            return
        self.client.send_message(jid, txt)

    def say_muc(self, to, txt):
        self.client.send_message(mto=to,
                                 mbody=txt,
                                 mtype='groupchat')

    def session_start(self, data):
        """ send a presence on startup. """
        self.client.send_presence()

    def sleek(self):
        """ server function of the xmpp bot. """
        self._connected.wait()
        if "client" in self and self.client:
            try:
                self.client.process(block=True)
            except Exception as ex:
                logging.error(get_exception())

    def stop(self):
        """ stop the xmpp bot. """
        if "client" in self and self.client:
            self.client.disconnect()
        super().stop()

    def start(self, *args, **kwargs):
        """ start the xmpp bot. """
        self.connect(cfg.jid or self.cfg.user)
        launcher.launch(self.sleek)
        super().start(*args, **kwargs)
        self.ready()
