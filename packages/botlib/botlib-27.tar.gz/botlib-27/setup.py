#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BOTLIB Framework to program bots
#
# setup.py
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

""" botlib setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run BOTLIB with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='botlib',
    version='27',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["sleekxmpp==1.3.1", "feedparser>=5.2.1", "dnspython", "pyasn1_modules","pyasn1>=0.3.2"],
    scripts=["bot", "bin/bot-do", "bin/bot-local", "bin/bot-udp"],
    packages=['botlib'],
    extra_path="botlib",
    long_description='''
BOTLIB is a python3 framework to use if you want to program IRC or XMPP bots.

| bart@okdan:~$ hg clone https://bitbucket.org/bthate/botlib
| bart@okdan:~$ cd botlib/
| bart@okdan:~/botlib$ ./bin/bot -i irc -n botlib -s irc.freenode.net -c \#botlib
| bart@okdan:~/botlib$ ./bin/bot -i xmpp,rss --room=test@conference.localhost

provides:

| CLI, IRC and XMPP bots.

| Object class	 	- save/load to/from a JSON file.
| ReST server 		- serve saved object’s over HTTP.
| RSS fetcher 		- echo rss feeds to IRC channels.
| UDP server 		- udp to bot to IRC channel.
| Watcher server 	- run tail -f and have output send to IRC channel.
| Email scanning 	- scan mbox format to searchable BOTLIB objects.
| JSON backend 		- objects are stored as json string in files on the fs.
| Db 			- iteration over stored objects.
| Timestamp		- time based filenames gives logging capabilities
| Future		- future sensors should provide entry to the logger.

setup
=====

One can choose from the following modules:

cli,irc,rest,rss,udp,watcher,xmpp

You might need to do one of the following if the bot doesn't work:

| Set export PYTHONPATH=”.” if the bot cannot be found by the python interpreter.
| Set export PYTHONIOENCODING=”utf-8” if your shell has problems with handling utf-8 strings.
| For the XMPP server use a ~/.sleekpass file with the password in it

source
======

.. autosummary::
    :toctree: botlib
    :template: module.rst

    botlib.bot
    botlib.cli
    botlib.clock
    botlib.cmnds
    botlib.compose
    botlib.engine
    botlib.db
    botlib.error
    botlib.event
    botlib.fleet
    botlib.handler
    botlib.irc
    botlib.kernel
    botlib.launcher
    botlib.log
    botlib.object
    botlib.raw
    botlib.rss
    botlib.selector
    botlib.task
    botlib.trace
    botlib.users
    botlib.xmpp
    botlib.register
    botlib.rest
    botlib.runner
    botlib.space
    botlib.static
    botlib.template
    botlib.test
    botlib.udp
    botlib.utils
    botlib.url
    botlib.watcher
    botlib.worker

contact
=======

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com

BOTLIB has a MIT :ref:`license <license>` - https://bitbucket.org/bthate/botlib


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
