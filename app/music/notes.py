from music.CircularList import CircularList
from music.errors import InvalidNoteError


class Notes:

    A = 'A'
    Bb = 'Bb'
    B = 'B'
    C = 'C'
    Db = 'Db'
    D = 'D'
    Eb = 'Eb'
    E = 'E'
    F = 'F'
    Gb = 'Gb'
    G = 'G'
    Ab = 'Ab'

    ALL = CircularList([
        C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B
    ])

    _NOTE_NAMES = {
        'ab': Ab,
        'a': A,
        'a#': Bb,
        'bb': Bb,
        'b': B,
        'b#': C,
        'cb': B,
        'c': C,
        'c#': Db,
        'db': Db,
        'd': D,
        'd#': Eb,
        'eb': Eb,
        'e': E,
        'e#': F,
        'fb': E,
        'f': F,
        'f#': Gb,
        'gb': Gb,
        'g': G,
        'g#': Ab
    }

    @staticmethod
    def parse(note_str):
        note_str_lower = str(note_str).lower()
        if note_str_lower not in Notes._NOTE_NAMES:
            raise InvalidNoteError(note_str_lower)
        return Notes._NOTE_NAMES[note_str_lower]