from enum import Enum
from functools import total_ordering

type Semitone = int
type Octave = int


PITCH_COUNT = 12

class PitchClass(Enum):
    C = 0
    Db = 1
    D = 2
    Eb = 3
    E = 4
    F = 5
    Gb = 6
    G = 7
    Ab = 8
    A = 9
    Bb = 10
    B = 11


class Modality(Enum):
    MAJOR = 0
    MINOR = 1


@total_ordering
class Pitch:
    pitch_class: PitchClass
    octave: Octave

    def __init__(self, pitch_class: PitchClass, octave: Octave):
        self.pitch_class = pitch_class
        self.octave = octave

    def __str__(self):
        return f'{self.pitch_class.name}{self.octave}'

    def __eq__(self, other):
        return self.pitch_class == other.pitch_class and self.octave == other.octave

    def __lt__(self, other):
        return self.frequency() < other.frequency()

    # MIDI index
    def index(self):
        return (self.octave + 1) * PITCH_COUNT + self.pitch_class.value

    def distance(self, other):
        return other.index() - self.index()

    # base frequency on A4 = 440Hz
    # source https://en.wikipedia.org/wiki/Piano_key_frequencies
    def frequency(self):
        return 440 * (2 ** ((Pitch(PitchClass.A, 4).distance(self)) / 12))