# Copyright 2017 StreamSets Inc.

"""Assorted utility functions."""

import logging
import random
import re

from inflection import camelize

logger = logging.getLogger(__name__)


def get_random_string(characters, length=8):
    """
    Returns a string of the requested length consisting of random combinations of the given
    sequence of string characters.
    """
    return ''.join(random.choice(characters) for _ in range(length))


def join_url_parts(*parts):
    """
    Join a URL from a list of parts. See http://stackoverflow.com/questions/24814657 for
    examples of why urllib.parse.urljoin is insufficient for what we want to do.
    """
    return '/'.join([piece.strip('/') for piece in parts])


def get_params(parameters, exclusions=None):
    """Get a dictionary of parameters to be passed as requests methods' params argument.

    The typical use of this method is to pass in locals() from a function that wraps a
    REST endpoint. It will then create a dictionary, filtering out any exclusions (e.g.
    path parameters) and unset parameters, and use camelize to convert arguments from
    ``this_style`` to ``thisStyle``.
    """
    return {camelize(arg, uppercase_first_letter=False): value
            for arg, value in parameters.items()
            if value is not None and arg not in exclusions}


class Version:
    """Maven version string abstraction.

    Use this class to enable correct comparison of Maven versioned projects. That is, along with handling normal
    dot-separated versions, it also recognizes snapshot artifacts as being 'earlier' than release artifacts.

    Args:
        version (`str`): Version string (e.g. '2.5.0.0-SNAPSHOT')
    """
    # pylint: disable=protected-access,too-few-public-methods
    def __init__(self, version):
        self._str = version

        # Generate a tuple of versions by padding the given version to have 4 numbers (e.g. '2.5' => '2.5.0.0-SNAPSHOT'
        # and '2.5-SNAPSHOT' => '2.5.0.0-SNAPSHOT'). We do this in a bit of a gross way using slice notation to insert
        # the correct number of zeros at the end of the list (or before the last element, if the last element is
        # the 'SNAPSHOT' specifier.
        version_list = [int(i) if i.isdigit() else i for i in re.split('[.-]', self._str)]
        lvl = len(version_list)
        version_list[lvl if version_list[-1] != 'SNAPSHOT' else lvl - 1:
                     lvl if version_list[-1] != 'SNAPSHOT' else lvl - 1] = (
                         [0] * (4 - (lvl if version_list[-1] != 'SNAPSHOT' else lvl - 1))
                     )
        self._tuple = tuple(version_list)

    def __repr__(self):
        return str(self._tuple)

    def __eq__(self, other):
        return self._tuple == other._tuple

    def __lt__(self, other):
        if not isinstance(other, Version):
            raise TypeError('Comparison can only be done for two Version instances.')
        if (all(version._tuple[-1] == 'SNAPSHOT' for version in (self, other)) or
                all(version._tuple[-1] != 'SNAPSHOT' for version in (self, other)) or
                self._tuple[:3] < other._tuple[:3]):
            return self._tuple < other._tuple
        elif self._tuple[:3] == other._tuple[:3]:
            return self._tuple[-1] == 'SNAPSHOT'

    def __gt__(self, other):
        return other.__lt__(self)
