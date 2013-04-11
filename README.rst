=========================
The **translit** xmpp bot
=========================

This xmpp bot converts Russian text into Latin script (transliteration).
The list of encode tables available by ':help' command.

.. contents::

Usage
------------
Change account settings in the file translit_xmpp_bot.py::

  USER = "translit.bot@gmail.com"
  PASSWORD = "google accaunt passphrase"
  SERVER = "gmail.com"
  
and start bot::

  python ./translit_xmpp_bot.py

Or use module enc.py
  >>> import enc
  >>> outStr = enc.translit(inStr, enc.ISO9MODEA)

Or make chat with my bot 'translit.bot@gmail.com'

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
