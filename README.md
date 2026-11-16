# Rhythm to Notes 

A small Python project that converts audio recordings into musical notes. It detects beats using audio amplitude, estimates note durations, and exports the result as a MusicXML file compatible with MuseScore.

## Features

- Record and load WAV audio files.
- Detect beats using amplitude thresholds.
- Visualise waveforms and detected beats.
- Convert beat intervals into musical note durations.
- Export compositions to MusicXML.

## Installation

```bash
git clone https://github.com/dunainitaly/rhythm-to-notes.git
cd rhythm-to-notes
chmod +x setup.sh
./setup.sh
```

Alternatively, install dependencies manually:

```bash
pip install -r requirements.txt
```

## Usage

Place or record a WAV file named `recording.wav` in the project directory and run:

```bash
python main.py
```

The generated composition will be saved as `composition.musicxml`. Open it in MuseScore to view and edit the notes.

## Configuration

Adjust these parameters in `main.py`:

```python
loudness_threshold = 0.035  # Beat detection sensitivity
beat_separation = 0.06      # Minimum time between beats (seconds)
metronome = 150             # Tempo (BPM)
```

## Requirements

- Python 3.10+
- NumPy
- SoundDevice
- SoundFile
- Matplotlib
- Music21


