#!/usr/bin/env python3

"""
prototype::
    date = 2017-09-13


???????


This script contains two functions to ease the use of the package ``datetime``.
"""

from copy import deepcopy
from datetime import *

from dateutil.parser import (
    parse as _parsedate,
    parserinfo as _ParserInfo
)

from mistool.config.date_name import *


# --------------------------------------------------- #
# -- ENHANCED VERSION OF ``dateutil.parser.parse`` -- #
# --------------------------------------------------- #

_PARSER_INFOS_USED = {}

def _buildnamesparsed(lang, lowformat):
    return list(
        zip(
            POINTERS[FORMATS_TRANSLATIONS[lowformat][lang]],
            POINTERS[FORMATS_TRANSLATIONS[lowformat.upper()][lang]]
        )
    )

def _buildnewparserinfo(lang):

    # ajout du support de
    #
    #     HMS = [('h', 'hour', 'hours'), ('m', 'minute', 'minutes'), ('s', 'second', 'seconds')]
    #
    #     et (cf 1ER août par exemple)
    #
    #     JUMP = [' ', '.', ',', ';', '-', '/', "'",
    #     'at', 'on', 'and', 'ad', 'm', 't', 'of', 'st', 'nd', 'rd', 'th']
    #

    class _NewParserInfo(_ParserInfo):
        WEEKDAYS = _buildnamesparsed(
            lang      = lang,
            lowformat = '%a'
        )

        MONTHS = _buildnamesparsed(
            lang      = lang,
            lowformat = '%b'
        )

        JUMP = [' ', '.', ',', ';', '-', '/', "'", "à", "et", "du", "er"]

    _PARSER_INFOS_USED[lang] = deepcopy(_NewParserInfo())


def parsedate(timestr, lang = "en_GB"):
    """
prototype::
    see = dateutil.parser.parse


????????????
    """
    if lang == "en_GB":
        return _parsedate(timestr)

    elif lang not in LANGS:
        raise ValueError(
            'illegal value << {0} >> for the argument ``lang``.'.format(lang)
        )

    elif lang not in _PARSER_INFOS_USED:
        _buildnewparserinfo(lang)

    return _parsedate(
        timestr    = timestr,
        parserinfo = _PARSER_INFOS_USED[lang]
    )


# -------------------------------------- #
# -- ENHANCED VERSION OF ``datetime`` -- #
# -------------------------------------- #

def build_ddatetime(*args, **kwargs):
    """
prototype::
    see = ddatetime



mutiformat support for date without words

Friday 01 august 2017
ok car parsedate appelé avec argu patrdéfaut
mais di coup
Vendredi 1er août 2017
rejeté penser à utiliser parsedate dans ce cas !!!!
    """
    datetime_version = None

# One single argument
    if len(args) == 1:
        onearg = args[0]

        if isinstance(onearg, (tuple, list)):
            datetime_version = datetime(*onearg)

        elif isinstance(onearg, str):
            datetime_version = parsedate(onearg)

        elif isinstance(onearg, datetime):
            datetime_version = onearg

        else:
            raise TypeError(
                "unsupported single argument with type ``{0}``".format(
                    type(onearg)
                )
            )

# Several arguments used.
    else:
        datetime_version = datetime(*args, **kwargs)

# From a datetime object to a DDateTime object.
    kwargs = {
        oneattr: getattr(datetime_version, oneattr)
        for oneattr in [
            "year", "month", "day",
            "hour", "minute", "second", "microsecond",
            "tzinfo"
        ]
    }

    return ddatetime(**kwargs)


class ddatetime(datetime):
    """
prototype::
    see = build_ddatetime

    type = cls ;
           ???


?????
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

# -- SPECIAL DATES -- #

    def nextday(self, name):
        """
prototype::
    see = datetime

    arg = datetime.date: date ;
          the date
    arg = str: name ;
          the english long name of the day wanted

    return = datetime.date ;
             the date of the next day with name equal to the value of ``name``


In some applications, you have a date and you want to find the nearest coming
day given by its name, for example the next nearest sunday after november the
30th of the year 2013. You can achieve this using a code like the one above
(the local settings of the computer used were english ones).

pyterm::
    >>> from dateutil.parser import parse as parsedate
    >>> from mistool.datetime_use import nextday
    >>> onedate = parsedate("2017-08-01")  # This is a ``datetime`` object.
    >>> print(oneself.strftime("%Y-%m-%d is a %A."))
    2017-08-01 is a Tuesday.
    >>> nextsunday = nextday(date = onedate, name = "friday")
    >>> print("Next Friday:", nextsunday.strftime("%Y-%m-%d"))
    Next Friday: 2017-08-04


info::
    The simple but efficient method used in the code was found in cf::``this
    discussion ; http://stackoverflow.com/a/6558571/1054158``.
    """
        name = name.lower()

        if name not in WEEKDAYS:
            raise ValueError("illegal day name ``{0}``.".format(name))

        daysahead = WEEKDAYS[name] - self.weekday()

        if daysahead <= 0:
            daysahead += 7

        return build_ddatetime(self + timedelta(daysahead))

# -- TRANSLATING -- #

    def translate(self, strformat, lang = 'en_GB'):
        """
prototype::
    see = datetime

    arg = datetime.date: date ;
          the date
    arg = str: strformat ;
          this string follows the special formatters available in the method
          ``strftime`` of the class ``datetime.date``.
    arg = str: lang = DEFAULT_LANG ;
          this defines the language to use, the syntax is the one of the
          function ``locale.setlocale`` of the standard package ``locale``.

    return = str ;
             the date formatting by ``strftime`` but with the name translating
             regarding to the value of ``lang``


The aim of this function is to avoid the use of something like in the following
code (the documentation of the standard package ``locale`` avoids to do that
kind of things).

pyterm::
    >>> import locale
    >>> import datetime
    >>> print (datetime.date(2015, 6, 2).strftime("%A %d %B %Y"))
    Tuesday 02 June 2015
    >>> locale.setlocale(locale.LC_ALL, 'fr_FR')
    'fr_FR'
    >>> print (datetime.date(2015, 6, 2).strftime("%A %d %B %Y"))
    Mardi 02 juin 2015


The same thing can be achieved using the function ``translate`` like in the
following lines of code (the mechanism used in backstage is very basic : it
never calls the standard package ``locale``).

pyterm::
    >>> import datetime
    >>> from mistool.datetime_use import translate
    >>> onedate   = datetime.date(2015, 6, 2)
    >>> oneformat = "%A %d %B %Y"
    >>> print(translate(date = onedate, strformat = oneformat))
    Tuesday 02 June 2015
    >>> print(translate(date = onedate, strformat = oneformat, lang = "fr_FR"))
    Mardi 02 juin 2015
"""
        if lang not in LANGS:
            raise ValueError(
                'illegal value << {0} >> for the argument ``lang``.'.format(lang)
            )

        nbday   = self.weekday()
        nbmonth = self.month - 1

        for nbid, formats in [
            (nbday  , ('%a', '%A')),
            (nbmonth, ('%b', '%B'))
        ]:
            for oneformat in formats:
                if oneformat in strformat:
                    name = POINTERS[
                        FORMATS_TRANSLATIONS[oneformat][lang]
                    ][nbid]

                    strformat = strformat.replace(oneformat, name)

        return self.strftime(strformat)
