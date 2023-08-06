"""Utilities for data management and interacting with the api"""
from datetime import datetime, timezone
import os


def persist_token(token, file='token_db'):
    with open(file, 'w') as f:
        f.write(str(token))


def read_token(file='token_db'):
    with open(file, 'r') as f:
        return f.read()


def format_time_to_iso(year, month, day,
                       hour=0, minute=0, second=0):
    """
    Convert local time to UTC time with TZ offset,
    in proper UTC format required by the api
    """
    datetime_obj = datetime(year, month, day, hour, minute, second)
    return datetime_obj.astimezone().isoformat()
