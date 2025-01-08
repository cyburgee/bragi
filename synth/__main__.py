import numpy as np
import pyaudio
from pynput import keyboard

type Hz = int
type Seconds = float

SAMPLE_RATE = 44100
BUFFER_SIZE = 1024
CHUNK_DURATION = BUFFER_SIZE / SAMPLE_RATE

KEY_MAP = {
    'f': 261.63,  # middle c
    'g': 293.67,
    'h': 329.63,
    'j': 349.23
}
VOICES = {}

# generator for sine wave voices
class SinOsc:
    def __init__(self, frequency: Hz, amplitude=0.5):
        self.frequency = frequency
        self.amplitude = amplitude
        self.start = 0.0
        self.end = CHUNK_DURATION

    def __iter__(self):
        return self

    def __next__(self):
        time_stamps = np.linspace(self.start, self.end, BUFFER_SIZE)
        samples = self.amplitude * np.sin(time_stamps * (2 * np.pi * self.frequency))
        # update the sample start and end for the next playback buffer
        self.start = self.end
        self.end += CHUNK_DURATION
        return samples.astype(np.float32)


def stream_callback(in_data, frame_count, time_info, status_flags):
    # mix all the voices into a single waveform
    # make sure to get a list of all voices so that it doesn't freak out if one is added or dropped during iteration
    input_signals = [next(voice) for voice in list(VOICES.values())]
    if not input_signals: # output silence if no inputs
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
                # print(f'generating {freq}')
                VOICES[key.char] = SinOsc(freq)

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


