import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 5

rythm:list = []
temp:int = 60

def record_audio(filename:str):
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )

    sd.wait()
    sf.write(filename, audio, SAMPLE_RATE)

def load_audio(filename:str):
    audio, sr = sf.read(filename)
    return audio, sr

def add_timestamps(audio, sample_rate):
    time = np.arange(len(audio)) / sample_rate
    timed_audio = np.column_stack((time, audio))
    return timed_audio

def visualise(timed_audio: NDArray[np.float64]):
    time = np.arange(len(audio)) / sample_rate

    plt.plot(timed_audio[:, 0], timed_audio[:, 1])
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Audio waveform")
    plt.grid()
    plt.show()

def detect_beats(timed_audio, treshold:float)-> NDArray[np.float64]:
    beats = np.argwhere(timed_audio[:, 1]>treshold)
    return beats

# record_audio("recording.wav")

audio, sample_rate = load_audio("recording.wav")
timed_audio = add_timestamps(audio, sample_rate)
beats = detect_beats(timed_audio, 0.75)
visualise(timed_audio)
print(beats)


plt.figure()
plt.hlines(1,1,20)  # Draw a horizontal line
plt.eventplot(beats, orientation='horizontal', colors='b')
plt.axis('off')
plt.show()


