from unittest import TestCase
from ..midi import nameToMidi
from ..midi import listToMidi


class TestNameToMidi(TestCase):

    def process(self, names):
        current_note = 0
        for octave in range(0, 11):
            names_with_octave = [ x + str(octave) for x in names ]
            for name in names_with_octave:
                self.assertEqual(current_note, nameToMidi(name))
                current_note += 1

    def test_natural_and_sharp_notes(self):
        self.process(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])

    def test_natural_and_flat_notes(self):
        self.process(['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'])


#----------------------------------------------------------


class TestListToMidi(TestCase):

    def process(self, notes, expected):
        midi_notes = listToMidi(notes)
        self.assertEqual(len(expected), len(midi_notes))
        self.assertEqual(expected, midi_notes)

    def test_single_notes(self):
        notes = ['C5', 'D5', 'E5']
        expected = [60, 62, 64]
        self.process(notes, expected)

    def test_chords(self):
        notes = [
            ['C5', 'D5', 'E5'],
            ['G5', 'B5', 'D6']
        ]

        expected = [
            [60, 62, 64],
            [67, 71, 74]
        ]

        self.process(notes, expected)

    def test_rest(self):
        notes = []
        expected = []
        self.process(notes, expected)

    def test_fingered_single_notes(self):
        notes = [
            dict(notes=['C5'], fingers=[1]),
            dict(notes=['E5'], fingers=[3]),
            dict(notes=['G5'], fingers=[5]),
        ]

        expected = [
            dict(notes=[60], fingers=[1]),
            dict(notes=[64], fingers=[3]),
            dict(notes=[67], fingers=[5]),
        ]

        self.process(notes, expected)

    def test_fingered_chords(self):
        notes = [
            dict(notes=['C5', 'D5', 'E5'], fingers=[1, 2, 3]),
            dict(notes=['G5', 'B5', 'D6'], fingers=[1, 3, 5])
        ]

        expected = [
            dict(notes=[60, 62, 64], fingers=[1, 2, 3]),
            dict(notes=[67, 71, 74], fingers=[1, 3, 5])
        ]

        self.process(notes, expected)

    def test_mixed(self):
        notes = [
            'C5',
            ['C5', 'D5', 'E5'],
            [],
            dict(notes=['C5'], fingers=[1]),
            dict(notes=['G5', 'B5', 'D6'], fingers=[1, 3, 5])
        ]

        expected = [
            60,
            [60, 62, 64],
            [],
            dict(notes=[60], fingers=[1]),
            dict(notes=[67, 71, 74], fingers=[1, 3, 5])
        ]

        self.process(notes, expected)
