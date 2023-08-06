# coding: utf-8
"""
Regex primitives.

"""

import re


ANYTHING = ".+"
WHITESPACE = "\s"
WHITESPACES = "{0}+".format(WHITESPACE)
NON_WHITESPACE = "\S"
NON_WHITESPACES = "{0}+".format(NON_WHITESPACE)
DIGIT = "\d"
NUMBER = "{0}+".format(DIGIT)
FLOAT = "{0}.{0}".format(NUMBER)
START_OF_STRING = "^"
END_OF_STRING = "$"


def make_matcher(pattern):
    return re.compile(pattern, re.VERBOSE).match


def group(expression):
    return "({0})".format(expression)


def named_group(group_name, expression):
    return "(?P<{0}>{1})".format(group_name, expression)


def choices(values, delimiter="|"):
    return delimiter.join(values)
