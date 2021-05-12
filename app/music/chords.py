from music.CircularList import CircularList
from music.note import Note


class Chord:

    def __init__(self, notes):
        self.notes = CircularList(notes)

    def transpose(self, steps):
        self.notes = CircularList([note.transpose(steps) for note in self.notes.list])

    def contains(self, note):
        return self.notes.contains(note.name)

    def render(self, from_note, octave=4, duration=4, volume=80):
        rendered_notes = [Note(name, octave, duration, volume) for name in self.notes.list]

        for i in range(1, len(rendered_notes)):
            if rendered_notes[i] < rendered_notes[i-1]:
                rendered_notes[i].transpose(12)

        j = len(rendered_notes) - 1

        while rendered_notes[j] >= from_note:
            rendered_notes[j].transpose(-12)
            rendered_notes = rendered_notes[j:] + rendered_notes[:j]

        return rendered_notes

    def render_include_octave(self, from_note, octave=4, duration=4, volume=80):
        rendered_notes = [Note(name, octave, duration, volume) for name in self.notes.list]
        rendered_notes.append(rendered_notes[0].transposed(12))

        for i in range(1, len(rendered_notes)):
            if rendered_notes[i] < rendered_notes[i-1]:
                rendered_notes[i].transpose(12)

        j = len(rendered_notes) - 1

        while rendered_notes[j] >= from_note:
            rendered_notes[j].transpose(-12)
            rendered_notes = rendered_notes[j:] + rendered_notes[:j]

        return rendered_notes

    def __str__(self):
        return f"Chord{str(self.notes)}"