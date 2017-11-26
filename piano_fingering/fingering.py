# Fingering algorithm
#
# Ported in Python from https://github.com/blakewest/performer,
# by Blake West
#
# Use it by calling:
#
#    fingered_notes = computeFingering(notes, 'right')
#
# or
#
#    fingered_notes = computeFingering(notes, 'left')
#
# This function accepts a list of MIDI notes. The elements of the list
# can have the following formats:
#
#     - A single note: 60
#     - A chord: [60, 62, 64]
#     - A single note with fingering: { 'notes': [60], 'fingers': [1] }
#     - A chord with fingering: { 'notes': [60, 62, 64], 'fingers': [1, 2, 3] }
#     - A rest: []
#
# Each entry in the returned list has the following format:
#
#  { 'notes': [note1, ..., noteN], 'fingers': [finger1, ..., fingerN] }
#
# If fingering is provided in input, it is respected to compute the
# fingering of the other notes.


from collections import namedtuple
from copy import copy
import math
from .cost import createCostDatabase


#----------------------------------------------------------


RIGHT_HAND_COST_DATABASE, LEFT_HAND_COST_DATABASE = createCostDatabase()


NotesInfo = namedtuple('NotesInfo', ['notes', 'fingers'])


#----------------------------------------------------------


def computeFingering(notes, left_or_right):
    """Compute the best fingering for the provided list of MIDI notes

    'left_or_right' must be either 'left' or 'right'.

    The elements of the list of MIDI notes can have the following formats:

      - A single note: 60
      - A chord: [60, 62, 64]
      - A single note with fingering: { 'notes': [60], 'fingers': [1] }
      - A chord with fingering: { 'notes': [60, 62, 64], 'fingers': [1, 2, 3] }
      - A rest: []

    Each entry in the returned list has the following format:

      { 'notes': [note1, ..., noteN], 'fingers': [finger1, ..., fingerN] }

    If fingering is provided in input, it is respected to compute the
    fingering of the other notes.
    """
    notes, rests = preprocessNotes(notes)

    layers = [ [Node([], [])] ]

    for infos in notes:
        layers.append(makeLayer(infos.notes, left_or_right, infos.fingers))

    # Go through each layer
    for layer_index in range(1, len(layers)):

        # Go through each node in the layer
        for current_node in layers[layer_index]:
            min_score = float('inf')

            # Go through each node in the previous layer
            for previous_node in layers[layer_index - 1]:
                total_cost = previous_node.score

                cost = calcCost(current_node, previous_node, left_or_right)

                total_cost += cost

                if total_cost < min_score:
                    min_score = total_cost
                    current_node.score = total_cost
                    current_node.best_previous_node = previous_node

    # Find the best final node
    best_node = layers[-1][0]
    for node in layers[-1][1:]:
        if node.score < best_node.score:
            best_node = node

    # Walk the nodes backward to construct the best path
    result = []
    while best_node is not None:
        result.insert(0, dict(notes=best_node.notes, fingers=best_node.fingers))
        best_node = best_node.best_previous_node

    result = result[1:]

    for rest in rests:
        result.insert(rest, dict(notes=[], fingers=[]))

    return result


#----------------------------------------------------------


def getAllFingerOptions(nb_fingers, left_or_right):
    results = []
    finger_options = [1, 2, 3, 4, 5]

    def walk(nb_fingers, current_fingers, finger_options):
        if len(current_fingers) == nb_fingers:
            current = copy(current_fingers)
            current.sort()
            if left_or_right == 'left':
                current.reverse()
            results.append(current)
            return

        for i in range(0, len(finger_options)):
            current = current_fingers + [finger_options[i]]
            walk(nb_fingers, current, finger_options[0:i])

    walk(nb_fingers, [], finger_options)

    return results


# Initialize finger options object
ALL_FINGER_OPTIONS_RIGHT = {}
ALL_FINGER_OPTIONS_LEFT = {}

for i in range(1, 6):
    ALL_FINGER_OPTIONS_RIGHT[i] = getAllFingerOptions(i, 'right')
    ALL_FINGER_OPTIONS_RIGHT[i].sort()

    ALL_FINGER_OPTIONS_LEFT[i] = getAllFingerOptions(i, 'left')
    ALL_FINGER_OPTIONS_LEFT[i].sort()


#----------------------------------------------------------


def preprocessNotes(notes):
    result = []
    rests = []

    for index, entry in enumerate(notes):
        if isinstance(entry, list):
            if len(entry) > 0:
                result.append(NotesInfo(notes=entry, fingers=None))
            else:
                rests.append(index)
        elif isinstance(entry, dict):
            result.append(NotesInfo(notes=entry['notes'], fingers=entry['fingers']))
        else:
            result.append(NotesInfo(notes=[entry], fingers=None))

    return result, rests


#----------------------------------------------------------


class Node(object):

    def __init__(self, notes, fingers):
        self.notes = notes
        self.fingers = fingers
        self.score = 0
        self.best_previous_node = None


def makeLayer(notes, left_or_right, fingers=None):
    layer = []

    if fingers is not None:
        layer.append(Node(notes, fingers))
    else:
        if left_or_right == 'right':
            options = ALL_FINGER_OPTIONS_RIGHT[len(notes)]
        else:
            options = ALL_FINGER_OPTIONS_LEFT[len(notes)]

        for option in options:
            layer.append(Node(notes, option))

    return layer


#----------------------------------------------------------


def computeRightHandCost(n1, n2, f1, f2):
    key = '%d,%d,%d,%d' % (n1, n2, f1, f2)
    return RIGHT_HAND_COST_DATABASE[key]


#----------------------------------------------------------


def computeLeftHandCost(n1, n2, f1, f2):
    key = '%d,%d,%d,%d' % (n1, n2, abs(f1), abs(f2))
    return LEFT_HAND_COST_DATABASE[key]


#----------------------------------------------------------


def calcCost(current_node, previous_node, left_or_right):
    if left_or_right == 'left':
        costFunction = computeLeftHandCost
    else:
        costFunction = computeRightHandCost

    total_cost = 0

    # Go through each note in the current node
    for i in range(0, len(current_node.notes)):
        current_note = current_node.notes[i]
        current_finger = current_node.fingers[i]

        # This helps add the "state" cost of actually using those fingers for
        # that chord. This isn't captured by the transition costs
        has_next_note = i < len(current_node.notes) - 1
        if has_next_note:
            next_note = current_node.notes[i + 1]
            next_finger = current_node.fingers[i + 1]
            total_cost += costFunction(current_note, next_note, current_finger, next_finger)

        # Add up scores for each of the previous nodes notes trying to get to current node note
        for j in range(0, len(previous_node.notes)):
            previous_note = previous_node.notes[j]
            previous_finger = previous_node.fingers[j]

            total_cost += costFunction(previous_note, current_note, previous_finger, current_finger)

    return total_cost
