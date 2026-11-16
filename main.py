import sounddevice as sd
from music21 import stream, note, meter, tempo
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

def export_to_musescore(tempo_number:int, notes:dict[str,int]):
    score = stream.Score()
    part = stream.Part()
    for notee in notes:
        print(notee)

    part.append(meter.TimeSignature("4/4"))
    part.append(tempo.MetronomeMark(number=tempo_number))
    print(notes)

    for pitch, duration in notes:
        n = note.Note(pitch)
        n.quarterLength = duration
        part.append(n)

    score.append(part)

    score.write("musicxml", fp="composition.musicxml")

def find_closest(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        if abs(arr[left] - target) <= abs(arr[right] - target):
            right -= 1
        else:
            left += 1
    return arr[left]

def to_notes(beats, metronome:int, sensitivity):
    notes:dict[str,int] = []
    possible_notes = []

    i = 1
    note_duration:float=10
    while note_duration > 0.04:
        note_duration = 4/(2**i)
        possible_notes.append(note_duration)
        # possible_notes.append(note_duration/3)
        note_duration += 4/(2**(i+1))
        possible_notes.append(note_duration)
        i += 1
    possible_notes.sort()
    preprocessed_beats = []
    print(possible_notes)
    for i in range(len(beats)):
        preprocessed_beats.append(beats[0+i] - beats[0])
    for i, beat in enumerate(preprocessed_beats):
        print(len(preprocessed_beats),i)
        if len(preprocessed_beats)>i+1:
            beat_duration = preprocessed_beats[i+1] - beat
            diff_tempo = beat_duration/(60/metronome)
            match = find_closest(possible_notes, diff_tempo)
            notes.append(("C4", match))
            print(beat_duration, preprocessed_beats[i +1],beat, diff_tempo)
    return notes

record_filename = "150.wav"

# record_audio(record_filename, duration = 20)

loudness_threshold = 0.035
beat_separation = 0.06
metronome = 140

audio, sample_rate = load_audio(record_filename)
timed_audio = add_timestamps(audio, sample_rate)
beats = detect_beats(timed_audio,
                     loudness_threshold=loudness_threshold,
                     beat_separation=beat_separation
                ) 
notes = to_notes(beats, metronome, beat_separation)
visualise(timed_audio, beats)
export_to_musescore(tempo_number = metronome, notes = notes)

