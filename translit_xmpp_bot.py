#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# (c) Valik mailto:vasnake@gmail.com

u''' GTalk bot for translit rus texts using set of encode tables.
You can add translit.bot@gmail.com to your XMPP or GTalk roster and talk to him.

Tables taken from wiki: Транслитерация русского алфавита латиницей

install libs
# aptitude install python-xmpp
or
$ wget http://downloads.sourceforge.net/project/xmpppy/xmpppy/0.5.0-rc1/xmpppy-0.5.0rc1.tar.gz?use_mirror=nchc
$ tar -xzvvf  xmpppy-0.5.0rc1.tar.gz
$ cd  xmpppy-0.5.0rc1
$ sudo python setup.py install

and from http://pypi.python.org/pypi/trans
# pip install trans

links
http://habrahabr.ru/post/137089/
http://www.linuxforu.com/2012/06/use-xmpp-to-create-your-own-google-talk-client/
http://rus-linux.net/MyLDP/algol/xmpp-to-create-google-talk-client.html

Copyright (C) 2013, Valentin Fedulov
Originally by Valik <vasnake@gmail.com>, 2012
Licensed under GNU GENERAL PUBLIC LICENSE (http://www.gnu.org/licenses/gpl.txt)
'''

import sys, xmpp, string, time, traceback
import enc

USER = "translit.bot@gmail.com"
PASSWORD = "google accaunt passphrase"
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

	mode = MODES.get(fromUser, enc.ISO9MODEA)
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

	res = conn.connect()
	print res
	res = conn.auth(jid.getNode(), PASSWORD, "console")
	print res
	conn.RegisterHandler('message', messageHandler)
	conn.RegisterHandler('presence',presenceHandler)
	conn.sendInitPresence()
	return conn
#def connect():


def main():
	""" infinite loop """
	try:
		conn = connect()
		while conn.Process(1):
			pass
	except (KeyboardInterrupt, SystemExit):
		print u'shutdown...'
		return
	except:
		print u'xmpp exception, restart after pause...'
		traceback.print_exc(file=sys.stderr)
	# loop
	time.sleep(7)
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
		#~ doDocTest()
		main()
		print 'Done.'
	except Exception, e:
		if type(e).__name__ == 'COMError':
			print 'COM Error, msg [%s]' % e
		else:
			print 'Error, program failed:'
			traceback.print_exc(file=sys.stderr)
	print time.strftime('%Y-%m-%d %H:%M:%S')
