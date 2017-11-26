# Cost functions for various types of moves between notes
#
# Ported in Python from https://github.com/blakewest/performer,
# by Blake West
#
# Use it by calling:
#
#    right_hand_cost_database, left_hand_cost_database = createCostDatabase()
#
# This will compute a cost table for all possible moves in the right and
# left hands


import math


#----------------------------------------------------------


MOVE_CUTOFF = 7.5


#----------------------------------------------------------


FINGER_DISTANCE = {
  '1,1': 0,
  '1,2': 2,
  '1,3': 3.5, # Making an allowance since this seriously is either 3 or 4 about half the time
  '1,4': 5,
  '1,5': 7,
  '2,1': 2,
  '2,2': 0,
  '2,3': 2,
  '2,4': 3.5,  # Same
  '2,5': 5,
  '3,1': 3.5, # Same
  '3,2': 2,
  '3,3': 0,
  '3,4': 2,
  '3,5': 3.5, # Same
  '4,1': 5,
  '4,2': 3.5, # Same
  '4,3': 2,
  '4,4': 0,
  '4,5': 2,
  '5,1': 7,
  '5,2': 5,
  '5,3': 3.5, # Same
  '5,4': 2,
  '5,5': 0
}


#----------------------------------------------------------


MOVE_HASH_BASE = {
    1 : 0,
    2 : 0.5,
    3 : 1.8,
    4 : 3,
    5 : 5,
    6 : 7,
    7 : 8,
    8 : 8.9,
    9 : 9.7,
    10 : 10.5,
    11 : 11,
    12 : 11.4,
    13 : 11.8,
    14 : 12.2,
    15 : 12.5,
    16 : 12.8,
    17 : 13.1,
    18 : 13.4,
    19 : 13.7,
    20 : 14,
    21 : 14.3,
    22 : 14.6,
    23 : 14.9,
    24 : 15.2,
}

def makeMoveHash(fixed_cost):
    result = {}
    for k,v in MOVE_HASH_BASE.items():
        result[k] = v + fixed_cost
    return result

MOVE_HASH = makeMoveHash(4)


#----------------------------------------------------------


COLOR = {
  0: 'White',
  1: 'Black',
  2: 'White',
  3: 'Black',
  4: 'White',
  5: 'White',
  6: 'Black',
  7: 'White',
  8: 'Black',
  9: 'White',
  10: 'Black',
  11: 'White'
}


#----------------------------------------------------------


DESC_THUMB_STRETCH_VALS = {
  '1,2' : 1,
  '1,3' : 1,
  '1,4' : 0.9,
  '1,5' : 0.95
};


#----------------------------------------------------------


ASC_THUMB_STRETCH_VALS = {
  '2,1' : 0.95,
  '3,1' : 1,
  '4,1' : 0.95,
  '5,1' : 0.95
};


#----------------------------------------------------------


FINGER_STRETCH = {
  '1,1' : 0.8,
  '1,2' : 1.15,
  '1,3' : 1.4,
  '1,4' : 1.45,
  '1,5' : 1.6,
  '2,1' : 1.15,
  '2,2' : 0.6,
  '2,3' : 0.9,
  '2,4' : 1.15,
  '2,5' : 1.3,
  '3,1' : 1.4,
  '3,2' : 0.9,
  '3,3' : 0.6,
  '3,4' : 0.9,
  '3,5' : 1.15,
  '4,1' : 1.45,
  '4,2' : 1.15,
  '4,3' : 0.9,
  '4,4' : 0.7,
  '4,5' : 0.7,
  '5,1' : 1.6,
  '5,2' : 1.3,
  '5,3' : 1.15,
  '5,4' : 0.8,
  '5,5' : 0.6
}


#----------------------------------------------------------


def createCostDatabase():
    right_hand_cost_database = {}
    left_hand_cost_database = {}

    for finger1 in range(1, 6):
        for note1 in range(21, 109):    # in MIDI land, note 21 is actually the lowest
                                        # note on the piano, and 108 is the highest
            for finger2 in range(1, 6):
                for note2 in range(21, 109):
                    computeRightHandCost(note1, note2, finger1, finger2, right_hand_cost_database)
                    computeLeftHandCost(note1, note2, finger1, finger2, left_hand_cost_database)

    return right_hand_cost_database, left_hand_cost_database


#----------------------------------------------------------


def computeRightHandCost(n1, n2, f1, f2, cost_database):
    key = '%d,%d,%d,%d' % (n1, n2, f1, f2)
    note_distance = abs(n2 - n1)
    finger_distance = fingerDistance(f1, f2)

    # Handles cases where the note is ascending or descending and you're using the same
    # finger. It doesn't matter whether we send it to ascMoveFormula or descMoveFormula,
    # since in either case, finger_distance is zero.
    if (note_distance > 0) and (f2 - f1 == 0):
        cost_database[key] = ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)

    # Handles ascending notes and descending fingers, but f2 isn't thumb.
    # It means you're crossing over. Bad idea. Only plausible way to do this is picking
    # your hand up. Thus move formula
    elif (n2 - n1 >= 0) and (f2 - f1 < 0) and (f2 != 1):
        cost_database[key] = ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles descending notes with ascending fingers where f1 isn't thumb.
    # It means your crossing over. Same as above. Only plausible way is picking hand up,
    # so move formula.
    elif (n2 - n1 < 0) and (f2 - f1 > 0) and (f1 != 1):
        cost_database[key] = ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles ascending notes, where you start on a finger that isn't your thumb,
    # but you land on your thumb, thus bringing your thumb under.
    elif (n2 - n1 >= 0) and (f2 - f1 < 0) and (f2 == 1):
        cost_database[key] = ascThumbCost(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles descending notes, where you start on your thumb, but don't end with it.
    # Thus your crossing over your thumb.
    elif (n2 - n1 < 0) and (f1 == 1) and (f2 != 1):
        cost_database[key] = descThumbCost(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles ascending or same note, with ascending or same finger.
    # To be clear... only remaining options are ((n2 - n1 >= 0) and (f2 - f1 > 0)) or
    # ((n2 - n1 <= 0) and (f2 - f1 < 0))
    else:
        stretch = fingerStretch(f1, f2)
        x = abs(note_distance - finger_distance) / stretch
        if x > MOVE_CUTOFF:
            cost_database[key] = descMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)
        else:
            cost_database[key] = ascDescNoCrossCost(note_distance, finger_distance, x, n1, n2, f1, f2)


#----------------------------------------------------------


def computeLeftHandCost(n1, n2, f1, f2, cost_database):
    key = '%d,%d,%d,%d' % (n1, n2, f1, f2)
    note_distance = abs(n2 - n1)
    finger_distance = fingerDistance(f1, f2)

    # Handles cases where the note is ascending or descending and you're using the same
    # finger. It doesn't matter whether we send it to ascMoveFormula or descMoveFormula,
    # since in either case, finger_distance is zero.
    if (note_distance > 0) and (f2 - f1 == 0):
        cost_database[key] = ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)

    # Handles descending notes and descending fingers, but f2 isn't thumb.
    # It means you're crossing over. Bad idea. Only plausible way to do this is picking
    # your hand up. Thus move formula
    elif (n2 - n1 <= 0) and (f2 - f1 < 0) and (f2 != 1):
        cost_database[key] = ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles ascending notes with ascending fingers where f1 isn't thumb.
    # It means your crossing over. Same as above. Only plausible way is picking hand up,
    # so move formula.
    elif (n2 - n1 > 0) and (f2 - f1 > 0) and (f1 != 1):
        cost_database[key] = ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles descending notes, where you start on a finger that isn't your thumb,
    # but you land on your thumb, thus bringing your thumb under.
    elif (n2 - n1 <= 0) and (f2 - f1 < 0) and (f2 == 1):
        cost_database[key] = ascThumbCost(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles ascending notes, where you start on your thumb, but don't end with it.
    # Thus your crossing over your thumb.
    elif (n2 - n1 >= 0) and (f1 == 1) and (f2 != 1):
        cost_database[key] = descThumbCost(note_distance, finger_distance, n1, n2, f1, f2)

    # This handles ascending or same note, with descending fingers or it takes
    # descending notes with ascending fingers.
    # To be clear... only remaining options are ((n2 - n1 >= 0) and (f2 - f1 < 0)) or
    # ((n2 - n1 <= 0) and (f2 - f1 > 0))
    else:
        stretch = fingerStretch(f1, f2)
        x = abs(note_distance - finger_distance) / stretch
        if x > MOVE_CUTOFF:
            cost_database[key] = descMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)
        else:
            cost_database[key] = ascDescNoCrossCost(note_distance, finger_distance, x, n1, n2, f1, f2)


#----------------------------------------------------------
    

def fingerDistance(f1, f2):
    """Currently assumes your on Middle C. Could potentially take into account n1 as
    a way to know how to handle the irregularities. Such as E-F being 1 half step,
    but G-A being 2.
    """
    key = '%d,%d' % (f1, f2)
    return FINGER_DISTANCE[key]


#----------------------------------------------------------


def colorRules(n1, n2, f1, f2, finger_distance):
    # If you're moving up from white to black with pinky or thumb, that's much harder
    # than white-to-white would be. So we're adding some amount.
    if (COLOR[n1 % 12] == 'White') and (COLOR[n2 % 12] == 'Black'):
        if (f2 == 5) or (f2 == 1):
            return 4    # Using thumb or pinky on black is extra expensive

        if finger_distance == 0:
            return 4;   # Using same finger is extra expensive

    if (COLOR[n1 % 12] == 'Black') and (COLOR[n2 % 12] == 'White'):
        if (f1 == 5) or (f1 == 1):
            return 4    # Moving from thumb or pinky that's already on black is extra expensive

        if finger_distance == 0:
            return -1   # Moving black to white with same finger is a slide. That's easy and
                        # common. reduce slightly.

    return 0    # If none of the rules apply, then don't add or subtract anything


#----------------------------------------------------------


def ascThumbStretch(f1, f2):
    key = '%d,%d' % (f1, f2)
    return ASC_THUMB_STRETCH_VALS[key];


#----------------------------------------------------------


def descThumbStretch(f1, f2):
    key = '%d,%d' % (f1, f2)
    return DESC_THUMB_STRETCH_VALS[key];


#----------------------------------------------------------


def fingerStretch(f1, f2):
    key = '%d,%d' % (f1, f2)
    return FINGER_STRETCH[key]


#----------------------------------------------------------

def thumbCrossCostFunc(x):
    """Got this crazy function from regressing values I wanted at about 15 points
    along the graph."""
    return 0.0002185873295 * math.pow(x, 7) - 0.008611946279 * math.pow(x, 6) + \
           0.1323250066 * math.pow(x, 5) - 1.002729677 * math.pow(x, 4) + \
           3.884106308 * math.pow(x, 3) - 6.723075747 * math.pow(x, 2) + \
           1.581196785 * x + 7.711241722;


#----------------------------------------------------------


def ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2):
    """This is for situations where direction of notes and fingers are opposite,
    because either way, you want to add the distance between the fingers.
    """

    # The math.ceil part is so it really hits a value in our moveHash.
    # This could be fixed if I put more resolution into the moveHash
    total_distance = math.ceil(note_distance + finger_distance);

    # This adds a small amount for every additional halfstep over 24. Fairly
    # representative of what it should be. 
    if total_distance > 24:
        return MOVE_HASH[24] + (total_distance - 24) / 5;
    else:
        cost = MOVE_HASH[total_distance];
        cost += colorRules(n1, n2, f1, f2, finger_distance)
        return cost


#----------------------------------------------------------


def descMoveFormula(note_distance, finger_distance, n1, n2, f1, f2):
    """This is for situations where direction of notes and fingers is the
    same. You want to subtract finger distance in that case.
    """

    # The math.ceil part is so it really hits a value in our moveHash.
    # This could be fixed if I put more resolution into the moveHash
    total_distance = math.ceil(note_distance - finger_distance);

    # This adds a small amount for every additional halfstep over 24. Fairly
    # representative of what it should be. 
    if total_distance > 24:
        return MOVE_HASH[24] + (total_distance - 24) / 5;
    else:
        cost = MOVE_HASH[total_distance];
        cost += colorRules(n1, n2, f1, f2, finger_distance)
        return cost


#----------------------------------------------------------


def ascThumbCost(note_distance, finger_distance, n1, n2, f1, f2):
    stretch = ascThumbStretch(f1, f2)
    x = (note_distance + finger_distance) / stretch

    # If it's over 10, again use the move formula
    if x > 10:
        return ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)
    else:
        cost = thumbCrossCostFunc(x)
        if (COLOR[n1 % 12] == 'White') and (COLOR[n2 % 12] == 'Black'):
            cost += 8
        return cost;


#----------------------------------------------------------


def descThumbCost(note_distance, finger_distance, n1, n2, f1, f2):
    stretch = descThumbStretch(f1, f2)
    x = (note_distance + finger_distance) / stretch

    # If it's over 10, again use the move formula
    if x > 10:
        return ascMoveFormula(note_distance, finger_distance, n1, n2, f1, f2)
    else:
        cost = thumbCrossCostFunc(x)
        if (COLOR[n1 % 12] == 'Black') and (COLOR[n2 % 12] == 'White'):
            cost += 8
        return cost


#----------------------------------------------------------


def ascDescNoCrossCost(note_distance, finger_distance, x, n1, n2, f1, f2):
    def costFunc(x):
        return -0.0000006589793725 * math.pow(x, 10) - \
               0.000002336381414 * math.pow(x, 9) + \
               0.00009925769823 * math.pow(x, 8) + \
               0.0001763353131 * math.pow(x, 7) - \
               0.004660305277 * math.pow(x, 6) - \
               0.004290746384 * math.pow(x, 5) + \
               0.06855725903 * math.pow(x, 4) + \
               0.03719817227 * math.pow(x, 3) + \
               0.4554696705 * math.pow(x, 2) - \
               0.08305450359 * x + \
               0.3020594956

    # If it's above 6.8, but below moveCutoff, then we use an additional formula
    # because the current one has an odd shape to it where it goes sharply negative
    # after 6.8  I know this appears janky, but after messing with other potential
    # regression formulas, I can't get any single one to match both the overall shape,
    # and certainly specific Y values I want. So this seems like best option.
    if (x > 6.8) and (x <= MOVE_CUTOFF):
        return costFunc(6.8) + (x - 6.8) * 3
    else:
      cost = costFunc(x)
      cost += colorRules(n1, n2, f1, f2, finger_distance)
      return cost
