from midiutil.MidiFile import MIDIFile
# import pygame
from random import randint, shuffle

from music.note import Note
from music.notes import Notes


def get_midi_pitch(note):
    delta = note - Note(Notes.C)
    return 60 + delta


class MidiWriter:

    def __init__(self, filename):
        self.mf = MIDIFile(1)
        self.filename = filename
        self.track = 0
        self.channel = 0

    def write(self, note_sequence, scale, tempo, blues=False):
        time = 0
        self.mf.addTrackName(self.track, time, "Sample Track")
        self.mf.addTempo(self.track, time, tempo)

        chord_spacing = 4
        if note_sequence.pace == 3:
            next_chord = 1
        elif note_sequence.pace > 0:
            next_chord = 2
        next_chord = 0
        rand = randint(0, 2)
        use_arps = rand == 1
        use_rhythm = rand == 2
        prev_note = None

        for i in range(len(note_sequence.notes)):
            note = note_sequence.notes[i]
            if blues:
                self.write_note_blues(note, time)
            else:
                self.write_note(note, time)
            if time >= next_chord:
                if use_arps:
                    self.write_arp_from_note(note, scale, next_chord, chord_spacing / 4.0)
                elif prev_note is None:
                    if use_rhythm:
                        self.write_rhythm_from_note(note, scale, next_chord, chord_spacing)
                    else:
                        self.write_chord_from_note(note, scale, next_chord, chord_spacing)
                else:
                    if use_rhythm:
                        self.write_rhythm_from_note(prev_note, scale, next_chord, chord_spacing)
                    else:
                        self.write_chord_from_note(prev_note, scale, next_chord, chord_spacing)
                next_chord += chord_spacing
            time += note.duration
            prev_note = note

        self.write_chord_from_note(Note(scale.tonic, prev_note.octave), scale, next_chord, 16)

        with open(self.filename, 'wb') as outf:
            self.mf.writeFile(outf)

    def write_waltz(self, note_sequence, scale, tempo):
        time = 0
        self.mf.addTrackName(self.track, time, "Sample Track")
        self.mf.addTempo(self.track, time, tempo)

        chord_spacing = 3
        next_chord = 0
        use_arps = randint(0, 2)
        prev_note = None

        for i in range(len(note_sequence.notes)):
            note = note_sequence.notes[i]
            self.write_note(note, time)
            if time >= next_chord:
                if use_arps == 1:
                    self.write_waltz_arp_from_note(note, scale, next_chord)
                elif use_arps == 2:
                    self.write_waltz_arp_from_note_with_octave(note, scale, next_chord)
                elif prev_note is None:
                    self.write_waltz_chord_from_note(note, scale, next_chord)
                else:
                    self.write_waltz_chord_from_note(prev_note, scale, next_chord)
                next_chord += chord_spacing
            time += note.duration
            prev_note = note

        self.write_chord_from_note(Note(scale.tonic, prev_note.octave), scale, next_chord, 12)

        with open(self.filename, 'wb') as outf:
            self.mf.writeFile(outf)

    def write_12tone(self, length, tempo, osc):
        time = 0
        self.mf.addTrackName(self.track, time, "Sample Track")
        self.mf.addTempo(self.track, time, tempo)

        all_notes = Notes.ALL.list[:]
        available_notes = all_notes[:]
        prev_note = None
        next_bass = 0
        pace = randint(0, 3)

        for i in range(length):
            index = randint(0, len(available_notes) - 1)
            note = Note(available_notes[index])
            note.duration = self._calc_12tone_duration(i, pace)

            if prev_note is not None:
                if osc.direction and note < prev_note:
                    note.transpose(12)
                elif not osc.direction and note > prev_note:
                    note.transpose(-12)

            del available_notes[index]

            if len(available_notes) == 0:
                available_notes = all_notes[:]

            if time >= next_bass:
                bass_note = None
                bass_length = randint(1, 4)
                index = randint(0, len(available_notes) - 1)
                bass_note = Note(available_notes[index])
                while bass_note.name == note.name:
                    index = randint(0, len(available_notes) - 1)
                    bass_note = Note(available_notes[index])
                while bass_note >= note:
                    bass_note.transpose(-12)
                bass_note.duration = bass_length
                del available_notes[index]

                if len(available_notes) == 0:
                    available_notes = all_notes[:]

                self.write_note(bass_note, next_bass)
                next_bass += bass_length

                if len(available_notes) > 0 and randint(0, 1) == 1:
                    bass_note = None
                    index = randint(0, len(available_notes) - 1)
                    bass_note = Note(available_notes[index])
                    while bass_note.name == note.name:
                        index = randint(0, len(available_notes) - 1)
                        bass_note = Note(available_notes[index])
                    while bass_note >= note:
                        bass_note.transpose(-12)
                    bass_note.duration = bass_length
                    del available_notes[index]

                    if len(available_notes) == 0:
                        available_notes = all_notes[:]

                    self.write_note(bass_note, next_bass)

            self.write_note(note, time)

            time += note.duration
            prev_note = note
            osc.update(i)

        with open(self.filename, 'wb') as outf:
            self.mf.writeFile(outf)

    def _calc_12tone_duration(self, i, pace):
        max = 4 + pace
        lengths = [4, 2, 1, 3, 0.5, 0.75, 0.25]
        actual_lengths = lengths[:max]
        shuffle(actual_lengths)
        return actual_lengths[i % max]

    def write_note(self, note, time, is_waltz=False):
        pitch = get_midi_pitch(note)
        fixed_time = max(0, time + (randint(-3, 3) / 100.0))
        mod = time % 3 if is_waltz else time % 4
        mod = 1 if mod < 1 else int(mod)
        min_vol = 0 - mod - 3
        fixed_volume = min(100, note.volume + (randint(min_vol, 3)))
        self.mf.addNote(self.track, self.channel, pitch, fixed_time, note.duration, fixed_volume)

    def write_note_blues(self, note, time):
        pitch = get_midi_pitch(note)
        if time % 4 != 0:
            time += 0.3
        fixed_time = max(0, time + (randint(-3, 3) / 100.0))
        mod = time % 4
        mod = 1 if mod < 1 else int(mod)
        min_vol = 0 - mod - 3
        fixed_volume = min(100, note.volume + (randint(min_vol, 3)))
        self.mf.addNote(self.track, self.channel, pitch, fixed_time, note.duration, fixed_volume)

    def write_chord_from_note(self, note, scale, time, interval):
        chord = scale.select_chord(note)
        notes = chord.render(note, note.octave - 1, interval)
        for n in notes:
            self.write_note(n, time)

    def write_rhythm_from_note(self, note, scale, time, interval):
        chord = scale.select_chord(note)
        half = interval / 2
        notes = chord.render(note, note.octave - 1, half)
        self.write_note(notes[0], time)
        for i in range(1, len(notes)):
            self.write_note(notes[i], time + half)

    def write_arp_from_note(self, note, scale, time, interval):
        chord = scale.select_chord(note)
        notes = chord.render(note, note.octave - 1, interval)
        if len(notes) < 4:
            notes.append(notes[1])
        i = 0
        for n in notes:
            self.write_note(n, time + i)
            i += interval

    def write_waltz_chord_from_note(self, note, scale, time):
        chord = scale.select_chord(note)
        notes = chord.render(note, note.octave - 1, 1)
        self.write_note(notes[0], time, True)
        self.write_note(notes[1], time + 1, True)
        self.write_note(notes[2], time + 1, True)
        self.write_note(notes[1], time + 2, True)
        self.write_note(notes[2], time + 2, True)

    def write_waltz_arp_from_note_with_octave(self, note, scale, time):
        chord = scale.select_chord(note)
        notes = chord.render_include_octave(note, note.octave - 1, 1)
        self.write_note(notes[0], time, True)
        self.write_note(notes[1], time + 0.5, True)
        self.write_note(notes[2], time + 1, True)
        self.write_note(notes[3], time + 1.5, True)
        self.write_note(notes[2], time + 2, True)
        self.write_note(notes[1], time + 2.5, True)

    def write_waltz_arp_from_note(self, note, scale, time):
        chord = scale.select_chord(note)
        notes = chord.render(note, note.octave - 1, 1)
        self.write_note(notes[0], time, True)
        self.write_note(notes[1], time + 0.5, True)
        self.write_note(notes[2], time + 1, True)
        self.write_note(notes[1], time + 1.5, True)
        self.write_note(notes[2], time + 2, True)
        self.write_note(notes[1], time + 2.5, True)


# class MidiPlayer:
#
#     def __init__(self, sample_rate, bitsize, channels, buffer):
#         pygame.mixer.init(sample_rate, bitsize, channels, buffer)
#         pygame.mixer.music.set_volume(1.0)
#
#     def play(self, filename):
#         try:
#             clock = pygame.time.Clock()
#             pygame.mixer.music.load(filename)
#             pygame.mixer.music.play()
#             while pygame.mixer.music.get_busy():
#                 clock.tick(30)
#
#         except KeyboardInterrupt:
#             pygame.mixer.music.fadeout(1000)
#             pygame.mixer.music.stop()
#             raise SystemExit
