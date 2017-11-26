from unittest import TestCase
from ..fingering import computeFingering
from ..midi import listToMidi


class TestFingering(TestCase):

    def process(self, notes, expected, left_or_right):
        fingered_notes = computeFingering(notes, left_or_right)
        self.assertEqual(expected, fingered_notes)

    def test_C_scale_right_hand(self):
        notes = [
            60,
            62,
            64,
            65,
            67,
            69,
            71,
            72,
        ]

        expected = [
            dict(notes=[60], fingers=[1]),
            dict(notes=[62], fingers=[2]),
            dict(notes=[64], fingers=[3]),
            dict(notes=[65], fingers=[1]),
            dict(notes=[67], fingers=[2]),
            dict(notes=[69], fingers=[3]),
            dict(notes=[71], fingers=[4]),
            dict(notes=[72], fingers=[5]),
        ]

        self.process(notes, expected, 'right')

    def test_C_scale_left_hand(self):
        notes = [
            60,
            62,
            64,
            65,
            67,
            69,
            71,
            72,
        ]

        expected = [
            dict(notes=[60], fingers=[5]),
            dict(notes=[62], fingers=[4]),
            dict(notes=[64], fingers=[3]),
            dict(notes=[65], fingers=[2]),
            dict(notes=[67], fingers=[1]),
            dict(notes=[69], fingers=[3]),
            dict(notes=[71], fingers=[2]),
            dict(notes=[72], fingers=[1]),
        ]

        self.process(notes, expected, 'left')

    def test_notes_and_rest_right_hand(self):
        notes = [
            60,
            [],
            64,
        ]

        expected = [
            dict(notes=[60], fingers=[1]),
            dict(notes=[], fingers=[]),
            dict(notes=[64], fingers=[3]),
        ]

        self.process(notes, expected, 'right')

    def test_notes_and_rest_left_hand(self):
        notes = [
            60,
            [],
            64,
        ]

        expected = [
            dict(notes=[60], fingers=[3]),
            dict(notes=[], fingers=[]),
            dict(notes=[64], fingers=[1]),
        ]

        self.process(notes, expected, 'left')

    def test_chords_right_hand(self):
        notes = [
            [60, 62, 64],
            [67, 71, 74],
        ]

        expected = [
            dict(notes=[60, 62, 64], fingers=[1, 2, 3]),
            dict(notes=[67, 71, 74], fingers=[1, 3, 5]),
        ]

        self.process(notes, expected, 'right')

    def test_chords_left_hand(self):
        notes = [
            [60, 62, 64],
            [67, 71, 74],
        ]

        expected = [
            dict(notes=[60, 62, 64], fingers=[5, 3, 1]),
            dict(notes=[67, 71, 74], fingers=[3, 2, 1]),
        ]

        self.process(notes, expected, 'left')

    def test_fingered_notes_right_hand(self):
        notes = [
            60,
            62,
            64,
            dict(notes=[65], fingers=[4]),
            67,
            69,
            71,
            72,
        ]

        expected = [
            dict(notes=[60], fingers=[1]),
            dict(notes=[62], fingers=[2]),
            dict(notes=[64], fingers=[3]),
            dict(notes=[65], fingers=[4]),
            dict(notes=[67], fingers=[1]),
            dict(notes=[69], fingers=[2]),
            dict(notes=[71], fingers=[3]),
            dict(notes=[72], fingers=[4]),
        ]

        self.process(notes, expected, 'right')

    def test_fingered_notes_left_hand(self):
        notes = [
            60,
            62,
            64,
            65,
            dict(notes=[67], fingers=[4]),
            69,
            71,
            72,
        ]

        expected = [
            dict(notes=[60], fingers=[4]),
            dict(notes=[62], fingers=[3]),
            dict(notes=[64], fingers=[2]),
            dict(notes=[65], fingers=[1]),
            dict(notes=[67], fingers=[4]),
            dict(notes=[69], fingers=[3]),
            dict(notes=[71], fingers=[2]),
            dict(notes=[72], fingers=[1]),
        ]

        self.process(notes, expected, 'left')
