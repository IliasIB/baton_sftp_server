from enum import Enum


class CommandPatterns(Enum):
    """Enum for different command patterns"""
    get = 'GET (?P<revision>[1-9][0-9]*)'
    get_file = 'GET (?P<revision>[1-9][0-9]*)'
    '(?: (?P<file_name>.+))?'
