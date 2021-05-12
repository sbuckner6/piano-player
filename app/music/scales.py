from music.CircularList import CircularList
from music.chords import Chord
from music.note import Note
from music.notes import Notes
from music.oscillator import Oscillator
from random import randint


class Scale:

    def __init__(self, notes, tonic=None):
        self.notes = CircularList(notes)
        self.tonic = tonic

    def get_notes(self):
        return self.notes

    def get_random_note(self, note_range=None):
        note_name = self.notes.choice()
        note = Note(note_name)
        if note_range is not None:
            while note < note_range.bottom:
                note.transpose(12)
            while note > note_range.top:
                note.transpose(-12)
        return note

    def get_next_note(self, start_note, steps, direction):
        steps %= self.notes.size()
        steps = steps * -1 if not direction else steps
        index = self.notes.index(start_note.name) + steps
        note_name = self.notes.get(index)
        next_note = Note(note_name, start_note.octave)
        if direction == Oscillator.UP and next_note < start_note:
            next_note.transpose(12)
        elif direction == Oscillator.DOWN and next_note > start_note:
            next_note.transpose(-12)
        return next_note

    def __str__(self):
        return f"Scale{str(self.notes)}"


class DiatonicScale(Scale):

    def __init__(self, notes, tonic):
        super().__init__(notes, tonic)
        self.supertonic = self.notes.get(1)
        self.mediant = self.notes.get(2)
        self.subdominant = self.notes.get(3)
        self.dominant = self.notes.get(4)
        self.submediant = self.notes.get(5)
        self.leadingtone = self.notes.get(6)

    def get_tonic_triad(self):
        return Chord([self.tonic, self.mediant, self.dominant])

    def get_subdominant_triad(self):
        return Chord([self.subdominant, self.submediant, self.tonic])

    def get_dominant_triad(self):
        return Chord([self.dominant, self.leadingtone, self.supertonic])

    def get_submediant_triad(self):
        return Chord([self.submediant, self.tonic, self.mediant])

    def select_chord(self, note):
        chord = self.get_dominant_triad()
        if chord.contains(note):
            return chord
        chord = self.get_tonic_triad()
        if chord.contains(note):
            return chord
        return self.get_subdominant_triad()


class BluesScale(DiatonicScale):

    def __init__(self, notes, tonic):
        super().__init__(notes, tonic)
        self.bar = 0

    def get_tonic_triad(self):
        note = Note(self.tonic)
        mediant = note.transposed(4)
        dominant = note.transposed(7)
        leading = note.transposed(10)
        return Chord([self.tonic, mediant.name, dominant.name, leading.name])

    def get_subdominant_triad(self):
        note = Note(self.tonic).transposed(5)
        mediant = note.transposed(4)
        dominant = note.transposed(7)
        leading = note.transposed(10)
        return Chord([self.tonic, mediant.name, dominant.name, leading.name])

    def get_dominant_triad(self):
        note = Note(self.tonic).transposed(7)
        mediant = note.transposed(4)
        dominant = note.transposed(7)
        leading = note.transposed(10)
        return Chord([self.tonic, mediant.name, dominant.name, leading.name])

    def select_chord(self, note):
        if self.bar == 8:
            return self.get_dominant_triad()
        elif self.bar in [4, 5, 9]:
            return self.get_subdominant_triad()
        else:
            return self.get_tonic_triad()
        self.bar += 1
        if self.bar == 12:
            self.bar = 0


def generate_chromatic_scale():
    return Scale(Notes.ALL)


def _generate_scale(start_note, step_sequence):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in step_sequence:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return Scale(notes_in_scale, start_note)


def generate_major_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [2, 2, 1, 2, 2, 2]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)


def generate_dorian_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [2, 1, 2, 2, 2, 1]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)


def generate_phyrigian_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [1, 2, 2, 2, 1, 2]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)


def generate_lydian_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [2, 2, 2, 1, 2, 2]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)


def generate_mixolydian_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [2, 2, 1, 2, 2, 1]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)


def generate_minor_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [2, 1, 2, 2, 1, 2]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)


def generate_locrian_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [1, 2, 2, 1, 2, 2]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)

def generate_harmonic_minor_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [2, 1, 2, 2, 1, 3]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return DiatonicScale(notes_in_scale, start_note)


def generate_blues_scale(start_note):
    index = Notes.ALL.index(start_note)
    max_scale_length = Notes.ALL.size()
    notes_in_scale = [start_note]
    for step in [3, 2, 1, 2, 3]:
        index += step
        index = index - max_scale_length if index >= max_scale_length else index
        notes_in_scale.append(Notes.ALL.get(index))
    return BluesScale(notes_in_scale, start_note)


def pick_a_scale(start_note):
    choice = randint(1, 15)
    if choice == 1:
        return generate_harmonic_minor_scale(start_note)
    elif choice == 2:
        return generate_dorian_scale(start_note)
    elif choice == 3:
        return generate_phyrigian_scale(start_note)
    elif choice == 4:
        return generate_lydian_scale(start_note)
    elif choice == 5:
        return generate_mixolydian_scale(start_note)
    elif choice == 6:
        return generate_locrian_scale(start_note)
    elif choice == 7:
        return generate_dorian_scale(start_note)
    elif choice < 11:
        return generate_minor_scale(start_note)
    else:
        return generate_major_scale(start_note)



def generate_pentatonic_scale(start_note):
    return _generate_scale(start_note, [2, 2, 3, 2])

