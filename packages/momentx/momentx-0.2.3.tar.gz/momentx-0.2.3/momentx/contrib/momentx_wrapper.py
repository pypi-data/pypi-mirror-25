# -*- encoding: utf-8 -*-

from momentx import MomentX

# create a class if you need to support multiple default timezones or restricy
class MomentXWrapper(object):
    """
    Simple wrapper for momentx.

    1) wrapped the moment api to set a custom default_timezone
    2) additionally you may set a fixed 'now' which makes now()/utcnow() a
    constant during the lifetime of MomentXWrapper. This might also be convenient
    for testing
    """

    def __init__(self, default_timezone="UTC", now=None):
        self.default_timezone = default_timezone
        if now:
            self.args_now = [now]
        else:
            self.args_now = []

    def date(self, *args, **kwargs):
        """Create a moment using the default timezone as default."""
        return MomentX(*args, timezone=kwargs.get("timezone", self.default_timezone))

    def now(self, **kwargs):
        """Create a date from the present time."""
        return MomentX(*self.args_now, timezone=kwargs.get("timezone", self.default_timezone))

    def utc(self, *args, **kwargs): # pylint:disable=no-self-use
        """Create a date using the UTC time zone as default."""
        return MomentX(*args, timezone=kwargs.get("timezone", "UTC"))

    def utcnow(self): # pylint:disable=no-self-use
        """UTC equivalent to `now` function."""
        return MomentX(*self.args_now, timezone="UTC")
