# -*- coding: utf-8 -*-

# Copyright © 2017
# Contributed by Raphaël Bleuse <raphael.bleuse@imag.fr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Toolkit to manage sets of closed intervals.

This implementation requires intervals bounds to be non-negative integers. This
design choice has been made as procset targets managment of resources for
scheduling. Hence, the manipulated intervals can be represented as indexes.
"""

import operator


class ProcInt(tuple):
    """A ProcInt is a closed interval of non-negative integers."""

    __slots__ = ()

    def __new__(cls, inf, sup):
        """Create new instance of ProcInt(inf, sup)."""
        if not isinstance(inf, int):
            raise TypeError('{}() argument inf must be int'.format(cls.__name__))
        if not isinstance(sup, int):
            raise TypeError('{}() argument sup must be int'.format(cls.__name__))
        if inf > sup:
            raise ValueError('Invalid interval bounds')
        if inf < 0:
            raise ValueError('Invalid negative bound(s)')
        return tuple.__new__(cls, (inf, sup))

    def __repr__(self):
        """Return a nicely formatted representation string."""
        return '{}(inf={!r}, sup={!r})'.format(self.__class__.__name__, *self)

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        if self.inf == self.sup:
            return str(self.inf)
        else:
            if len(format_spec) > 1:
                raise ValueError('Invalid format specifier')
            insep = format_spec or '-'
            return insep.join(map(str, self))

    def __len__(self):
        return self.sup - self.inf + 1

    def __contains__(self, item):
        return self.inf <= item <= self.sup

    inf = property(operator.itemgetter(0), doc='Alias for field number 0')

    sup = property(operator.itemgetter(1), doc='Alias for field number 1')


class _Sentinel:
    """Helper class whose instances are greater than any object."""

    __slots__ = ()

    def __eq__(self, other):
        return self is other

    def __lt__(self, other):
        return False

    __le__ = __eq__

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True


class ProcSet:
    """
    A ProcSet is a set of non-overlapping ProcInt.

    The current implementation uses a sorted list of ProcSet to store the
    ProcInt.
    """

    __slots__ = '_itvs'

    def __init__(self, *intervals):
        """
        Initialize a ProcSet.

        A ProcSet can be initialized with either nothing (empty set), any
        number of non-negative int, any number of ProcInt compatible objects
        (iterable of exactly 2 ints), or any combination of both.

        There are no restrictions on the domains of the intervals in the
        constructor: they may overlap.

        Examples:
            ProcSet()  # empty set
            ProcSet(1)
            ProcSet(ProcInt(0, 1))
            ProcSet(ProcInt(0, 1), ProcInt(2, 3))
            ProcSet((0, 1), [2, 3])  # identical to previous call
            ProcSet(ProcInt(0, 1), *[0, 3])  # mixing ProcInt and lists
        """
        self._itvs = []  # list of disjoint intervals
        for itv in intervals:
            self.add(itv)

    @classmethod
    def from_str(cls, string, insep="-", outsep=" "):
        """Parse a string interval set representation into a ProcSet."""
        if not isinstance(string, str):
            raise TypeError(
                'from_str() argument 2 must be str, not {}'.format(string.__class__.__name__)
            )

        new_pset = cls()

        # empty string is parsed as empty ProcSet
        if string == '':
            return new_pset

        try:
            for itv in string.split(sep=outsep):
                bounds = itv.split(sep=insep, maxsplit=1)
                if len(bounds) == 1:
                    new_pset.add(int(itv))
                else:
                    inf, sup = bounds
                    new_pset.add(ProcInt(int(inf), int(sup)))
        except ValueError:
            raise ValueError(
                'Invalid interval format, parsed string is: {}'.format(string)
            ) from None

        return new_pset

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        if format_spec:
            try:
                insep, outsep = format_spec
            except ValueError:
                raise ValueError('Invalid format specifier') from None
        else:
            insep, outsep = '- '

        return outsep.join(format(itv, insep) for itv in self._itvs)

    # def __repr__(self):
    #     pass

    def __iter__(self):
        """Iterate through the processors in self by increasing order."""
        # as self._itvs is sorted by increasing order, we can directly yield
        for itv in self._itvs:
            yield from range(itv.inf, itv.sup + 1)

    def __reversed__(self):
        """Iterate through the processors in self by decreasing order."""
        # as self._itvs is sorted in increasing order, we yield from the
        # reversed iterator
        for itv in reversed(self._itvs):
            yield from range(itv.sup, itv.inf - 1, -1)

    def __contains__(self, item):
        """Check if item is in self."""
        if self._itvs:
            low, high = 0, len(self._itvs)
            while low < high:
                mid = (low + high) // 2
                if item in self._itvs[mid]:
                    return True
                elif item < self._itvs[mid].inf:
                    high = mid
                else:
                    low = mid + 1
        return False

    def __len__(self):
        """Return the number of processors."""
        return sum(len(itv) for itv in self._itvs)

    def count(self):
        """Return the number of disjoint processors' intervals."""
        return len(self._itvs)

    def iscontiguous(self):
        """Return True if the processors form a single contiguous set."""
        return self.count() <= 1

    def isdisjoint(self, other):
        raise NotImplementedError

    def issubset(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def issuperset(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def _flatten(self):
        """Generate the (flat) list of interval bounds contained by self."""
        for itv in self._itvs:
            # use inf as is
            yield False, itv.inf
            # convert sup, as merging operations are made with half-open
            # intervals
            yield True, itv.sup + 1

    @classmethod
    def _merge_core(cls, leftset, rightset, keeppredicate):
        """
        Generate the (flat) list of interval bounds of the requested merge.

        The implementation is inspired by https://stackoverflow.com/a/20062829.
        """
        endbound = False
        sentinel = _Sentinel()

        # pylint: disable=protected-access
        lflat = leftset._flatten()
        rflat = rightset._flatten()
        lend, lhead = next(lflat, (False, sentinel))
        rend, rhead = next(rflat, (False, sentinel))

        head = min(lhead, rhead)
        while head < sentinel:
            inleft = (head < lhead) == lend
            inright = (head < rhead) == rend
            keep = keeppredicate(inleft, inright)

            if keep ^ endbound:
                endbound = not endbound
                yield head
            if head == lhead:
                lend, lhead = next(lflat, (False, sentinel))
            if head == rhead:
                rend, rhead = next(rflat, (False, sentinel))

            head = min(lhead, rhead)

    @classmethod
    def _merge(cls, leftset, rightset, keeppredicate):
        """
        Generate the ProcInt list of the requested merge.

        The returned iterator is supposed to be assigned to the _itvs attribute
        of the result ProcSet.
        See the difference(), intersection(), symmetric_difference(), and
        union() methods for an usage example.
        """
        flat_merge = cls._merge_core(leftset, rightset, keeppredicate)

        # Note that we are feeding the same iterable twice to zip.
        # The iterated bounds are hence grouped by pairs (lower and upper
        # bounds of the intervals).
        # As zip() stops on the shortest iterable, it won't consider the
        # optional terminating sentinel (the sentinel would be the last
        # element, and would have an odd index).
        for inf, sup in zip(flat_merge, flat_merge):
            yield ProcInt(inf, sup - 1)  # convert back to closed intervals

    def union(self, *others):
        raise NotImplementedError

    def __or__(self, other):
        """Return a new ProcSet with the intervals from self and other."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # We directly assign result._itvs as self._merge(…) returns a valid
        # _itvs list. This is the same as ProcSet(*self._merge(…)), minus the
        # input validation step.
        result = ProcSet()
        result._itvs = list(self._merge(self, other, operator.or_))
        return result

    def __eq__(self, other):
        # pylint: disable=protected-access
        return self._itvs == other._itvs

    def intersection(self, *others):
        raise NotImplementedError

    def __and__(self, other):
        """Return a new ProcSet with the intervals common to self and other."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # We directly assign result._itvs as self._merge(…) returns a valid
        # _itvs list. This is the same as ProcSet(*self._merge(…)), minus the
        # input validation step.
        result = ProcSet()
        result._itvs = list(self._merge(self, other, operator.and_))
        return result

    def difference(self, *others):
        raise NotImplementedError

    def __sub__(self, other):
        """
        Return a new ProcSet with the intervals in self that are not in other.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # We directly assign result._itvs as self._merge(…) returns a valid
        # _itvs list. This is the same as ProcSet(*self._merge(…)), minus the
        # input validation step.
        result = ProcSet()
        result._itvs = list(
            self._merge(
                self, other,
                lambda inleft, inright: inleft and not inright
            )
        )
        return result

    def symmetric_difference(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        """
        Return a new ProcSet with the intervals in either self or other, but
        not both.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # We directly assign result._itvs as self._merge(…) returns a valid
        # _itvs list. This is the same as ProcSet(*self._merge(…)), minus the
        # input validation step.
        result = ProcSet()
        result._itvs = list(self._merge(self, other, operator.xor))
        return result

    def copy(self):
        raise NotImplementedError

    def update(self, *others):
        raise NotImplementedError

    def __ior__(self, other):
        """Update the ProcSet, adding the intervals from other."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        self._itvs = list(self._merge(self, other, operator.or_))
        return self

    def intersection_update(self, *others):
        raise NotImplementedError

    def __iand__(self, other):
        """
        Update the ProcSet, keeping only the intervals found in self and other.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        self._itvs = list(self._merge(self, other, operator.and_))
        return self

    def difference_update(self, *others):
        raise NotImplementedError

    def __isub__(self, other):
        """Update the ProcSet, removing the intervals found in other."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        self._itvs = list(
            self._merge(
                self, other,
                lambda inleft, inright: inleft and not inright
            )
        )
        return self

    def symmetric_difference_update(self, other):
        raise NotImplementedError

    def __ixor__(self, other):
        """
        Update the ProcSet, keeping only the intervals found in either self or
        other, but not in both.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        self._itvs = list(self._merge(self, other, operator.xor))
        return self

    def add(self, elem):
        """
        Insert elem into self.

        It is assumed elem is ProcInt compatible (iterable of exaclty 2 ints),
        or a single int.
        In the first case, ProcInt(*elem) is added into self, in the latter
        ProcInt(elem, elem) is added.

        If some processors already exist in self, they will not be added twice
        (hey this is a set!).
        """
        try:
            newinf, newsup = elem  # assume it is ProcInt compatible
        except TypeError:
            newinf, newsup = elem, elem  # if not assume it is a single point

        for itv in list(self._itvs):
            if newinf > itv.sup + 1:
                continue
            if newsup + 1 < itv.inf:
                break
            self._itvs.remove(itv)
            newinf = min(newinf, itv.inf)
            newsup = max(newsup, itv.sup)

        self._itvs.append(ProcInt(newinf, newsup))
        self._itvs.sort()

    def remove(self, elem):
        raise NotImplementedError

    def discard(self, elem):
        raise NotImplementedError

    def pop(self, elem):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    # we do not define __setitem__ as it makes no sense to modify a processor

    def __delitem__(self, key):
        raise NotImplementedError

    def aggregate(self):
        """
        Return the ProcSet that is the convex hull of self.

        If self is empty, its convex hull is the empty ProcSet.
        If self is not empty, its convex hull is the ProcSet with the smallest
        interval containing all intervals from self.
        """
        if self._itvs:
            return ProcSet(ProcInt(self.min, self.max))
        else:
            return ProcSet()

    def intervals(self):
        """Return an iterator on the intervals of self in increasing order."""
        return iter(self._itvs)

    @property
    def min(self):
        """The first processor in self (in increasing order)."""
        try:
            return self._itvs[0].inf
        except IndexError:
            raise ValueError('empty ProcSet') from None

    @property
    def max(self):
        """The last processor in self (in increasing order)."""
        try:
            return self._itvs[-1].sup
        except IndexError:
            raise ValueError('empty ProcSet') from None
