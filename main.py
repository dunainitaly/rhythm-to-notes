import sounddevice as sd
import soundfile as sf


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

record_audio("recording.wav")
audio, sr = load_audio("recording.wav")

