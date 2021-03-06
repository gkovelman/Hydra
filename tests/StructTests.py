#!/usr/bin/env python
"""
Contains various tests for the `Struct` class of the base module.

:file: StructTests.py
:date: 30/08/2015
:authors:
    - Gilad Naaman <gilad.naaman@gmail.com>
"""
import unittest
from hydra import *

#########################
# "Structs" for testing #
#########################


class SmallStruct(Struct):
    only_element = UInt8()


class SimpleStruct(Struct):
    b_first_variable = UInt8(0xDE)
    a_second_variable = UInt16(0xCAFE)
    x_third_variable = UInt8(0xAD)


class ComplicatedStruct(Struct):
    other_struct = NestedStruct(SmallStruct)
    some_field = TypedArray(3, SimpleStruct)
    numeric = UInt32()


class BigEndianStruct(Struct):
    settings = {'endian': BigEndian}

    hello_i_am_trapped_in_a_variable_factory_please_help_theyre_going_to_ = UInt16(0xFF00)


##############
# Test Cases #
##############


class StructTests(unittest.TestCase):
    """ A testcase checking for a few of `Struct`'s features. """
    
    def setUp(self):
        HydraSettings.push()
        HydraSettings.endian = LittleEndian

    def tearDown(self):
        HydraSettings.pop()

    def test_serialize_simple(self):
        """ Test serialization of a simple struct. """
        obj = SimpleStruct()
        raw_data = obj.serialize()
        self.assertEqual(raw_data, b'\xDE\xFE\xCA\xAD')

    def test_one_does_not_complicatedly(self):
        """ Test serialization and deserialization of a more complicated struct."""
        s = ComplicatedStruct()
        s.numeric = 0xAEAEAEAE
        data = s.serialize()
        # Test serialization.
        self.assertEqual(data, b'\x00\xDE\xFE\xCA\xAD\xDE\xFE\xCA\xAD\xDE\xFE\xCA\xAD\xAE\xAE\xAE\xAE')

        # Test deserialization.
        d_s = ComplicatedStruct.deserialize(data)
        self.assertEqual(d_s, s)

    def test_big_endian_struct(self):
        """ Test the struct-wide settings of a struct and their serialization overrides."""
        big_endian_struct = BigEndianStruct()
        self.assertEqual(big_endian_struct.serialize(), b'\xFF\x00')

        # Force little endian
        self.assertEqual(big_endian_struct.serialize({'endian': LittleEndian}), b'\x00\xFF')


if __name__ == '__main__':
    unittest.main()
