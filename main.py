from piano_fingering.cost import createCostDatabase
from piano_fingering.fingering import computeFingering
from piano_fingering.midi import listToMidi
from pprint import pprint


right_hand_cost_database, left_hand_cost_database = createCostDatabase()

print(right_hand_cost_database['48,50,1,2'])
print(left_hand_cost_database['48,50,1,2'])
print(left_hand_cost_database['48,50,5,4'])

notes = [
    'C4',
    'D4',
    'E4',
    'F4',
    'G4',
    'A4',
    'B4',
    'C5',
    [],
    'C5',
    'B4',
    'A4',
    'G4',
    'F4',
    'E4',
    'D4',
    'C4',
    [],
    ['E4', 'G4', 'C5'],
    dict(notes=['E4', 'G4', 'B4'], fingers=[1, 3, 5]),
    ['F4', 'A4', 'C5'],
    ['F4', 'A4', 'D5'],
]

notes = listToMidi(notes)


notes = computeFingering(notes, 'left')

pprint(notes)
