import pytest
from synth.music import Pitch, PitchClass

def test_pitch_str():
    pitch = Pitch(PitchClass.C, 4)
    assert str(pitch) == 'C4'

def test_pitch_equality():
    c4 = Pitch(PitchClass.C, 4)
    c4_prime = Pitch(PitchClass.C, 4)
    d4 = Pitch(PitchClass.D, 4)
    assert c4 == c4_prime
    assert c4 != d4

def test_pitch_comparison():
    c4 = Pitch(PitchClass.C, 4)
    d4 = Pitch(PitchClass.D, 4)
    assert c4 < d4
    assert d4 > c4
    assert c4 <= d4
    assert d4 >= c4

def test_pitch_distance():
    c4 = Pitch(PitchClass.C, 4)
    db5 = Pitch(PitchClass.Db, 5)
    b3 = Pitch(PitchClass.B, 3)
    b4 = Pitch(PitchClass.B, 4)
    assert c4.distance(db5) == 13
    assert db5.distance(c4) == -13
    assert b3.distance(c4) == 1
    assert b4.distance(c4) == -11

def test_pitch_frequency():
    a4 = Pitch(PitchClass.A, 4)
    c4 = Pitch(PitchClass.C, 4)
    assert pytest.approx(a4.frequency(), 0.01) == 440.0
    assert pytest.approx(c4.frequency(), 0.01) == 261.63