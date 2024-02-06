import pytest

from gcd_algorithm import great_circle_distance

def test_great_circle_distance():
    assert great_circle_distance((0,0), (0,0)) == 0.0 # same point
    assert great_circle_distance((0,0), (0,90)) == 10018.754171394621 # different longitude
    assert great_circle_distance((0,0), (90,0)) == 10018.754171394621 # different latitude
    assert great_circle_distance((50.775, 6.08333), (56.18333, 10.23333)) == 661.5651375967635 # different latitude and longitude