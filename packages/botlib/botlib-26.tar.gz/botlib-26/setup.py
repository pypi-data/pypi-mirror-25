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
    version='26',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program bots",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["sleekxmpp==1.3.1", "feedparser>=5.2.1", "dnspython", "pyasn1_modules","pyasn1>=0.3.2"],
    scripts=["bin/bot", "bin/bot-do", "bin/bot-local", "bin/bot-udp"],
    packages=['botlib'],
    extra_path="botlib",
    long_description='''

BOTLIB is a python3 framework to use if you want to program IRC or XMPP bots.

| 13:58 <@botfather> hg clone https://bitbucket.org/bthate/botlib
| 14:54 <@botfather> ./bin/bot cfg irc server <name>
| 14:54 <@botfather> ./bin/bot cfg irc channel <name>
| 14:32 <@botfather> ./bin/bot -u -i irc -l info 

provides:

| CLI, IRC and XMPP bots.

| Object class 		- save/load to/from a JSON file.
| ReST server 		- serve saved object’s over HTTP.
| RSS fetcher 		- echo rss feeds to IRC channels.
| UDP server 		- udp to bot to IRC channel.
| Watcher server 	- run tail -f and have output send to IRC channel.
| Email scanning 	- scan mbox format to searchable BOTLIB objects.
| JSON backend 		- objects are stored as json string in files on the fs.
| Db	 		- iteration over stored objects.
| Timestamp		- time based filenames gives logging capabilities
| Future		- future sensors should provide entry to the logger.

setup:

| Set export PYTHONPATH=”.” if the bot cannot be found by the python interpreter.
| Set export PYTHONIOENCODING=”utf-8” if your shell has problems with handling utf-8 strings.
| For the XMPP server use a ~/.sleekpass file with the password in it

source:

| botlib		- botlib package.
| botlib.bot		- bot base class.
| botlib.cli 		- command line interfacce bot, gives a shell prompt to issue bot commands.
| botlib.clock 		- timer, repeater and other clock based classes.
| botlib.cmnds 		- botlib basic commands.
| botlib.compose 	- construct a object into it’s type.
| botlib.engine 	- select.epoll event loop, easily interrup_table esp. versus a blocking event loop.
| botlib.db 		- JSON file db.
| botlib.error 		- botlib exceptions.
| botlib.event 		- event handling classes.
| botlib.fleet 		- fleet is a list of bots.
| botlib.handler 	- schedule events.
| botlib.irc 		- IRC bot class.
| botlib.kernel 	- program boot and module loading.
| botlib.launcher 	- a launcher launches threads (or tasks in this case).
| botlib.log 		- log module to set standard format of logging.
| botlib.object 	- JSON file backed object with dotted access.
| botlib.raw 		- raw output using print.
| botlib.rss 		- rss module.
| botlib.selector 	- functions used in code to select what objects to use.
| botlib.task 		- adapted thread to add extra functionality to threads.
| botlib.trace 		- functions concering stack trace.
| botlib.users 		- class to access user records.
| botlib.xmpp 		- XMPP bot class.
| botlib.register 	- object with list for multiple values.
| botlib.rest 		- rest interface.
| botlib.runner 	- threaded loop to run tasks on.
| botlib.space 		- central module to store objects in.
| botlib.static 	- static definitions.
| botlib.template 	- cfg objects containing default values for various services and plugins.
| botlib.test 		- plugin containing test commands and classes.
| botlib.udp 		- relay txt through a udp port listener.
| botlib.utils 		- lib local helper functions.
| botlib.url 		- functions that fetch data from url.
| botlib.watcher 	- watch files.

contact:

| Bart Thate
| botfather on #dunkbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com

BOTLIB has a MIT license - https://bitbucket.org/bthate/botlib


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
