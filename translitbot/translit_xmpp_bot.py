#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# (c) Valik mailto:vasnake@gmail.com

u''' Translitbot is XMPP bot for translit rus texts using set of encode tables.
You can add translit.bot@gmail.com to your XMPP or GTalk roster and talk to him.

Tables taken from wiki: Транслитерация русского алфавита латиницей


Install example
valik@snafu:~$ mkdir ~/translit.bot; pushd ~/translit.bot
valik@snafu:~/translit.bot$ virtualenv --no-site-packages env
valik@snafu:~/translit.bot$ source env/bin/activate
(env)valik@snafu:~/translit.bot$ pip install trans dnspython pydns sleekxmpp
(env)valik@snafu:~/translit.bot$ wget https://github.com/vasnake/transbot/archive/master.zip
(env)valik@snafu:~/translit.bot$ unzip -j master.zip

Run
$ export TRANSBOT_USER='your gtalk acc@gmail.com'
$ export TRANSBOT_PASSWORD='your secret'
$ python -m translitbot


links
http://habrahabr.ru/post/137089/
http://www.linuxforu.com/2012/06/use-xmpp-to-create-your-own-google-talk-client/
http://rus-linux.net/MyLDP/algol/xmpp-to-create-google-talk-client.html


Copyright 2012-2014 Valentin Fedulov

This file is part of Translitbot.

Translitbot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Translitbot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Translitbot. If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import os
import string
import time
import traceback

import sleekxmpp

import translitbot.enc as enc

USER = os.environ.get("TRANSBOT_USER", "google account name@gmail.com")
PASSWORD = os.environ.get("TRANSBOT_PASSWORD", "google account passphrase")
SERVER = os.environ.get("TRANSBOT_SERVER", "gmail.com")

CP = 'utf-8'

MODES = {}
# translit modes for users


def usage():
    """ Help message """
    txt = u"Присылайте команду или текст. Команды начинаются с символа ':' и могут быть такими"
    txt += u"\n%s" % u'help'
    for encname, enccode in sorted(enc.TRANSTABS.keys()):
        txt += u"\n%s" % encname
    return txt
#def usage():


def getTransKey(transname):
    """ Return None or tuple ('translation name', 'encoder name')
    from encoders
    """
    for encname, enccode in enc.TRANSTABS.keys():
        if transname.lower() == encname.lower():
            return (encname, enccode)
    return None
#def getTransKey(inStr):


def makeResponce(userName, inStr):
    """Return responce (string) to input message inStr for user userName.
    """
    res = u''

    userName, inStr = (userName.strip(), inStr.strip())
    print(u"user '%s' say '%s'" % (userName, inStr))

    # empty input
    if not inStr or inStr.lower() == u'none':
        return res

    # help commands
    if inStr == u'?' or inStr.lower() == u'help' or inStr.lower() == u':help':
        res = usage()
        return res

    # set mode command
    if inStr[0] == u':':
        mode = getTransKey(inStr[1:])
        if mode:
            MODES[userName] = mode
            res = u"Установлен режим транслитерации по методу '%s'" % mode[0]
            return res
        else:
            res = u"Незнакомая команда '%s'" % inStr
            return res

    # translit text
    mode = MODES.get(userName, enc.DRIVELICMODE)
    outStr = enc.translit(inStr, mode)
    res = u"Mode '%s', answer is:\n%s" % (mode[0], outStr)
    return res
#def makeResponce(userName, inStr):


class TranslitBot(sleekxmpp.ClientXMPP):
    """A simple SleekXMPP chat bot that will translit messages it receives.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        # https://github.com/fritzy/SleekXMPP/wiki/Roster-Management
        self.auto_authorize = True
        self.auto_subscribe = True


    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        try:
            print(u"\n message type '%s'" % msg['type'])
            if msg['type'] in ('chat', 'normal'):
                print("make responce...")
                resp = makeResponce(u'%s' % msg['from'], u'%s' % msg['body'])
                if resp:
                    print(u"responce is '%s'" % resp)
                    msg.reply(resp).send()
                else:
                    print(u"responce is empty")
            else:
                print("service message, skip it")
        except:
            print u'TranslitBot.messge failed:'
            traceback.print_exc(file=sys.stderr)
#class TranslitBot(sleekxmpp.ClientXMPP):


def main():
    """Infinite loop - create XMPP bot and connect it to server.
    """
    try:
        xmpp = TranslitBot(USER, PASSWORD)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0199') # XMPP Ping
        #~ xmpp.register_plugin('xep_0004') # Data Forms
        #~ xmpp.register_plugin('xep_0060') # PubSub

        if xmpp.connect(): # if xmpp.connect(('talk.google.com', 5222)):
            print("connected, process messages...")
            xmpp.process(block=True)
            print("xmpp.process done")
        else:
            print("unable to connect.")

    except (KeyboardInterrupt, SystemExit):
        print u'shutdown...'
        return
    except:
        print u'app exception, restart after pause...'
        traceback.print_exc(file=sys.stderr)

    # loop
    print u"will wait and try again..."
    time.sleep(61)
    main()
#def main():


def doDocTest():
    ''' http://docs.python.org/library/doctest.html
    http://stackoverflow.com/questions/1733414/how-do-i-include-unicode-strings-in-python-doctests
    '''
    import doctest
    doctest.testmod(verbose=True)
#def doDocTest():


if __name__ == "__main__":
    print time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        doDocTest()
        print 'Done.'
    except Exception as e:
        print 'Error, program failed:'
        traceback.print_exc(file=sys.stderr)
    print time.strftime('%Y-%m-%d %H:%M:%S')
