from music import scales
from midi.midi import MidiWriter
from music.note import Note
from music.notes import Notes
from music.oscillator import FibonacciOscillator
from music.range import Range
from random import randint
from music.note_sequence import FibonacciNoteSequence
# from audio.audio import render_audio

def compose_midi(filename):
    key = Notes.ALL.choice()
    scale = scales.pick_a_scale(key)
    blues = False

    if randint(1, 4) == 3:
        blues = True
        scale = scales.generate_blues_scale(key)

    note_range = Range(Note(key, 2), Note(key, 6))
    osc = FibonacciOscillator(randint(0, 100))
    total_measures = randint(12, 60)

    filename = filename#'../output.mid'
    midi_writer = MidiWriter(filename)

    if randint(1, 12) == 12:
        tempo = randint(100, 400)
        midi_writer.write_12tone(total_measures * 4, tempo, osc)
    elif not blues and randint(0, 2) == 1:
        note_seq = FibonacciNoteSequence(scale, total_measures * 3, note_range, osc)
        tempo = randint(50, 200)
        midi_writer.write_waltz(note_seq, scale, tempo)
    else:
        note_seq = FibonacciNoteSequence(scale, total_measures * 4, note_range, osc)
        tempo = randint(100, 400)
        midi_writer.write(note_seq, scale, tempo, blues)

    # render_audio(filename, 'out.flac')
    # midi_player = MidiPlayer(44100, -16, 2, 1024)
    # midi_player.play(filename)