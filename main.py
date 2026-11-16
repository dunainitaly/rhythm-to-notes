import sounddevice as sd
import soundfile as sf


SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 5

rythm:list = []
temp:int = 60

def record_audio(filename):
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )

    sd.wait()
    sf.write(filename, audio, SAMPLE_RATE)

record_audio("recording.wav")
