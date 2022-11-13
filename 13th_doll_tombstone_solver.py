'''
Solver for the tombstone puzzle in 13th Doll in the dining room (also 7th Guest)

Useful discovery: The tombstones can be represented as a 2D mask. The mask toggles every tombstone.
The position of the tombstone doesn't need to be recorded directly, that's captured in its mask
(it has a 1 at its own coordinate).

From this we come to more conclusions.
- A tombstone will only need to be pressed once. Pressing it twice (with any number of ops in
    between) is a no-op, because we're applying the toggle mask twice.
- Order doesn't matter.

The easiest solution is to try every combination. Since order doesn't matter, we don't need BFS/DFS
or any performance optimization. For example, 12 choose 6 = 924, so we won't need to test more than
10k combinations (sum of 12 choose n for n in 1..12).
Itertools.combination solves this easily.
'''

import math
import itertools


def get_tombstones_to_click(initial_state, tombstones):
    tombstones_to_click = []

    # Try every possible combination
    for i in range(1, len(tombstones)+1):
        for combination in itertools.combinations(tombstones, i):
            if(check_solution(initial_state, combination)):
                tombstones_to_click.append(combination)

    return tombstones_to_click


def check_solution(initial_state, tombstones):
    '''
    Given an initial state and a set of tombstones, checks whether those tombstones result in
    all-1s

    Hack: To avoid losing leading zeros on the state, we preface the state with a 1 before int(2)
    '''
    initial_state = '1' + initial_state
    state = int(initial_state.replace(',', ''), 2)
    tombstones = [int(t.replace(',', ''), 2) for t in tombstones]

    for tombstone in tombstones:
        # bitwise xor the two and save the result
        state = state ^ tombstone

    # print(format(initial_state, b))

    # If n is all 1s, n+1 is a power of 2,
    return math.log(state+1, 2).is_integer()



if __name__ == '__main__':
    # Test checker
    assert check_solution('100,100,100,100', ['010,010,010,010', '001,001,001,001'])
    assert not check_solution('000,100,100,100', ['010,010,010,010', '001,001,001,001'])

    # Notation is row-by-row
    INITIAL_STATE = '101,001,100,000'
    TOMBSTONES = [
        '100,100,110,110',
        '010,101,010,010',
        '111,111,111,111',
        '000,100,110,110',
        '010,010,010,010',
        '000,001,011,111',
        '000,100,110,111',
        '010,111,111,111',
        '000,000,111,111',
        '000,010,111,111',
        '000,000,000,010',
        '000,001,111,111',
    ]

    print(get_tombstones_to_click(INITIAL_STATE, TOMBSTONES))
