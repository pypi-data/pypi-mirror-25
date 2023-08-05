#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of inenv.
# https://github.com/pnegahdar/inenv

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Parham Negahdar <pnegahdar@gmail.com>

from preggy import expect

from inenv.version import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('1.0.6')
