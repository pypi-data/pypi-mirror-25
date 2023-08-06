# -*- coding: utf-8 -*-
import requests
import logging
from datetime import datetime

from .weather import Weather

__author__ = "PvtHaggard"

__license__ = "GPLv3"
__maintainer__ = "PvtHaggard"
__email__ = "pvtgaggard@gmail.com"


log = logging.getLogger("pydarksky")

# TODO: Add ability to handle timezones
# TODO: date_time should also take an unix timestamp
"""
Not entirely sure how this would work.
Given that Darksky.net with use the locations timezone by default, the timestamp should be ETC/UTC time or
local time and timezone. I don't know, timezones are confusing.
"""


class DarkSky(object):
    """
    :param str api_key: Darksky.net API key

    :var str api_key: Darksky.net API key
    :var float latitude: The requested latitude. Maybe different from the value returned from an API request
    :var float longitude: The requested longitude. Maybe different from the value returned from an API request
    :var datetime or str or int date: The requested date/time.
    :var bool extend:
    :var str url:
    :var int api_call_count:
    :var str response_time: Server response time in ms
    :var str response_date: Response date and time
    :var str units: API response units type
    :var str lang: API call response language
    :var list[str] excludes: Data blocks to be excluded in API response

    :var tuple[str] UNITS: Valid Dark Sky API response units
    :var list[str] LANGS: Valid Dark Sky API response languages
    :var tuple[str] EXCLUDES: Valid Dark Sky API data block exclusions
    """
    _LANGS = {"auto": "auto", "Arabic": "ar", "Azerbaijani": "az", "Belarusian": "be", "Bulgarian": "bg",
              "Bosnian": "bs", "Catalan": "ca", "Czech": "cs", "German": "de", "Greek": "el", "English": "en",
              "Spanish": "es", "Estonian": "et", "French": "fr", "Croatian": "hr", "Hungarian": "hu",
              "Indonesian": "id", "Italian": "it", "Icelandic": "is", "Georgian": "ka", "Cornish": "kw",
              "Norwegian Bokmål": "nb", "Dutch": "nl", "Polish": "pl", "Portuguese": "pt", "Russian": "ru",
              "Slovak": "sk", "Slovenian": "sl", "Serbian": "sr", "Swedish": "sv", "Tetum": "tet",
              "Turkish": "tr", "Ukrainian": "uk", "Igpay Atinlay": "x-pig-latin", "simplified Chinese": "zh",
              "traditional Chinese": "zh-tw"}

    def __init__(self, api_key=None):
        log.debug("Caution: Logging at debug level may expose API key")

        self._api_key = None
        self._latitude = None
        self._longitude = None
        self._response = None
        self._weather = None
        self._date = None
        self._lang = self._LANGS["auto"]
        self._units = "auto"
        self._extend = False
        self._exclude = []

        self.api_key = api_key

    @property
    def api_key(self):
        # type:() -> str
        return self._api_key

    @property
    def latitude(self):
        # type:() -> float
        return self._latitude

    @property
    def longitude(self):
        # type:() -> float
        return self._longitude

    @property
    def url(self):
        # type:() -> str
        """
        Build and returns a URL used to make a Dark Sky API call.
        """
        url = "https://api.darksky.net/forecast/{key}/{lat},{lon}".format(key=self.api_key,
                                                                          lat=self.latitude,
                                                                          lon=self.longitude)

        if isinstance(self._date, datetime):
            url += ",{:%Y-%m-%dT%H:%M:%S}".format(self._date)

        url += "?units={}".format(self.units)

        if self.lang != "auto":
            url += "&lang={}".format(self.lang)

        if len(self._exclude) > 0:
            url += "&exclude="
            for e in self._exclude:
                url += "{},".format(e)
            url = url.strip(",")

        if self._extend:
            url += "&extend=hourly"

        return url

    @property
    def extend(self):
        # type:() -> bool
        return self._extend

    @property
    def exclude(self):
        # type:() -> list
        return self._exclude

    @property
    def EXCLUDES(self):
        # type:() -> tuple
        return "currently", "minutely", "hourly", "daily", "alerts", "flags"

    @property
    def api_call_count(self):
        # type:() -> str
        return self._response.headers["x-forecast-api-calls"]

    @property
    def response_time(self):
        # type:() -> str
        return self._response.headers["x-response-time"]

    @property
    def response_date(self):
        # type:() -> str
        return self._response.headers["date"]

    @property
    def response_status_code(self):
        # type:() -> int
        return self._response.status_code

    @property
    def LANGS(self):
        # type:() -> list
        keys = list(self._LANGS.keys())
        keys.sort()
        return keys

    @property
    def lang(self):
        # type:() -> str
        return self._lang

    @property
    def UNITS(self):
        # type:() -> tuple
        return "auto", "ca", "uk2", "ui", "si"

    @property
    def units(self):
        # type:() -> str
        return self._units

    @property
    def date(self):
        # type:() -> datetime
        return self._date

    @api_key.setter
    def api_key(self, api_key):
        # type:(str) -> None
        api_key = str(api_key)

        if len(api_key) != 32:
            log.debug("api_key must be 32 characters long.")
            raise ValueError("api_key must be 32 characters long.")

        self._api_key = api_key

    @latitude.setter
    def latitude(self, latitude):
        # type:(float) -> None
        self._latitude = float(latitude)

    @longitude.setter
    def longitude(self, longitude):
        # type:(float) -> None
        self._longitude = float(longitude)

    @extend.setter
    def extend(self, extend):
        # type:(str) -> None
        self._extend = bool(extend)

    @exclude.setter
    def exclude(self, excludes):
        # type:(list) -> None
        if isinstance(excludes, str):
            if excludes in self.EXCLUDES:
                self._exclude = [excludes]
            else:
                log.debug("'{}' is not a valid exclude value".format(exclude))
                raise ValueError("'{}' is not a valid exclude value".format(exclude))
        elif isinstance(excludes, list):
            # Done this way to so self._exclude is not overridden if there is an exception
            _e = []
            for exclude in excludes:
                if exclude in self.EXCLUDES:
                    _e.append(exclude)
                else:
                    log.debug("'{}' is not a valid exclude value".format(exclude))
                    raise ValueError("'{}' is not a valid exclude value".format(exclude))
            self._exclude = _e
        elif excludes is None:
            self._exclude = None
        else:
            log.debug("excludes must be type '<class 'list'>' or '<class 'str'>' is type '{}'".format(type(excludes)))
            raise TypeError("excludes must be type '<class 'list'>' or '<class 'str'>' is type '{}'".format(type(excludes)))

    @lang.setter
    def lang(self, language):
        # type:(str) -> None
        if language in self._LANGS.keys():
            self._lang = self._LANGS[language]
        elif language in self._LANGS.values():
            self._lang = language
        else:
            raise ValueError("'{}' is not a valid response language".format(language))

    @units.setter
    def units(self, unit):
        # type:(str) -> None
        if unit not in self.UNITS:
            raise ValueError("'{}' is not a valid unit type".format(unit))
        self._units = unit

    @date.setter
    def date(self, date):
        # type:(datetime) -> None
        if isinstance(date, datetime) or date is None:
            self._date = date
        else:
            log.debug("date must be type '<class 'datetime'>' is type '{}'".format(type(date_time)))
            raise TypeError("date must be type '<class 'datetime'>' is type '{}'".format(type(date_time)))

    def weather(self, latitude=None, longitude=None, date=None):
        # type:(float, float, datetime) -> Weather
        """
        :param float latitude: Locations latitude
        :param float longitude: Locations longitude
        :param datetime or str or int date: Date/time for historical weather data

        :raises requests.exceptions.HTTPError: Raises on bad http response
        :raises TypeError: Raises on invalid param types

        :rtype: Weather

        Example uses

        .. code-block:: python

            # DarkSky instantiation
            >>> darksky = pydarksky.DarkSky(api_key)

            # Pre-define values
            >>> darksky.latitude = -34.9285
            >>> darksky.longitude = 138.6005
            >>> weather = darksky.weather()

            # Pass values as params
            >>> weather = darksky.weather(latitude=-34.9285, longitude=138.6005)

            # Pass values from dict
            >>> kwargs = {"longitude": 138.6005, "latitude": -34.9285}
            >>> weather = darksky.weather(**kwargs)
        """

        # If params are default(None) check if latitude/longitude have already been defined(Not None)
        # Otherwise TypeError is raised
        if latitude is None:
            if self.latitude is None:
                raise TypeError("latitude must be type '<class 'str'>' is None")
        else:
            self.latitude = latitude

        if longitude is None:
            if self.longitude is None:
                raise TypeError("longitude must be type '<class 'str'>' is None")
        else:
            self.longitude = longitude

        self._date = date

        url = self.url

        log.debug(url)

        self._response = requests.get(url, headers={"Accept-Encoding": "gzip"}, timeout=5)
        self._response.raise_for_status()

        self._weather = Weather(self._response.text)
        return self._weather

    def weather_last(self):
        # type:() -> Weather
        """
        Weather data from the last successful weather() call.

        :rtype: Weather or None
        """
        return self._weather

    def exclude_invert(self):
        # type:() -> None
        """
        Inverts the values in self.exclude

        .. code-block:: python

            >>> import pydarksky
            >>> darksky = pydarksky.DarkSky('0' * 32)

            >>> darksky.EXCLUDES
            ('currently', 'minutely', 'hourly', 'daily', 'alerts', 'flags')

            >>> darksky.exclude = ["alerts", "flags"]

            >>> darksky.exclude
            ['alerts', 'flags']

            >>> darksky.exclude_invert()

            >>> darksky.exclude
            ['currently', 'minutely', 'hourly', 'daily']

        """
        tmp = self.exclude
        self._exclude = []
        for i in self.EXCLUDES:
            if i not in tmp:
                self._exclude.append(i)


def weather(api_key, latitude, longitude, date_time=None):
    # type:(str, float, float) -> Weather
    """
    This is a shortcut method that can be used to perform a basic weather request with the default settings.

    :param str api_key: Darksky.net API key
    :param float latitude: The requested latitude. Maybe different from the value returned from an API request
    :param float longitude: The requested longitude. Maybe different from the value returned from an API request
    :param date_time: The requested date/time.

    :rtype: Weather
    """
    return DarkSky(api_key).weather(latitude, longitude, date_time)
