import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

rythm:list = []
temp:int = 60

def record_audio(filename:str, sample_rate = 44100, channels = 1, duration = 5): #not working
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype="float32"
    )

    sd.wait()
    sf.write(filename, audio, sample_rate)


def load_audio(filename:str):
    audio, sr = sf.read(filename)
    return audio, sr

def add_timestamps(audio: NDArray[np.float32], sample_rate: int) -> NDArray[np.float64]:
    time = np.arange(len(audio)) / sample_rate
    timed_audio = np.column_stack((time, audio))
    return timed_audio

def visualise(
    timed_audio: NDArray[np.float64],
    beats: NDArray[np.float64]
):
    plt.plot(timed_audio[:, 0], timed_audio[:, 1], label="Audio waveform")

    for beat in beats:
        plt.axvline(x=beat, color="red", alpha=0.7, linestyle="--")

    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Audio waveform with detected beats")
    plt.grid()
    plt.legend()
    plt.show()

def detect_beats(timed_audio, loudness_threshold:float, beat_separation:float=0.06)-> NDArray[np.float64]:
    beats = timed_audio[timed_audio[:, 1] > loudness_threshold, 0]
    first:np.float64 = None
    previous:np.float64 = None
    tbeats = []
    for beat in beats:
        if first is None:
            first = beat
            tbeats.append(first)
        if beat - first < beat_separation:
            previous = beat
            next
        elif beat - previous > beat_separation:
            first = beat
            tbeats.append(first)
    return tbeats
def to_notes(beats, tempo):
   notes = {} 


# record_audio("recording_test.wav", duration = 20)

audio, sample_rate = load_audio("recording_test.wav")
timed_audio = add_timestamps(audio, sample_rate)
beats = detect_beats(timed_audio, 0.035)
visualise(timed_audio, beats)
print(beats)


