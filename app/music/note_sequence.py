from music.oscillator import Oscillator
from random import shuffle, randint


def generate_fibonacci_sequence(n):
    seq = fib(n)
    i = randint(0, len(seq))
    return seq


def fib(n):
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        seq = fib(n-1)
        seq.append(seq[-1] + seq[-2])
        return seq


def generate_note_sequence(scale, ticks, note_range, osc):
    fib_seq = generate_fibonacci_sequence(ticks)
    current_note = scale.get_random_note(note_range)
    note_seq = [current_note]
    for i in range(ticks):
        steps_to_next_note = fib_seq[i]
        while True:
            next_note = scale.get_next_note(current_note, steps_to_next_note, osc.direction)
            if next_note < note_range.bottom:
                osc.direction = Oscillator.UP
            elif next_note > note_range.top:
                osc.direction = Oscillator.DOWN
            else:
                note_seq.append(next_note)
                current_note = next_note
                osc.update(i)
                break
    return note_seq


class NoteSequence:

    def __init__(self, scale, ticks, note_range, osc):
        self.notes = []
        self.pace = randint(0, 3)

    def __str__(self):
        return f"NoteSequence{str(list(map(lambda note: str(note), self.notes)))}"


class FibonacciNoteSequence(NoteSequence):

    def __init__(self, scale, ticks, note_range, osc):
        super().__init__(scale, ticks, note_range, osc)
        fib_seq = generate_fibonacci_sequence(ticks)
        current_note = scale.get_random_note(note_range)
        current_note.duration = self._calc_duration(0)
        self.notes = [current_note]
        for i in range(ticks):
            steps_to_next_note = fib_seq[i]
            while True:
                next_note = scale.get_next_note(current_note, steps_to_next_note, osc.direction)
                if next_note < note_range.bottom:
                    osc.direction = Oscillator.UP
                elif next_note > note_range.top:
                    osc.direction = Oscillator.DOWN
                else:
                    next_note.duration = self._calc_duration(i)
                    self.notes.append(next_note)
                    current_note = next_note

                    # if current_note == next_note and randint(0, 1) == 1:
                    #     self.notes[-1].duration += 0.25
                    #     current_note = self.notes[-1]
                    # else:
                    #     self.notes.append(next_note)
                    #     current_note = next_note

                    osc.update(i)
                    break

    def _calc_duration(self, i):
        max = 4 + self.pace
        lengths = [4, 2, 1, 3, 0.5, 0.75, 0.25]
        actual_lengths = lengths[:max]
        shuffle(actual_lengths)
        return actual_lengths[i % max]