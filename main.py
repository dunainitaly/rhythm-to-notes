import sounddevice as sd
from itertools import cycle
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
    filtered_beats = []
    for beat in beats:
        if first is None:
            first = beat
            filtered_beats.append(first)
        if beat - first < beat_separation:
            previous = beat
            next
        elif beat - previous > beat_separation:
            first = beat
            filtered_beats.append(first)
    return filtered_beats

def export_to_musescore(tempo_number:int, notes:dict[str,int], filename:str):
    score = stream.Score()
    part = stream.Part()

    part.append(meter.TimeSignature("4/4"))
    part.append(tempo.MetronomeMark(number=tempo_number))

    for pitch, duration in notes:
        n = note.Note(pitch)
        n.quarterLength = duration
        part.append(n)

    score.append(part)

    score.write("musicxml", fp=filename)

def find_closest(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        if abs(arr[left] - target) <= abs(arr[right] - target):
            right -= 1
        else:
            left += 1
    return arr[left]

def to_notes(beats, metronome:int):
    notes:dict[str,int] = []
    possible_notes = []

    iteration = 1
    notes_to_alternate = cycle(["C4", "E4"])
    maximum_note_duration:float=4
    minimal_note_duration = 0.2
    note_duration=maximum_note_duration
    while note_duration > minimal_note_duration:
        note_duration = maximum_note_duration/(2**iteration)
        possible_notes.append(note_duration)
        #if note_duration/3 > minimal_note_duration:
        #    possible_notes.append(note_duration/3)
        note_duration += maximum_note_duration/(2**(iteration+1))
        possible_notes.append(note_duration)
        iteration += 1
    possible_notes.sort()

    preprocessed_beats = []
    for iteration in range(len(beats)):
        preprocessed_beats.append(beats[0+iteration] - beats[0])

    for iteration, beat in enumerate(preprocessed_beats):
        if len(preprocessed_beats)>iteration+1:
            beat_duration = preprocessed_beats[iteration+1] - beat
            diff_tempo = beat_duration/(60/metronome)
            match = find_closest(possible_notes, diff_tempo)
            print(abs(diff_tempo-match))
            notes.append((next(notes_to_alternate), match))
    print(possible_notes,notes)
    return notes

record_filename = "150.wav"

# record_audio(record_filename, duration = 20)

loudness_threshold = 0.035
beat_separation = 0.06
metronome = 150

audio, sample_rate = load_audio(record_filename)
timed_audio = add_timestamps(audio, sample_rate)
beats = detect_beats(timed_audio,
                     loudness_threshold=loudness_threshold,
                     beat_separation=beat_separation
                ) 
notes = to_notes(beats, metronome)
#visualise(timed_audio, beats)
export_to_musescore(tempo_number = metronome, notes = notes, filename = "composition.musicxml")

