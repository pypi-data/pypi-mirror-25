#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

import doctest
import unittest

import zc.buildout.tests
import zc.buildout.testing



def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('nti.recipes.zcml', test)


tearDown = zc.buildout.testing.buildoutTearDown

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
    ))
