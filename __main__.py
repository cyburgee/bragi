import numpy as np
import pyaudio
from pynput import keyboard

from music import PitchClass, Pitch
from synth.components import SineOscillator

type Hz = int
type Seconds = float

from config import SAMPLE_RATE, BUFFER_SIZE, CHUNK_DURATION

c4 = Pitch(PitchClass.C, 4)

KEY_MAP = {
    'f': c4 ,
    'g': c4 + 1,
    'h': c4 + 2,
    'j': c4 + 3
}
VOICES = {}

def stream_callback(in_data, frame_count, time_info, status_flags):
    # mix all the voices into a single waveform
    # make sure to get a list of all voices so that it doesn't freak out if one is added or dropped during iteration
    input_signals = np.array([[next(voice) for _ in range(BUFFER_SIZE)] for voice in list(VOICES.values())])
    if len(input_signals) == 0: # output silence if no inputs
        return np.zeros(BUFFER_SIZE).astype(np.float32), pyaudio.paContinue
    mixed = np.mean(input_signals, axis=0)
    mixed = np.clip(mixed, -1.0, 1.0) # make sure the final output samples don't exceed amplitude of 1
    samples = mixed.astype(np.float32)
    return samples, pyaudio.paContinue

def key_pressed(key):
    if hasattr(key, 'char'):
        freq = KEY_MAP.get(key.char)
        if freq:
            if not VOICES.get(key.char):
                VOICES[key.char] = iter(SineOscillator(freq.frequency()))

def key_released(key):
    if key == keyboard.Key.esc:
        stream.stop_stream()
        stream.close()
        aud.terminate()
        return False
    if hasattr(key, 'char'):
        voice = VOICES.get(key.char)
        if voice:
            # print(f'stopping {voice.frequency}')
            del VOICES[key.char]

if __name__ == "__main__":
    # initialize the audio stream
    aud = pyaudio.PyAudio()
    stream = aud.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=SAMPLE_RATE,
        output=True,
        stream_callback=stream_callback,
        frames_per_buffer=BUFFER_SIZE)
    stream.start_stream()

    # grab keyboard events
    with keyboard.Listener(
        on_press=key_pressed,
        on_release=key_released) as listener:
        listener.join()


