#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cardbin` package."""

from cardbin import cardbin

def test_content():
	assert type(cardbin('6228480402564890018')) == dict
