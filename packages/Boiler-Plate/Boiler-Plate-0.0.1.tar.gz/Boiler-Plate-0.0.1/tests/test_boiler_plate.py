#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_boiler_plate
----------------------------------

Tests for `boiler_plate` module.
"""

import unittest

import boiler_plate
from boiler_plate.cli import hello


class TestBoiler_plate(unittest.TestCase):

    def setUp(self):
        self.hello_message = "Hello, Fang"
        pass

    def test_something(self):
        assert(boiler_plate.__version__)
        output = hello()
        assert(output == self.hello_message)

    def tearDown(self):
        pass
