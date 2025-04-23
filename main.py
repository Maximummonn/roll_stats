"""Script to compute probability of failure for crafting checks"""

import numpy as np


def roll(*, die: int = 20, number: int = 1) -> np.ndarray:
    """Vectorized dice roll.

    Args:
        die (int, optional): 'd' number of die to roll. Defaults to 20.
        number (int, optional): number of times to roll. Defaults to 1.

    Returns:
        np.ndarray: array of roll results
    """
    return np.random.randint(1, die + 1, size=number)


def make_checks(*, dc: int, modifier: int = 0, number: int = 1) -> np.ndarray:
    """make a number of checks against a DC. meets it, beats it

    Args:
        dc (int): difficulty class of check
        modifier (int, optional): number to add to check. Defaults to 0.
        number (int, optional): number of checks to make (for vectorizing). Defaults to 1.

    Returns:
        np.ndarray: array of True (success) and False (fail)
    """
    return roll(die=20, number=number) + modifier >= dc


def craft(
    *,
    dc: int,
    modifier: int = 0,
    successes_required: int,
    n_successes: int = 0,
    n_consec_fails: int = 0,
) -> bool:
    """simulates a series of crafting checks resulting in a success (True) or failure (False)

    Args:
        dc (int): difficulty class of crafting check
        successes_required (int): number of successes needed to craft
        modifier (int, optional): modifier to be added to rolls. Defaults to 0.
        n_successes (int, optional): initial number of successes (used for recursion). Defaults to 0.
        n_consec_fails (int, optional): initial number of consec fails (used for recursion). Defaults to 0.

    Returns:
        bool: success (True) for failure (False)
    """
    ROLL_CHUNK = 100  # used to vectorize the random int generation
    n_successes = n_successes
    n_consec_fails = n_consec_fails
    for result in make_checks(dc=dc, modifier=modifier, number=ROLL_CHUNK):
        if result:
            n_successes += 1
            n_consec_fails = 0  # reset fail counter
            if n_successes >= successes_required:
                return True
        else:
            n_consec_fails += 1
            if n_consec_fails >= 3:
                return False
    # recursive call to "craft()" if you run out of numbers in a set of roll chunks (should only happen at high DC)
    return craft(
        dc=dc,
        modifier=modifier,
        successes_required=successes_required,
        n_successes=n_successes,
        n_consec_fails=n_consec_fails,
    )


if __name__ == "__main__":
    dc = 18
    modifier = 9
    successes_required = 8
    n_repeats = 10000

    repeated_craft = [
        craft(dc=dc, modifier=modifier, successes_required=successes_required)
        for _ in range(n_repeats)
    ]
    print(f"percent failure:{(1-sum(repeated_craft)/len(repeated_craft))*100:.0f}")
