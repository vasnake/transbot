#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# (c) Valik mailto:vasnake@gmail.com

u''' Translit encode functions for rus transliterations mentioned in
wiki: Транслитерация русского алфавита латиницей

dependencies
	pip install trans

links
	http://habrahabr.ru/post/137089/

Copyright (C) 2013, Valentin Fedulov
Originally by Valik <vasnake@gmail.com>, 2012
Licensed under GNU GENERAL PUBLIC LICENSE (http://www.gnu.org/licenses/gpl.txt)

tests
>>> print translit(u'«Хилтон Хургада Плаза»', NAUCHNAYAMODE)
"Xilton Xurgada Plaza"
>>> print translit(u'абвгдеё жзийклмн опрст уфхцч шщъыь эюя', NAUCHNAYAMODE)
abvgdeë žzijklmn oprst ufxcč ššč″y′ èjuja
>>> print translit(u'abc-ABC, абвгдеё жзийклмн опрст уфхцч шщъыь эюя «!»', ISO9MODEA)
abc-ABC, abvgdeë žzijklmn oprst ufhcč šŝ″y′ èûâ «!»
>>> print translit(u'абвгдеё жзийклмн опрст уфхцч шщъыь эюя Центавр Цапля «!»', ISO9MODEB)
abvgdeyo zhzijklmn oprst ufxczch shshh``y`` e`yuya Centavr CZaplya "!"
>>> print translit(u'абвгдеё жзийклмн опрст уфхцч шщъыь эюя «!»', ISOR9MODE1)
abvgdjeë žzijklmn oprst ufchcč ššč″y′ èjuja "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', ISOR9MODE2)
abvgd ejozh zi jj klmnoprstuf khcchshshh″y′ehjuja "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', BGNMODE)
abvgd eëzh zi y klmnoprstuf khtschshshch″y′eyuya "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', BRITMODE)
abvgd eëzh zi ĭ klmnoprstuf khtschshshch″ȳ′éyuya "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', ALAMODE)
abvgd eëzh zi ĭ klmnoprstuf kht͡schshshch″y′ėi͡ui͡a "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', GOSTRMODE)
ABVGD EEZH ZI I KLMNOPRSTUF KHTCCHSHSHCH-Y-EIUIA "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', DRIVELICMODE)
abvgd eezh zi y klmnoprstuf khtschshshch'y'eyuya "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', PASSPORTMODE)
abvgd eezh zi y klmnoprstuf khtschshshch''y'eyuya "!"
>>> print translit(u'абвгд еёж зи й клмнопрстуф хцчшщъыьэюя «!»', TELEGRAMMODE)
abvgd eej zi i klmnoprstuf hcchshsc-y-eiuia "!"
>>> print translit(u'абвгдеё жзийклмн опрст уфхцч шщъыь эюя «!»', TRANSMODE)
abvgdeyo zhziyklmn oprst ufhcch shshy eyuya _!_
'''

import os, sys

#~ pth = os.path.join(os.path.dirname(__file__), 'trans')
#~ if pth not in sys.path:
	#~ sys.path.insert(0, pth)
import trans

__version__ = '1.0'
__author__ = 'Valentin Fedulov aka vasnake <vasnake@gmail.com>'

CP = 'utf-8'

# Two names because of:
# http://docs.python.org/2/library/codecs.html#codecs.register say:
# Search functions are expected to take one argument, the encoding name in all lower case letters
# http://docs.python.org/2/howto/unicode.html#the-unicode-type say:
# The unicode() constructor has the signature unicode(string[, encoding, errors]). All of its arguments should be 8-bit strings.
# Also it seems like spaces are prohibited
TRANSMODE = (u'py trans', 'pytrans')
NAUCHNAYAMODE = (u'Научная', 'nauchnaya')
ISO9MODEA = (u'ISO 9:1995, ГОСТ 7.79-2000 система А', 'iso9sysa')
ISO9MODEB = (u'ISO 9:1995, ГОСТ 7.79-2000 система Б', 'iso9sysb')
ISOR9MODE1 = (u'ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 1', 'isor9tab1')
ISOR9MODE2 = (u'ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 2', 'isor9tab2')
BGNMODE = (u'BGN/PCGN (1944)', 'bgnpcgn')
BRITMODE = (u'Британский стандарт (1958)', 'britstd')
ALAMODE = (u'ALA-LC', 'alalc')
GOSTRMODE = (u'ГОСТ Р 52535.1-2006', 'gostr')
TELEGRAMMODE = (u'Международные телеграммы', 'inttele')
DRIVELICMODE = (u'Водительское удостоверение (2000)', 'driverlic')
PASSPORTMODE = (u'Загранпаспорт (1997—2010)', 'passport')

TRANSTABS = {}
# ('translation name', 'encoder name') : (translate_table, translate_function)

def translit(inStr, mode=ISO9MODEA):
	''' Transliterate inStr according given mode
	and return encoded string.
	Strings must be in unicode.
	'''
	transtab, func = TRANSTABS.get(mode, ('',''))
	if not func:
		return inStr
	return func(inStr)

################################################################################
# encode tables

# ISO 9:1995, ГОСТ 7.79-2000 система Б
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'yo', u'ж': u'zh',
	u'з': u'z', u'и': u'i', u'й': u'j', u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'x', u'ц': u'cz',
	u'ч': u'ch', u'ш': u'sh', u'щ': u'shh', u'ъ': u'``', u'ы': u'y`', u'ь': u'`', u'э': u'e`', u'ю': u'yu',
	u'я': u'ya', u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D', u'Е': u'E', u'Ё': u'YO', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I', u'Й': u'J', u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F', u'Х': u'X', u'Ц': u'CZ',
	u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHH', u'Ъ': u'``', u'Ы': u'Y`', u'Ь': u'`', u'Э': u'E`', u'Ю': u'YU',
	u'Я': u'YA'
}

def transiso9b(inStr):
	u''' Python module trans, ISO 9:1995, ГОСТ 7.79-2000 система Б

	ц = c Рекомендуется использовать c перед буквами e, i, y, j; и cz — в остальных случаях.
	'''
	res = inStr.encode(u'trans/%s' % ISO9MODEB[1])
	res = res.replace('cze', 'ce').replace('czi', 'ci').replace('czy', 'cy').replace('czj', 'cj')
	res = res.replace('CZe', 'Ce').replace('CZi', 'Ci').replace('CZy', 'Cy').replace('CZj', 'Cj')
	res = res.replace('CZE', 'CE').replace('CZI', 'CI').replace('CZY', 'CY').replace('CZJ', 'CJ')
	res = res.replace('czE', 'cE').replace('czI', 'cI').replace('czY', 'cY').replace('czJ', 'cJ')
	return res

TRANSTABS[ISO9MODEB] = (tab, transiso9b)


# DRIVELICMODE = (u'Водительское удостоверение (2000)', 'driverlic')
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'e', u'ж': u'zh',
	u'з': u'z', u'и': u'i',
	u'й': u'y',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'kh', u'ц': u'ts', u'ч': u'ch', u'ш': u'sh', u'щ': u'shch', u'ъ': u"'",
	u'ы': u'y', u'ь': u"'", u'э': u'e', u'ю': u'yu', u'я': u'ya',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'E', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I',
	u'Й': u'Y',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'u', u'Ф': u'F',
	u'Х': u'KH', u'Ц': u'TS', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHCH', u'Ъ': u"'",
	u'Ы': u'Y', u'Ь': u"'", u'Э': u'E', u'Ю': u'YU', u'Я': u'YA'
}

def transDrivelic(inStr):
	u''' Python module trans, Водительское удостоверение (2000)

	е = ye В начале слов, а также после гласных и Ь, Ъ
	ё = yo В начале слов, а также после гласных и Ь, Ъ
	ё = e После согласных Ч, Ш, Щ, Ж.
	ё = ye После согласных, кроме Ч, Ш, Щ, Ж.
	и = yi После Ь
	'''
	res = inStr.encode(u'trans/%s' % DRIVELICMODE[1])
	return res

TRANSTABS[DRIVELICMODE] = (tab, transDrivelic)


# PASSPORTMODE = (u'Загранпаспорт (1997—2010)', 'passport')
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'e', u'ж': u'zh',
	u'з': u'z', u'и': u'i',
	u'й': u'y',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'kh', u'ц': u'ts', u'ч': u'ch', u'ш': u'sh', u'щ': u'shch', u'ъ': u"''",
	u'ы': u'y', u'ь': u"'", u'э': u'e', u'ю': u'yu', u'я': u'ya',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'E', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I',
	u'Й': u'Y',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'u', u'Ф': u'F',
	u'Х': u'KH', u'Ц': u'TS', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHCH', u'Ъ': u"''",
	u'Ы': u'Y', u'Ь': u"'", u'Э': u'E', u'Ю': u'YU', u'Я': u'YA'
}

def transPassport(inStr):
	u''' Python module trans, Загранпаспорт (1997—2010)

	е = ye После Ь
	ё = ye После Ь
	'''
	res = inStr.encode(u'trans/%s' % PASSPORTMODE[1])
	return res

TRANSTABS[PASSPORTMODE] = (tab, transPassport)


# Научная
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'ë', u'ж': u'ž',
	u'з': u'z', u'и': u'i', u'й': u'j', u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'x', u'ц': u'c',
	u'ч': u'č', u'ш': u'š', u'щ': u'šč', u'ъ': u'″', u'ы': u'y', u'ь': u'′', u'э': u'è', u'ю': u'ju',
	u'я': u'ja', u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D', u'Е': u'E', u'Ё': u'Ë', u'Ж': u'Ž',
	u'З': u'Z', u'И': u'I', u'Й': u'J', u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F', u'Х': u'X', u'Ц': u'C',
	u'Ч': u'Č', u'Ш': u'Š', u'Щ': u'ŠČ', u'Ъ': u'″', u'Ы': u'Y', u'Ь': u'′', u'Э': u'È', u'Ю': u'JU',
	u'Я': u'JA'
}

def transNauchnaya(inStr):
	u''' Python module trans, Научная encoder
	'''
	return inStr.encode(u'trans/%s' % NAUCHNAYAMODE[1])

TRANSTABS[NAUCHNAYAMODE] = (tab, transNauchnaya)


# Международные телеграммы
tab = { # Русские буквы Ъ и Ь при транслитерации телеграмм не должны применяться, соответствие для них не установлено
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'e', u'ж': u'j',
	u'з': u'z', u'и': u'i',
	u'й': u'i',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'h', u'ц': u'c', u'ч': u'ch', u'ш': u'sh', u'щ': u'sc', u'ъ': u'-',
	u'ы': u'y', u'ь': u'-', u'э': u'e', u'ю': u'iu', u'я': u'ia',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'E', u'Ж': u'J',
	u'З': u'Z', u'И': u'I',
	u'Й': u'I',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F',
	u'Х': u'H', u'Ц': u'C', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SC', u'Ъ': u'-',
	u'Ы': u'Y', u'Ь': u'-', u'Э': u'E', u'Ю': u'IU', u'Я': u'IA'
}

def transtgram(inStr):
	u''' Python module trans, Международные телеграммы

	Русские буквы Ъ и Ь при транслитерации телеграмм не должны применяться,
	соответствие для них не установлено
	'''
	return inStr.encode(u'trans/%s' % TELEGRAMMODE[1])

TRANSTABS[TELEGRAMMODE] = (tab, transtgram)


# ГОСТ Р 52535.1-2006
tab = { # По техническим причинам в документах используются только заглавные буквы
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'e', u'ж': u'zh',
	u'з': u'z', u'и': u'i',
	u'й': u'I',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'kh', u'ц': u'TC', u'ч': u'ch', u'ш': u'sh', u'щ': u'shch', u'ъ': u'-',
	u'ы': u'y', u'ь': u'-', u'э': u'E', u'ю': u'IU', u'я': u'IA',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'E', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I',
	u'Й': u'I',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F',
	u'Х': u'KH', u'Ц': u'TC', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHCH', u'Ъ': u'-',
	u'Ы': u'Y', u'Ь': u'-', u'Э': u'E', u'Ю': u'IU', u'Я': u'IA'
}

def transGOSTR(inStr):
	u''' Python module trans, ГОСТ Р 52535.1-2006

	По техническим причинам в документах используются только заглавные буквы;
	Соответствие для знаков русского алфавита Ъ и Ь не определено стандартом
	'''
	res = inStr.encode(u'trans/%s' % GOSTRMODE[1])
	return res.upper()

TRANSTABS[GOSTRMODE] = (tab, transGOSTR)


# ALA-LC
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'ë', u'ж': u'zh',
	u'з': u'z', u'и': u'i',
	u'й': u'ĭ',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'kh', u'ц': u't͡s', u'ч': u'ch', u'ш': u'sh', u'щ': u'shch', u'ъ': u'″',
	u'ы': u'y', u'ь': u'′', u'э': u'ė', u'ю': u'i͡u', u'я': u'i͡a',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'Ë', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I',
	u'Й': u'Ĭ',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F',
	u'Х': u'KH', u'Ц': u'T͡S', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHCH', u'Ъ': u'″',
	u'Ы': u'Y', u'Ь': u'′', u'Э': u'Ė', u'Ю': u'I͡U', u'Я': u'I͡A'
}

def transala(inStr):
	u''' Python module trans, ALA-LC
	'''
	res = inStr.encode(u'trans/%s' % ALAMODE[1])
	return res

TRANSTABS[ALAMODE] = (tab, transala)


# Британский стандарт (1958)
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'ë', u'ж': u'zh',
	u'з': u'z', u'и': u'i',
	u'й': u'ĭ',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'kh', u'ц': u'ts', u'ч': u'ch', u'ш': u'sh', u'щ': u'shch', u'ъ': u'″',
	u'ы': u'ȳ', u'ь': u'′', u'э': u'é', u'ю': u'yu', u'я': u'ya',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'Ë', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I',
	u'Й': u'Ĭ',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F',
	u'Х': u'KH', u'Ц': u'TS', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHCH', u'Ъ': u'″',
	u'Ы': u'Ȳ', u'Ь': u'′', u'Э': u'É', u'Ю': u'YU', u'Я': u'YA'
}

def transbrit(inStr):
	u''' Python module trans, Британский стандарт (1958)
	'''
	res = inStr.encode(u'trans/%s' % BRITMODE[1])
	return res

TRANSTABS[BRITMODE] = (tab, transbrit)


# BGN/PCGN (1944)
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'ë', u'ж': u'zh',
	u'з': u'z', u'и': u'i',
	u'й': u'y',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'kh', u'ц': u'ts', u'ч': u'ch', u'ш': u'sh', u'щ': u'shch', u'ъ': u'″',
	u'ы': u'y', u'ь': u'′', u'э': u'e', u'ю': u'yu', u'я': u'ya',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'Ë', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I',
	u'Й': u'Y',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F',
	u'Х': u'KH', u'Ц': u'TS', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHCH', u'Ъ': u'″',
	u'Ы': u'Y', u'Ь': u'′', u'Э': u'E', u'Ю': u'YU', u'Я': u'YA'
}

def transbgn(inStr):
	u''' Python module trans, BGN/PCGN (1944)

	е = ye, ё = yë В начале слов и после гласных
	'''
	res = inStr.encode(u'trans/%s' % BGNMODE[1])
	return res

TRANSTABS[BGNMODE] = (tab, transbgn)


# ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 2
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd',
	u'е': u'e', u'ё': u'jo', u'ж': u'zh',
	u'з': u'z', u'и': u'i',
	u'й': u'jj',
	u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f',
	u'х': u'kh', u'ц': u'c', u'ч': u'ch', u'ш': u'sh', u'щ': u'shh', u'ъ': u'″',
	u'ы': u'y', u'ь': u'′', u'э': u'eh', u'ю': u'ju', u'я': u'ja',
	u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
	u'Е': u'E', u'Ё': u'JO', u'Ж': u'ZH',
	u'З': u'Z', u'И': u'I',
	u'Й': u'JJ',
	u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F',
	u'Х': u'KH', u'Ц': u'C', u'Ч': u'CH', u'Ш': u'SH', u'Щ': u'SHH', u'Ъ': u'″',
	u'Ы': u'Y', u'Ь': u'′', u'Э': u'EH', u'Ю': u'JU', u'Я': u'JA'
}

def transisor92(inStr):
	u''' Python module trans, ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 2
	'''
	res = inStr.encode(u'trans/%s' % ISOR9MODE2[1])
	return res

TRANSTABS[ISOR9MODE2] = (tab, transisor92)


# ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 1
tab = {
	u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'je', u'ё': u'ë', u'ж': u'ž',
	u'з': u'z', u'и': u'i', u'й': u'j', u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
	u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'ch', u'ц': u'c',
	u'ч': u'č', u'ш': u'š', u'щ': u'šč', u'ъ': u'″', u'ы': u'y', u'ь': u'′', u'э': u'è', u'ю': u'ju',
	u'я': u'ja', u'«': u'"', u'»': u'"',
	u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D', u'Е': u'JE', u'Ё': u'Ë', u'Ж': u'Ž',
	u'З': u'Z', u'И': u'I', u'Й': u'J', u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
	u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F', u'Х': u'CH', u'Ц': u'C',
	u'Ч': u'Č', u'Ш': u'Š', u'Щ': u'ŠČ', u'Ъ': u'″', u'Ы': u'Y', u'Ь': u'′', u'Э': u'È', u'Ю': u'JU',
	u'Я': u'JA'
}

def transisor91(inStr):
	u''' Python module trans, ISO/R 9 (1968), ГОСТ 16876-71, СТ СЭВ 1362-78, ООН (1987) таблица 1

	Согласно приказу ГУГК № 231п за 1983 год и следующим ему рекомендациям ООН за 1987 год
	для е, х, ц, щ, ю, я в географических названиях используются только e, h, c, šč, ju, ja.
	'''
	res = inStr.encode(u'trans/%s' % ISOR9MODE1[1])
	return res

TRANSTABS[ISOR9MODE1] = (tab, transisor91)


# TRANSMODE = (u'py trans', 'pytrans')
def transPy(inStr):
	u''' Python module trans, py trans
	'''
	return inStr.encode('trans')

TRANSTABS[TRANSMODE] = ('', transPy)


# ISO9MODEA = (u'ISO 9:1995, ГОСТ 7.79-2000 система А', 'iso9sysa')
def transISO(inStr):
	u''' ISO 9:1995, ГОСТ 7.79-2000 система А

	http://stackoverflow.com/questions/1733414/how-do-i-include-unicode-strings-in-python-doctests
	>>> print transISO(u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
	abvgdeëžzijklmnoprstufhcčšŝ″y′èûâ
	'''
	frm = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
	frm = u'%s%s' % (frm, frm.upper())
	to = u'abvgdeëžzijklmnoprstufhcčšŝ″y′èûâ'
	to = u'%s%s' % (to, to.upper())

	tab = dict((ord(a), b) for a, b in zip(frm, to))
	#~ tab = string.maketrans(frm, to)
	res = inStr.translate(tab)
	return u'%s' % res
#def transISO

TRANSTABS[ISO9MODEA] = ('', transISO)


# register tables
for tabname, encname in TRANSTABS.keys():
	#~ print "'%s'" % tabname.encode(CP)
	transtab, func = TRANSTABS[(tabname, encname)]
	if isinstance(transtab, dict):
		transtab = ({}, transtab)
		ascii = ({}, dict(zip(trans.ascii_str, trans.ascii_str)))
		ascii[0].update(transtab[0])
		ascii[1].update(transtab[1])
		ascii[1][None] = u'_'
		trans.tables[encname] = ascii

################################################################################
# tests

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
	import traceback
	try:
		doDocTest()
	except Exception, e:
		if type(e).__name__ == 'COMError': print 'COM Error, msg [%s]' % e
		else:
			print 'Error, program failed:'
			traceback.print_exc(file=sys.stderr)
