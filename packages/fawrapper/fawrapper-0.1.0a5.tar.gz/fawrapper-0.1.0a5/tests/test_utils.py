"""Tests for the utils module"""
from fawrapper.utils import format_time_to_iso


def test_format_time_to_iso_utc_string():

    datetime_string = format_time_to_iso(2017, 9, 30, 21, 37, 1)

    # TODO: specify timezone for testing on multiple zones
    #assert datetime_string == '2017-09-30T21:37:01-05:00'
