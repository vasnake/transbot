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
(env)valik@snafu:~/translit.bot$ wget http://downloads.sourceforge.net/project/xmpppy/xmpppy/0.5.0-rc1/xmpppy-0.5.0rc1.tar.gz
(env)valik@snafu:~/translit.bot$ tar -xzvvf xmpppy-0.5.0rc1.tar.gz
(env)valik@snafu:~/translit.bot$ cd xmpppy-0.5.0rc1/
(env)valik@snafu:~/translit.bot/xmpppy-0.5.0rc1$ ../env/bin/python setup.py install
(env)valik@snafu:~/translit.bot$ cd ..
(env)valik@snafu:~/translit.bot$ pip install trans dnspython
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

import sys, os, xmpp, string, time, traceback
import translitbot.enc as enc

USER = os.environ.get("TRANSBOT_USER", "google account name@gmail.com")
PASSWORD = os.environ.get("TRANSBOT_PASSWORD", "google account passphrase")
SERVER = "gmail.com"

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


def messageHandler(sess, stanza):
    """ Process messages """
    def send(msg):
        sess.send(xmpp.Message(stanza.getFrom(), msg))
        print ("bot resp. '%s'" % msg).encode(CP)

    fromUser = stanza.getFrom().getStripped()
    inStr = (u'%s' % stanza.getBody()).strip()

    if not inStr or inStr.lower() == u'none':
        return
    print (u"user '%s' say '%s'" % (fromUser, inStr)).encode(CP)

    if inStr == u'?' or inStr.lower() == u'help' or inStr.lower() == u':help':
        send(usage())
        return

    if inStr[0] == u':':
        mode = getTransKey(inStr[1:])
        if mode:
            MODES[fromUser] = mode
            send(u"Установлен режим транслитерации по методу '%s'" % mode[0])
            return
        send(u"Незнакомая команда '%s'" % inStr)

    mode = MODES.get(fromUser, enc.DRIVELICMODE)
    outStr = enc.translit(inStr, mode)
    message = u"Mode '%s', answer is:\n%s" % (mode[0], outStr)
    send(message)
#def messageHandler(sess, stanza):


def presenceHandler(conn, pres):
    """ subscribe or unsubscribe processor """
    type=pres.getType()
    user=pres.getFrom()
    if type=='subscribe':
        conn.send(xmpp.Presence(user,'subscribed'))
    if type=='unsubscribe':
        conn.send(xmpp.Presence(user,'unsubscribed'))
#def presenceHandler(conn, pres):


def connect():
    """ Return connect from xmpp.Client() """
    jid = xmpp.JID(USER)
    #~ conn = xmpp.Client(SERVER)
    conn = xmpp.Client(SERVER, debug=[])

    print 'connect ...'
    res = conn.connect()
    print 'conn.connect() is', res

    res = conn.auth(jid.getNode(), PASSWORD, "console")
    print 'conn.auth() is', res
    if res is None:
        print "invalid login?"
        return res

    conn.RegisterHandler('message', messageHandler)
    conn.RegisterHandler('presence',presenceHandler)
    conn.sendInitPresence()

    return conn
#def connect():


def main():
    """ infinite loop """
    try:
        conn = connect()
        while conn and conn.Process(1):
            pass
    except (KeyboardInterrupt, SystemExit):
        print u'shutdown...'
        return
    except:
        print u'xmpp exception, restart after pause...'
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
    #~ import sys
    #~ reload(sys)
    #~ sys.setdefaultencoding("UTF-8")
    import doctest
    doctest.testmod(verbose=True)
#def doDocTest():


if __name__ == "__main__":
    print time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        doDocTest()
        print 'Done.'
    except Exception, e:
        print 'Error, program failed:'
        traceback.print_exc(file=sys.stderr)
    print time.strftime('%Y-%m-%d %H:%M:%S')
