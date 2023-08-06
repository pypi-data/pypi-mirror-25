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
    version='29',
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

BOTLIB is a python3 framework to use if you want to program CLI, IRC or XMPP bots.

| object class	 	- save/load to/from a json file.
| rest server 		- serve saved object’s over http.
| rss fetcher 		- echo rss feeds to irc channels.
| udp server 		- udp to bot to irc channel.
| watcher server 	- run tail -f and have output send to IRC channel.
| email scanning 	- scan mbox format to searchable botlib objects.
| json backend 		- objects are stored as json string in files on the fs.
| db			- iteration over stored objects.
| timestamp		- time based filenames gives logging capabilities
| future		- future sensors should provide entry to the logger.

source:

:: 

 bart@okdan:~$ hg clone https://bitbucket.org/bthate/botlib

 You might need to do one of the following if the bot doesn't work:

 bart@okdan:~/botlib$ export PYTHONPATH="."
 bart@okdan:~/botlib$ export PYTHONIOENCODING="utf-8"

Another option is to download with pip3 and install globally:

::

 bart@okdan:~$ pip3 install botlib --upgrade

usage:

Use -n <nick>, -s <server>, -c <channel> options to make the bot join the network:

::

 bart@okdan:~$ bot -i irc -n botlib -s irc.freenode.net -c \#botlib

You can use the -w option to write config values to ~/.bot/config/irc

For the xmpp server use a ~/.sleekpass file with the password in it:

::

 bart@okdan:~$ cat "password" > ~/.sleekpass
 bart@okdan:~$ bot -i xmpp,rss --room=test@conference.localhost

modules:

::

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
    botlib.wisdom

contact:

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com

BOTLIB has a MIT license`


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
