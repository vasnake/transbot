=========================
The **translit** xmpp bot
=========================

This xmpp bot converts russian text into latin script (transliteration).
The list of encode tables available by ':help' command.

Tested on Python 2.7

.. contents::

Usage
-----

Install package using setuptools, virtualenv::

    mkdir transbot
    cd transbot
    virtualenv --python=python2.7 env
    source env/bin/activate
    pip install git+git://github.com/vasnake/transbot.git@master
    # or download package and exec
    python setup.py install

Change account settings in the file translit_xmpp_bot.py::

    USER = "translit.bot@gmail.com"
    PASSWORD = "google account passphrase"
    SERVER = "gmail.com"

or set environment vars for using GTalk account::

    export TRANSBOT_USER='bot name@gmail.com'
    export TRANSBOT_PASSWORD='secret'
    export TRANSBOT_SERVER='gmail.com'
    export PYTHONIOENCODING=UTF-8

and start bot::

    python -m translitbot

Or you can just use module enc.py in your code::

    >>> import translitbot.enc as enc
    >>> inStr = u'опля'
    >>> outStr = enc.translit(inStr, enc.DRIVELICMODE)

Or make chat with my bot `xmpp:translit.bot@gmail.com`

For detaching program from console (daemon mode) you can use screen command.
For example::

    screen -d -R transbot

Encoders
--------
Transliteration can be done with those tables

+ py trans https://github.com/zzzsochi/trans
+ ALA-LC
+ BGN/PCGN (1944)
+ ISO 9:1995, ГОСТ 7.79-2000 система А
+ ISO 9:1995, ГОСТ 7.79-2000 система Б
+ ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 1
+ ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 2
+ Британский стандарт (1958)
+ Водительское удостоверение (2000)
+ ГОСТ Р 52535.1-2006
+ Загранпаспорт (1997—2010)
+ Международные телеграммы
+ Научная

All this tables has been taken from `<http://ru.wikipedia.org/wiki/Транслитерация_русского_алфавита_латиницей>`_
except 'py trans'.
