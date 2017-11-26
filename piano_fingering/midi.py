# MIDI-related utility functions


NOTE_INDICES = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11,
}


#----------------------------------------------------------


def nameToMidi(name):
    """Return the MIDI note corresponding to the provided note name

    Example of valid note names: C, C5, C#, C#3, Db, Db5

    When the octave isn't indicated, '5' is assumed
    """
    note = NOTE_INDICES[name[0]]
    octave = 5

    offset = 1

    if len(name) > 1:
        if name[1] == 'b':
            note -= 1
            offset = 2
        elif name[1] == '#':
            note += 1
            offset = 2

    if len(name) > offset:
        try:
            octave = int(name[offset:])
        except:
            pass

    return octave * 12 + note


#----------------------------------------------------------


def listToMidi(notes):
    """Convert a list of note names into a list of MIDI notes

    See 'nameToMidi()' for examples of valid note names.

    The elements of the list can have the following formats:
    
      - A single note: 'C'
      - A chord: ['C', 'D', 'E']
      - A single note with fingering: { 'notes': ['C'], 'fingers': [1] }
      - A chord with fingering: { 'notes': ['C', 'D', 'E'], 'fingers': [1, 2, 3] }
      - A rest: []
    """
    result = []

    for x in notes:
        if isinstance(x, dict):
            result.append(dict(notes=listToMidi(x['notes']), fingers=x['fingers']))
        elif isinstance(x, list):
            result.append(listToMidi(x))
        else:
            result.append(nameToMidi(x))

    return result
