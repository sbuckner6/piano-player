from music.notes import Notes


class Note:

    _NOTE_VALUES = {
        Notes.C: 0,
        Notes.Db: 1,
        Notes.D: 2,
        Notes.Eb: 3,
        Notes.E: 4,
        Notes.F: 5,
        Notes.Gb: 6,
        Notes.G: 7,
        Notes.Ab: 8,
        Notes.A: 9,
        Notes.Bb: 10,
        Notes.B: 11
    }

    def __init__(self, name, octave=4, duration=0.25, volume=100):
        self.name = name
        self.octave = octave
        self.duration = duration
        self.volume = volume

    def transpose(self, steps):
        while steps >= 12:
            steps -= 12
            self.octave += 1

        while steps <= -12:
            steps += 12
            self.octave -= 1

        if steps == 0:
            return

        index = Notes.ALL.index(self.name)
        index += steps

        if index >= 12:
            index -= 12
            self.octave += 1
        elif steps < 0:
            index += 12
            self.octave -= 1

        self.name = Notes.ALL.get(index)

    def transposed(self, steps):
        note = Note(self.name, self.octave, self.duration, self.volume)
        note.transpose(steps)
        return note

    def __int__(self):
        return 12 * self.octave + self._NOTE_VALUES[self.name]

    def __sub__(self, other):
        return int(self) - int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __ne__(self, other):
        return int(self) != int(other)

    def __str__(self):
        return f"{self.name}{self.octave}"