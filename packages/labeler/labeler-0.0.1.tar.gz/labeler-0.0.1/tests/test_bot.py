#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from labeler_site.bot import recognize_greeting


__author__ = "Hobson Lane"
__copyright__ = "Hobson Lane"
__license__ = "mit"


def test_recognize_greeting():
    assert recognize_greeting('Hi') is True
    assert recognize_greeting('Yo') is False
    assert recognize_greeting('') is False
    with pytest.raises(AttributeError):
        recognize_greeting(None)
