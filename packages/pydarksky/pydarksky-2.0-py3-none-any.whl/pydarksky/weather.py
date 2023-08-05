import logging
import json
import sys
import os

__author__ = "PvtHaggard"

__license__ = "GPLv3"
__maintainer__ = "PvtHaggard"
__email__ = "pvtgaggard@gmail.com"


log = logging.getLogger("pydarksky")


class Weather:
    """
    .. Note::

        Do not assume the existence of any attribute.

    :param str json_raw: JSON string

    :var dict json: [Required] JSON data returned by the Dark Sky API
    :var float latitude: [Required] The requested latitude.
                         Maybe different from the value passed to DarkSky class.
    :var float longitude: [Required] The requested longitude.
                          Maybe different from the value passed to DarkSky class.
    :var str timezone: [Required] The IANA timezone name for the requested location.
                       This is used for text summaries and for determining when hourly
                       and daily data block objects begin.

    :var Currently currently: A class containing the current weather conditions at the requested location.

    :var list[Daily] daily: A class containing the current weather conditions at the requested location.
    :var str daily_summary: A human-readable summary of the daily data block.
    :var str daily_icon: A machine-readable text summary of the daily data block.

    :var list[Hourly] hourly: A class containing the current weather conditions day-by-day for the next week.
    :var str hourly_summary: A human-readable summary of the hourly data block.
    :var str hourly_icon: A machine-readable text summary of the daily data block.

    :var list[Minutely] minutely: A class containing the current weather conditions
                                  minute-by-minute for the next hour.
    :var str minutely_summary: A human-readable summary of the minutely data block.
    :var str minutely_icon: A machine-readable text summary of the daily data block.

    :var list[Alert] alerts: An alerts array, which, if present, contains any severe weather
                             alerts pertinent to the requested location.
    """

    def __init__(self, json_raw):
        # type:(str) -> None
        self.json = json.loads(json_raw)
        try:
            self.latitude = self.json["latitude"]
            self.longitude = self.json["longitude"]
            self.timezone = self.json["timezone"]
        except KeyError as e:
            raise RequiredDataError("JSON missing required attribute '{}'".format(e.args[0]), e.args[0])

        if "currently" in self.json:
            self.now = Now(self.json["currently"], self)

        if "daily" in self.json:
            self.daily = []
            if self.json["daily"].get("summary") is not None:
                self.daily_summary = self.json["daily"].get("summary")
            if self.json["daily"].get("icon") is not None:
                self.daily_icon = self.json["daily"].get("icon")
            for data in self.json["daily"]["data"]:
                self.daily.append(Day(data, self))

        if "hourly" in self.json:
            self.hourly = []
            if self.json["hourly"].get("summary") is not None:
                self.hourly_summary = self.json["hourly"].get("summary")
            if self.json["hourly"].get("icon") is not None:
                self.hourly_icon = self.json["hourly"].get("icon")
            for data in self.json["hourly"]["data"]:
                self.hourly.append(Hour(data, self))

        if "minutely" in self.json:
            self.minutely = []
            if self.json["minutely"].get("summary") is not None:
                self.minutely_summary = self.json["minutely"].get("summary")
            if self.json["minutely"].get("icon") is not None:
                self.minutely_icon = self.json["minutely"].get("icon")
            for data in self.json["minutely"]["data"]:
                self.minutely.append(Minute(data, self))

        if "flags" in self.json:
            self.flags = Flag(self.json["flags"], self)

        if "alerts" in self.json:
            self.alerts = []
            for data in self.json["alerts"]:
                self.alerts.append(Alert(data, self))

    def has_now(self):
        # type() -> bool
        return hasattr(self, "currently")

    def has_daily(self):
        # type() -> bool
        return hasattr(self, "daily")

    def has_hourly(self):
        # type() -> bool
        return hasattr(self, "hourly")

    def has_minutely(self):
        # type() -> bool
        return hasattr(self, "minutely")

    def has_alerts(self):
        # type() -> bool
        return hasattr(self, "alerts")


class DataBlock:
    def __init__(self, data, parent=None):
        # type:(dict, Weather) -> None
        self.parent = parent
        for field, value in data.items():
            setattr(self, field, value)

    def __getattr__(self, attribute):
        if attribute not in dir(self):
            log.debug("'{}' object has no attribute '{}'".format(self.__name__(), attribute))
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__name__(), attribute))

        log.debug("'{}' instance has no data for attribute '{}'".format(self.__name__(), attribute))
        raise NoDataError("'{}' instance has no data for attribute '{}'".format(self.__name__(), attribute),
                          attribute)


class Now(DataBlock):
    """
    .. Note::

        Do not assume the existence of any attribute.

    :var apparentTemperature:
    :var cloudCover:
    :var dewPoint:
    :var humidity:
    :var icon:
    :var nearestStormBearing:
    :var nearestStormDistance:
    :var ozone:
    :var precipIntensity:
    :var precipProbability:
    :var precipType:
    :var pressure:
    :var summary:
    :var temperature:
    :var time:
    :var uvIndex:
    :var visibility:
    :var windBearing:
    :var windGust:
    :var windSpeed:
    """
    def __init__(self, data, parent=None):
        # type:(dict, Weather) -> None
        DataBlock.__init__(self, data, parent)

    @staticmethod
    def __name__():
        return "Now"

    @staticmethod
    def __dir__():
        return sorted(["apparentTemperature", "cloudCover", "dewPoint", "humidity", "icon",
                       "nearestStormBearing", "nearestStormDistance", "ozone", "precipIntensity",
                       "precipProbability", "precipType", "pressure", "summary", "temperature", "time",
                       "uvIndex", "visibility", "windBearing", "windGust", "windSpeed"])


class Day(DataBlock):
    """
    .. Note::

        Do not assume the existence of any attribute.

    :var apparentTemperatureHigh:
    :var apparentTemperatureHighTime:
    :var apparentTemperatureLow:
    :var apparentTemperatureLowTime:
    :var cloudCover:
    :var dewPoint:
    :var humidity:
    :var icon:
    :var moonPhase:
    :var ozone:
    :var precipAccumulation:
    :var precipIntensity:
    :var precipIntensityMax:
    :var precipIntensityMaxTime:
    :var precipProbability:
    :var precipType:
    :var pressure:
    :var summary:
    :var sunriseTime:
    :var sunsetTime:
    :var temperatureHigh:
    :var temperatureHighTime:
    :var temperatureLow:
    :var temperatureLowTime:
    :var time:
    :var uvIndex:
    :var uvIndexTime:
    :var visibility:
    :var windBearing:
    :var windGust:
    :var windSpeed:
    """
    def __init__(self, data, parent=None):
        # type:(dict, Weather) -> None
        DataBlock.__init__(self, data, parent)

    @staticmethod
    def __name__():
        return "Day"

    @staticmethod
    def __dir__():
        return sorted(["apparentTemperatureHigh", "apparentTemperatureHighTime", "apparentTemperatureLow",
                       "apparentTemperatureLowTime", "cloudCover", "dewPoint", "humidity", "icon",
                       "moonPhase", "ozone", "precipAccumulation", "precipIntensity", "precipIntensityMax",
                       "precipIntensityMaxTime", "precipProbability", "precipType", "pressure", "summary",
                       "sunriseTime", "sunsetTime", "temperatureHigh", "temperatureHighTime",
                       "temperatureLow", "temperatureLowTime", "time", "uvIndex", "uvIndexTime",
                       "visibility", "windBearing", "windGust", "windSpeed"])


class Hour(DataBlock):
    """
    .. Note::

        Do not assume the existence of any attribute.

    :var apparentTemperature:
    :var cloudCover:
    :var dewPoint:
    :var humidity:
    :var icon:
    :var ozone:
    :var precipAccumulation:
    :var precipIntensity:
    :var precipProbability:
    :var precipType:
    :var pressure:
    :var summary:
    :var temperature:
    :var time:
    :var uvIndex:
    :var visibility:
    :var windBearing:
    :var windGust:
    :var windSpeed:
    """
    def __init__(self, data, parent=None):
        # type:(dict, Weather) -> None
        DataBlock.__init__(self, data, parent)

    @staticmethod
    def __name__():
        return "Hour"

    @staticmethod
    def __dir__():
        return sorted(["apparentTemperature", "cloudCover", "dewPoint", "humidity", "icon", "ozone",
                       "precipAccumulation", "precipIntensity", "precipProbability", "precipType", "pressure",
                       "summary", "temperature", "time", "uvIndex", "visibility", "windBearing",
                       "windGust", "windSpeed"])


class Minute(DataBlock):
    """
    .. Note::

        Do not assume the existence of any attribute.

    :var apparentTemperature:
    :var cloudCover:
    :var dewPoint:
    :var humidity:
    :var icon:
    :var ozone:
    :var precipIntensity:
    :var precipProbability:
    :var precipType:
    :var pressure:
    :var summary:
    :var time:
    :var uvIndex:
    :var visibility:
    :var windBearing:
    :var windGust:
    :var windSpeed:
    """
    def __init__(self, data, parent=None):
        # type:(dict, Weather) -> None
        DataBlock.__init__(self, data, parent)

    @staticmethod
    def __name__():
        return "Minute"

    @staticmethod
    def __dir__():
        return sorted(["apparentTemperature", "cloudCover", "dewPoint", "humidity", "icon", "ozone",
                       "precipIntensity", "precipProbability", "precipType", "pressure", "summary", "time",
                       "uvIndex", "visibility", "windBearing", "windGust", "windSpeed"])


class Flag:
    # TODO: Find out darksky-unavailable data type
    """
    :var darksky-unavailable: [optional] The presence of this property indicates that the Dark Sky data source
                              supports the given location, but a temporary error (such as a radar station
                              being down for maintenance) has made the data unavailable.
    :var list[str] sources: This property contains an array of IDs for each data source
                            utilized in servicing this request.
    :var units units: Indicates the units which were used for the data in this request.
    """
    def __init__(self, data, parent=None):
        # type:(dict, Weather) -> None
        self.weather = parent
        if "darksky-unavailable" in data:
            self.darksky_unavailable = data["darksky-unavailable"]

        try:
            self.sources = data["sources"]
            self.units = data["units"]
        except KeyError as e:
            raise RequiredDataError("JSON missing required attribute '{}'".format(e.args[0]), e.args[0])


class Alert:
    """
    :var str description: A detailed description of the alert.
    :var int expires: The UNIX time at which the alert will expire.
    :var str regions: An array of strings representing the names of the regions covered by this weather alert.
    :var str severity: The severity of the weather alert, will be one of the following values:


        * *advisory*
        * *watch*
        * *warning*

    :var int time: The UNIX time at which the alert was issued.
    :var str title: A brief description of the alert.
    :var str uri: A HTTP(S) URI that one may refer to for detailed information about the alert.
    """
    def __init__(self, data, parent=None):
        # type:(dict, Weather) -> None
        self.weather = parent
        try:
            self.description = data["description"]
            self.expires = data["expires"]
            self.regions = data["regions"]
            self.severity = data["severity"]
            self.time = data["time"]
            self.title = data["title"]
            self.uri = data["uri"]
        except KeyError as e:
            raise RequiredDataError("JSON missing required attribute '{}'".format(e.args[0]), e.args[0])


class NoDataError(Exception):
    def __init__(self, msg, attribute):
        super(NoDataError, self).__init__(msg)
        self.attribute = attribute


class RequiredDataError(Exception):
    def __init__(self, msg, attribute):
        super(RequiredDataError, self).__init__(msg)
        self.attribute = attribute
