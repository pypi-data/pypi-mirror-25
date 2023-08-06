Python-MomentX
==============

|Travis CI| |Python versions| |new-style BSD|

A lightweight wrapper around datetime with a focus on timezone handling
and few dependencies (only datetime, pytz and six).

Provides a immutable date/time type that always has an attached
timezone.

This module was originally derived from the `moment
module <https://github.com/zachwill/moment>`__ by Zach Williams.
Following the main differences:

-  MomentX dates always contain a timezone
-  comparison made easy because all MomentX objects are
   timezone-offset-aware
-  strptime with timezone support (%z)
-  MomentX objects are immutable (add(), replace(), etc does not alter
   the object)
-  api methods were converted to @classmethod
-  zero() is now a method and not a property
-  python3 support
-  removed js like date formatting options and 'times' dependency

Typical usage may look like this:

::


    >>> from momentx import MomentX
    >>> 
    >>> MomentX.utc(2012, 12, 18)
    <Moment(2012-12-18 00:00:00+0000 / UTC)>
    >>> 
    >>> MomentX(2012, 12, 18, timezone="UTC")
    <Moment(2012-12-18 00:00:00+0000 / UTC)>
    >>> 
    >>> MomentX(2012, 12, 18, timezone="Europe/Berlin")
    <Moment(2012-12-18 00:00:00+0100 / Europe/Berlin)>
    >>> 
    >>> MomentX(2012, 12, 18, timezone="Europe/Berlin").astimezone("UTC")
    <Moment(2012-12-17 23:00:00+0000 / UTC)>
    >>> 
    >>> MomentX(2012, 12, 18, 10, 11, 12, timezone="UTC").replace(hours=3)
    <Moment(2012-12-18 03:11:12+0000 / UTC)>
    >>> 
    >>> MomentX(2012, 12, 18, 10, 11, 12, timezone="UTC").zero()
    <Moment(2012-12-18 00:00:00+0000 / UTC)>
    >>> 
    >>> MomentX.utc(2012, 12, 18).add(days=2)
    <Moment(2012-12-20 00:00:00+0000 / UTC)>
    >>> 
    >>> MomentX.utcnow()
    <Moment(2016-05-17 18:30:40+0000 / UTC)>
    >>> 
    >>> MomentX.utcnow().strftime('%Y-%m-%d %H:%M:%S%z')
    '2016-05-17 18:31:20+0000'

Public repository
-----------------

https://github.com/berlincode/momentx

License
-------

Code and documentation copyright Ulf Bartel. Code is licensed under the
`new-style BSD license <./LICENSE.txt>`__.

.. |Travis CI| image:: https://travis-ci.org/berlincode/momentx.svg?branch=master&style=flat
   :target: https://travis-ci.org/berlincode/momentx
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/momentx.svg
   :target: https://pypi.python.org/pypi/momentx/
.. |new-style BSD| image:: https://img.shields.io/pypi/l/momentx.svg
   :target: https://github.com/berlincode/momentx/blob/master/LICENSE.txt
