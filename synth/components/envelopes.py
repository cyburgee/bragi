import itertools

from config import SAMPLE_RATE
from util.types import Seconds, Amplitude

class ADSREnvelope:
    """
    A simple ADSR envelope with the four stages attack, decay, sustain and release.

    Has `.trigger_release()` implemented to trigger the release stage of the envelope.
    similarly has `.ended`, a flag to indicate the end of the release stage.
    """

    def __init__(
            self,
            attack_duration: Seconds=0.05,
            decay_duration: Seconds=0.2,
            sustain_level: Amplitude=0.7,
            release_duration: Seconds=0.3):
        """
        attack_duration : time taken to reach from 0 to 1 in s.
        decay_duration : time taken to reach from 1 to `sustain_level` in s.
        sustain_level : the float value of the sustain stage, should typically
            be in the range [0,1]
        release_duration : time taken to reach 0 from current value in s.
        """
        self.attack_duration = attack_duration
        self.decay_duration = decay_duration
        self.sustain_level = sustain_level
        self.release_duration = release_duration
        self.stepper = None

    def _get_ads_stepper(self):
        steppers = []
        if self.attack_duration > 0:
            steppers.append(
                itertools.count(
                    start=0, step=1 / (self.attack_duration * SAMPLE_RATE)
                )
            )
        if self.decay_duration > 0:
            steppers.append(
                itertools.count(
                    start=1,
                    step=-(1 - self.sustain_level)
                    / (self.decay_duration * SAMPLE_RATE),
                )
            )
        while True:
            l = len(steppers)
            if l > 0:
                val = next(steppers[0])
                if l == 2 and val > 1:
                    steppers.pop(0)
                    val = next(steppers[0])
                elif l == 1 and val < self.sustain_level:
                    steppers.pop(0)
                    val = self.sustain_level
            else:
                val = self.sustain_level
            yield val

    def _get_r_stepper(self):
        val = 1
        if self.release_duration > 0:
            release_step = -self.val / (self.release_duration * SAMPLE_RATE)
            stepper = itertools.count(self.val, step=release_step)
        else:
            val = -1
        while True:
            if val <= 0:
                self.ended = True
                val = 0
            else:
                val = next(stepper)
            yield val

    def __iter__(self):
        self.val = 0
        self.ended = False
        self.stepper = self._get_ads_stepper()
        return self

    def __next__(self):
        self.val = next(self.stepper)
        return self.val

    def trigger_release(self):
        self.stepper = self._get_r_stepper()
