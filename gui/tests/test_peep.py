#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from communication.peep import peep


"""
TH11
"""
def test_peepReset(qtbot):
    '''
    Test the reset of the Peep
    '''

    p = peep()

    # Set a negative value for the t5 parameter, so the time t is obiously greater than t5
    t5 = p.t5
    p.t5 = -1
    t0 = p.t0

    # Force the flow
    p.flow()

    assert p.t0 != t0

    p.t5 = t5
