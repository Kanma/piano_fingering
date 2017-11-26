=================
 piano_fingering
=================

.. image:: https://travis-ci.org/Kanma/piano_fingering.svg?branch=v1.0.0
    :target: https://travis-ci.org/Kanma/piano_fingering


A Python library to automatically determine the fingering of a serie of notes.

The algorithm is adapted from the corresponding one from
https://github.com/blakewest/performer, by Blake West.



Installation
============

To install this library, do::

    $ pip install piano_fingering



Usage
=====

Single notes
------------

The algorithm takes a list of MIDI notes as input::

    from piano_fingering import computeFingering

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

    fingered_notes = computeFingering(notes, 'right')   # or 'left'


The code above will produce the following output::

    fingered_notes = [
        {'notes': [60], 'fingers': [1]},
        {'notes': [62], 'fingers': [2]},
        {'notes': [64], 'fingers': [3]},
        {'notes': [65], 'fingers': [1]},
        {'notes': [67], 'fingers': [2]},
        {'notes': [69], 'fingers': [3]},
        {'notes': [71], 'fingers': [4]},
        {'notes': [72], 'fingers': [5]},
    ]


Chords
------

You can add chords to the list too::

    notes = [
        [60, 62, 64],
        [67, 71, 74],
    ]

    fingered_notes = computeFingering(notes, 'right')


The code above will produce the following output::

    fingered_notes = [
        {'notes': [60, 62, 64], 'fingers': [1, 2, 3]},
        {'notes': [67, 71, 74], 'fingers': [1, 3, 5]},
    ]


Rests
-----

A rest is specified by an empty list. Note that the algorithm doesn't take
rests in consideration. They are supported to help the user of the library to
use the result list. It is up to you to separate your notes on long rests,
so the fingering of one part of the song doesn't affect another one.

Example::

    notes = [
        60,
        [],
        64,
    ]

    fingered_notes = computeFingering(notes, 'right')


The code above will produce the following output::

    fingered_notes = [
        {'notes': [60], 'fingers': [1]},
        {'notes': [], 'fingers': []},
        {'notes': [64], 'fingers': [3]},
    ]


User-defined fingering
----------------------

In case the algorithm doesn't produce a fingering that you find optimal, you
can constrain it by specifying your own fingering on the input::

    notes = [
        60,
        62,
        64,
        {'notes': [65], 'fingers': [4]},
        67,
        69,
        71,
        72,
    ]

    fingered_notes = computeFingering(notes, 'right')   # or 'left'


The code above will produce the following output::

    fingered_notes = [
        {'notes': [60], 'fingers': [1]},
        {'notes': [62], 'fingers': [2]},
        {'notes': [64], 'fingers': [3]},
        {'notes': [65], 'fingers': [4]},
        {'notes': [67], 'fingers': [1]},
        {'notes': [69], 'fingers': [2]},
        {'notes': [71], 'fingers': [3]},
        {'notes': [72], 'fingers': [4]},
    ]


Converting a note name to a MIDI note
-------------------------------------

Two helpers functions are provided to convert note names (like *C5*, *A#*, *Bb3*)
to MIDI notes.

To convert a single note name, use::

    from piano_fingering import nameToMidi

    midi_note = nameToMidi('C4')

When the octave isn't indicated, '5' is assumed.


To convert a list of notes (with the same format than for *computeFingering()* in
the above examples), use::

    from piano_fingering import listToMidi

    notes = [
        'C5',
        ['C5', 'E5', 'G5'],
        {'notes': ['C5'], 'fingers': [1]},
    ]

    midi_notes = listToMidi(notes)



Running tests
=============

In the source package, do::

    $ python setup.py test



License
=======

*piano_fingering* is is made available under the MIT License. The text of the license
is in the file "LICENSE.txt".

Under the MIT License you may use *piano_fingering* for any purpose you wish, without
warranty, and modify it if you require, subject to one condition:

    "The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software."

In practice this means that whenever you distribute your application, whether as binary
or as source code, you must include somewhere in your distribution the text in the file
"LICENSE.txt". This might be in the printed documentation, as a file on delivered media,
or even on the credits / acknowledgements of the runtime application itself; any of
those would satisfy the requirement.

Even if the license doesn't require it, please consider to contribute your modifications
back to the community.



Special thanks to
=================

Blake West, for the initial javascript implementation.
