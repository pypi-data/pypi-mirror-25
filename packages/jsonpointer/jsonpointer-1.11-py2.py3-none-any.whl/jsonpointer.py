# -*- coding: utf-8 -*-
#
# python-json-pointer - An implementation of the JSON Pointer syntax
# https://github.com/stefankoegl/python-json-pointer
#
# Copyright (c) 2011 Stefan Kögl <stefan@skoegl.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

""" Identify specific nodes in a JSON document (RFC 6901) """

from __future__ import unicode_literals

# Will be parsed by setup.py to determine package metadata
__author__ = 'Stefan Kögl <stefan@skoegl.net>'
__version__ = '1.11'
__website__ = 'https://github.com/stefankoegl/python-json-pointer'
__license__ = 'Modified BSD License'


try:
    from urllib import unquote
    str = unicode
except ImportError:  # Python 3
    from urllib.parse import unquote

try:
    from collections.abc import Mapping, Sequence
except ImportError:  # Python 3
    from collections import Mapping, Sequence

import re
import copy


_nothing = object()


def set_pointer(doc, pointer, value, inplace=True):
    """Resolves pointer against doc and sets the value of the target within doc.

    With inplace set to true, doc is modified as long as pointer is not the
    root.

    >>> obj = {'foo': {'anArray': [ {'prop': 44}], 'another prop': {'baz': 'A string' }}}

    >>> set_pointer(obj, '/foo/anArray/0/prop', 55) == \
    {'foo': {'another prop': {'baz': 'A string'}, 'anArray': [{'prop': 55}]}}
    True

    >>> set_pointer(obj, '/foo/yet%20another%20prop', 'added prop') == \
    {'foo': {'another prop': {'baz': 'A string'}, 'yet another prop': 'added prop', 'anArray': [{'prop': 55}]}}
    True
    """

    pointer = JsonPointer(pointer)
    return pointer.set(doc, value, inplace)


def resolve_pointer(doc, pointer, default=_nothing):
    """ Resolves pointer against doc and returns the referenced object

    >>> obj = {'foo': {'anArray': [ {'prop': 44}], 'another prop': {'baz': 'A string' }}}

    >>> resolve_pointer(obj, '') == obj
    True

    >>> resolve_pointer(obj, '/foo') == obj['foo']
    True

    >>> resolve_pointer(obj, '/foo/another%20prop') == obj['foo']['another prop']
    True

    >>> resolve_pointer(obj, '/foo/another%20prop/baz') == obj['foo']['another prop']['baz']
    True

    >>> resolve_pointer(obj, '/foo/anArray/0') == obj['foo']['anArray'][0]
    True

    >>> resolve_pointer(obj, '/some/path', None) == None
    True
    """

    pointer = JsonPointer(pointer)
    return pointer.resolve(doc, default)


class JsonPointerException(Exception):
    pass


class EndOfList(object):
    """Result of accessing element "-" of a list"""

    def __init__(self, list_):
        self.list_ = list_

    def __repr__(self):
        return '{cls}({lst})'.format(cls=self.__class__.__name__,
                                     lst=repr(self.list_))


class JsonPointer(object):
    """A JSON Pointer that can reference parts of an JSON document"""

    # Array indices must not contain:
    # leading zeros, signs, spaces, decimals, etc
    _RE_ARRAY_INDEX = re.compile('0|[1-9][0-9]*$')

    def __init__(self, pointer):
        parts = pointer.split('/')
        if parts.pop(0) != '':
            raise JsonPointerException('location must starts with /')

        parts = map(unquote, parts)
        parts = [unescape(part) for part in parts]
        self.parts = parts

    def to_last(self, doc):
        """Resolves ptr until the last step, returns (sub-doc, last-step)"""

        if not self.parts:
            return doc, None

        doc = self.resolve(doc, parts=self.parts[:-1])
        last = self.parts[-1]
        ptype = type(doc)
        if ptype == dict:
            pass
        elif ptype == list or isinstance(doc, Sequence):
            if not self._RE_ARRAY_INDEX.match(str(last)):
                raise JsonPointerException(
                    "'%s' is not a valid list index" % (last, )
                )
            last = int(last)

        return doc, last

    def resolve(self, doc, default=_nothing, parts=None):
        """ Resolves the pointer against doc, returns the referenced object """
        if parts is None:
            parts = self.parts

        try:
            for part in parts:
                ptype = type(doc)
                if ptype == dict:
                    doc = doc[part]
                elif ptype == list or isinstance(doc, Sequence):
                    if part == '-':
                        doc = EndOfList(doc)
                    else:
                        if not self._RE_ARRAY_INDEX.match(str(part)):
                            raise JsonPointerException(
                                "'%s' is not a valid list index" % (part, )
                            )
                        doc = doc[int(part)]
                else:
                    doc = doc[part]
        except KeyError:
            if default is not _nothing:
                return default
            raise JsonPointerException(
                "member '%s' not found in %s" % (part, doc)
            )

        except IndexError:
            if default is not _nothing:
                return default
            raise JsonPointerException(
                "index '%s' is out of bounds" % (part, )
            )

        except TypeError:
            if default is not _nothing:
                return default
            raise JsonPointerException(
                "Document '%s' does not support indexing, must be dict/list "
                "or support __getitem__" % type(doc)
            )

        return doc

    get = resolve

    def set(self, doc, value, inplace=True):
        """Resolve the pointer against the doc and replace the target with value."""

        if len(self.parts) == 0:
            if inplace:
                raise JsonPointerException('cannot set root in place')
            return value

        if not inplace:
            doc = copy.deepcopy(doc)

        (parent, part) = self.to_last(doc)

        parent[part] = value
        return doc

    def get_part(self, doc, part):
        """Returns the next step in the correct type"""

        # Optimize for common cases of doc being a dict or list, but not a
        # sub-class (because isinstance() is far slower)
        ptype = type(doc)
        if ptype == dict:
            return part
        if ptype == list or isinstance(doc, Sequence):
            if part == '-':
                return part

            if not self._RE_ARRAY_INDEX.match(str(part)):
                raise JsonPointerException(
                    "'%s' is not a valid list index" % (part, )
                )
            return int(part)

        elif hasattr(doc, '__getitem__'):
            # Allow indexing via ducktyping
            # if the target has defined __getitem__
            return part

        else:
            raise JsonPointerException(
                "Document '%s' does not support indexing, must be "
                "mapping/sequence or support __getitem__" % type(doc)
            )

    def walk(self, doc, part):
        """ Walks one step in doc and returns the referenced part """

        part = self.get_part(doc, part)

        if part == '-' and isinstance(doc, Sequence):
            return EndOfList(doc)

        try:
            return doc[part]

        except KeyError:
            raise JsonPointerException(
                "member '%s' not found in %s" % (part, doc)
            )

        except IndexError:
            raise JsonPointerException(
                "index '%s' is out of bounds" % (part, )
            )

        except TypeError:
            raise JsonPointerException(
                "Document '%s' does not support indexing, must be dict/list "
                "or support __getitem__" % type(doc)
            )

        except KeyError:
            raise JsonPointerException(
                "member '%s' not found in %s" % (part, doc)
            )

    def contains(self, ptr):
        """ Returns True if self contains the given ptr """
        return self.parts[:len(ptr.parts)] == ptr.parts

    def __contains__(self, item):
        """ Returns True if self contains the given ptr """
        return self.contains(item)

    @property
    def path(self):
        """Returns the string representation of the pointer

        >>> ptr = JsonPointer('/~0/0/~1').path == '/~0/0/~1'
        """
        parts = [escape(part) for part in self.parts]
        return ''.join('/' + part for part in parts)

    def __eq__(self, other):
        """Compares a pointer to another object

        Pointers can be compared by comparing their strings (or splitted
        strings), because no two different parts can point to the same
        structure in an object (eg no different number representations)
        """

        if not isinstance(other, JsonPointer):
            return False

        return self.parts == other.parts

    def __hash__(self):
        return hash(tuple(self.parts))

    @classmethod
    def from_parts(cls, parts):
        """Constructs a JsonPointer from a list of (unescaped) paths

        >>> JsonPointer.from_parts(['a', '~', '/', 0]).path == '/a/~0/~1/0'
        True
        """
        parts = [escape(str(part)) for part in parts]
        ptr = cls(''.join('/' + part for part in parts))
        return ptr


def escape(s):
    return s.replace('~', '~0').replace('/', '~1')

def unescape(s):
    return s.replace('~1', '/').replace('~0', '~')
