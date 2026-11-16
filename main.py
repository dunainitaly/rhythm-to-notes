import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np

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

def visualise(audio, sample_rate):
    time = np.arange(len(audio)) / sample_rate

    plt.plot(time, audio)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Audio waveform")
    plt.grid()
    plt.show()
def detect_beats(timed_audio):
    pass

audio, sample_rate = load_audio("recording.wav")
timed_audio = add_timestamps(audio, sample_rate)
print(timed_audio)
