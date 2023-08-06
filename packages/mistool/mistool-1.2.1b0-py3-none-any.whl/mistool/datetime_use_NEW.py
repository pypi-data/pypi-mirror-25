#!/usr/bin/env python3

"""
prototype::
    date = 2017-08-????


This script proposes easy-to-use classes for playing with dates and times.
"""

from datetime import (
    datetime,
    timedelta
)

from mistool.config.date_name import *


# ----------- #
# -- DATES -- #
# ----------- #

class HDate:
    """
prototype::
    see = HDeltaTime


HDate + HDeltaTime = HDate
HDate + HDate = INTERDIT
HDate - HDate = HDeltaTime
HDeltaTime - HDeltaTime = HDeltaTime
HDeltaTime + HDeltaTime = HDeltaTime

HDeltaTime < 0 ok !!!


not really iso becaus no T and incomplete date are accepted
    --> addition and comparison are done if this is meaningfull
        10-20 > 10-10
        10-20 <?> 2017-10-10



>>> import datetime
>>> print(datetime.datetime.strptime("2017-07-23", "%Y-%m-%d"))
2017-07-23 00:00:00

Pas fubny du tout même si a priori plu puissant


yyyy et yyyy-mm : ok mais implicite au début possible (1er mois, 1er jour)


yyyy-mm-dd


yyyy-mm-dd hh:min:s
           [HDeltaTime ok ici après 1ere espace si inférieure à une journée !!!!]
???
    """

    def __init__(self, iso, lang = 'en_GB'):
        self.lang = lang
        self.iso  = iso

        for oneattr in [
            "year", "month", "day",
            "hour", "min", "second", "microsecond"
        ]:
            self.__setattr__(oneattr, None)


    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        if value not in LANGS:
            raise ValueError(
                "unkwown language ``{0}``".format(
                    value
                )
            )

        self._lang = value


    @property
    def iso(self):
        return self._iso

    @iso.setter
    def iso(self, value):
        if not isinstance(value, str):
            raise TypeError("the attribut ``iso`` must be a string")

        date, *time = value.split(maxsplit=1)

        if time:
            time = time[0]

        else:
            time = ""

        print(">>>>>", date, time)
        self._iso = str( (date, time) )

        values = {}

        print(dir(self))
        for oneattr in [
            "year", "month", "day",
            "hour", "min", "second", "microsecond"
        ]:
            oneval = self.__dict__[oneattr]

            if oneval is not None:
                values[oneattr] = oneval

        self.datetime = datetime(**values)









    def __repr__(self):
        return "HDate(iso = '{0}', lang = '{1}')".format(
            self.iso,
            self.lang
        )

    def __str__(self):
        return self.iso





class HDeltaTime:
    """
prototype::
    see = ???


12y 1m 4d 3600s
    """
