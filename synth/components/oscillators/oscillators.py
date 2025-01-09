import math

from config import SAMPLE_RATE
from util.types import Hz, Degrees, Amplitude
from .base_oscillator import Oscillator


class SineOscillator(Oscillator):
    def _post_freq_set(self):
        self._step = (2 * math.pi * self._f) / SAMPLE_RATE

    def _post_phase_set(self):
        self._p = (self._p / 360) * 2 * math.pi

    def _initialize_osc(self):
        self._i = 0

    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if self._wave_range is not (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a


class SquareOscillator(SineOscillator):
    def __init__(
        self,
        freq: Hz=440,
        phase: Degrees=0,
        amp: Amplitude=1,
        wave_range=(-1, 1),
        duty=0,
    ):
        super().__init__(freq, phase, amp, wave_range)
        self.threshold = duty

    def __next__(self):
        val = math.sin(self._i + self._p)
        self._i = self._i + self._step
        if val < self.threshold:
            val = self._wave_range[0]
        else:
            val = self._wave_range[1]
        return val * self._a


class SawtoothOscillator(Oscillator):
    def _post_freq_set(self):
        self._period = SAMPLE_RATE / self._f
        self._post_phase_set()

    def _post_phase_set(self):
        self._p = ((self._p + 90) / 360) * self._period

    def _initialize_osc(self):
        self._i = 0

    def __next__(self):
        div = (self._i + self._p) / self._period
        val = 2 * (div - math.floor(0.5 + div))
        self._i = self._i + 1
        if self._wave_range is not (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a


class TriangleOscillator(SawtoothOscillator):
    def __next__(self):
        div = (self._i + self._p) / self._period
        val = 2 * (div - math.floor(0.5 + div))
        val = (abs(val) - 0.5) * 2
        self._i = self._i + 1
        if self._wave_range is not (-1, 1):
            val = self.squish_val(val, *self._wave_range)
        return val * self._a
