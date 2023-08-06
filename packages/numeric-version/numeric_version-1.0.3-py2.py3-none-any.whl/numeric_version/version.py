# Copyright 2017 Neverware Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple numeric version class."""

import functools

@functools.total_ordering
class NumericVersion(object):
    """Numeric version, e.g. 3.4.12.

    Internally represented as a tuple of integers.
    """
    __slots__ = ('_parts',)

    def __init__(self, *parts):
        self._parts = None
        self.parts = parts

    @property
    def parts(self):
        """Tuple of integers representing the version."""
        return self._parts

    @parts.setter
    def parts(self, parts):
        """Set a new tuple of integers representing the version."""
        self._parts = tuple(int(part) for part in parts)

    @classmethod
    def parse(cls, string):
        """Parse a dotted-string into a NumericVersion."""
        return cls(*string.split('.'))

    def __str__(self):
        return '.'.join(str(part) for part in self.parts)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

    def __len__(self):
        return len(self.parts)
