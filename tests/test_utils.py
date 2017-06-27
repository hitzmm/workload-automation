#    Copyright 2013-2015 ARM Limited
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
#


# pylint: disable=R0201
from unittest import TestCase

from nose.tools import raises, assert_equal, assert_not_equal, assert_in, assert_not_in
from nose.tools import assert_true, assert_false

from wa.utils.types import (list_or_integer, list_or_bool, caseless_string,
                            arguments, prioritylist, enum, level)



class TestPriorityList(TestCase):

    def test_insert(self):
        pl = prioritylist()
        elements = {3: "element 3",
                    2: "element 2",
                    1: "element 1",
                    5: "element 5",
                    4: "element 4"
                    }
        for key in elements:
            pl.add(elements[key], priority=key)

        match = zip(sorted(elements.values()), pl[:])
        for pair in match:
            assert(pair[0] == pair[1])

    def test_delete(self):
        pl = prioritylist()
        elements = {2: "element 3",
                    1: "element 2",
                    0: "element 1",
                    4: "element 5",
                    3: "element 4"
                    }
        for key in elements:
            pl.add(elements[key], priority=key)
        del elements[2]
        del pl[2]
        match = zip(sorted(elements.values()), pl[:])
        for pair in match:
            assert(pair[0] == pair[1])

    def test_multiple(self):
        pl = prioritylist()
        pl.add('1', 1)
        pl.add('2.1', 2)
        pl.add('3', 3)
        pl.add('2.2', 2)
        it = iter(pl)
        assert_equal(it.next(), '3')
        assert_equal(it.next(), '2.1')
        assert_equal(it.next(), '2.2')
        assert_equal(it.next(), '1')

    def test_iterator_break(self):
        pl = prioritylist()
        pl.add('1', 1)
        pl.add('2.1', 2)
        pl.add('3', 3)
        pl.add('2.2', 2)
        for i in pl:
            if i == '2.1':
                break
        assert_equal(pl.index('3'), 3)

    def test_add_before_after(self):
        pl = prioritylist()
        pl.add('m', 1)
        pl.add('a', 2)
        pl.add('n', 1)
        pl.add('b', 2)
        pl.add_before('x', 'm')
        assert_equal(list(pl), ['a', 'b', 'x', 'm', 'n'])
        pl.add_after('y', 'b')
        assert_equal(list(pl), ['a', 'b','y', 'x', 'm', 'n'])
        pl.add_after('z', 'm')
        assert_equal(list(pl), ['a', 'b', 'y', 'x', 'm', 'z', 'n'])


class TestEnumLevel(TestCase):

    def test_serialize_level(self):
        l = level('test', 1)
        s = l.to_pod()
        l2 = level.from_pod(s)
        assert_equal(l, l2)

    def test_deserialize_enum(self):
        e = enum(['one', 'two', 'three'])
        s = e.one.to_pod()
        l = e.from_pod(s)
        assert_equal(l, e.one)
