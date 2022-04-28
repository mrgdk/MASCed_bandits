from some_bandits.bandits.egreedy import egreedy
from some_bandits.bandits.EXP3 import EXP3
from some_bandits.bandits.EXP4 import EXP4
from some_bandits.bandits.UCB import UCB
from some_bandits.bandits.UCBImproved import UCBImproved
from some_bandits.bandits.UCBNorm import UCBNorm
from some_bandits.bandits.SWUCB import SWUCB
from some_bandits.bandits.EwS import EwS
from some_bandits.bandits.EXP3S import EXP3S
from some_bandits.bandits.DUCB import DUCB
from some_bandits.bandits.explore_commit import explore_commit


def init_bandit(name, formula=""):
    chosen_bandit = {
        "egreedy": egreedy,
        "UCB": UCB,
        "EXP3": EXP3,
        "UCBImproved": UCBImproved,
        "UCBNorm": UCBNorm,
        "SWUCB": SWUCB,
        "EwS": EwS,
        "EXP3S": EXP3S,
        "EXP4": EXP4,
        "DUCB": DUCB,
        "explore_commit": explore_commit

    }.get(name, None)

    if(chosen_bandit):
        return chosen_bandit(formula)
    else:
        raise RuntimeError("Specified Bandit " + str(chosen_bandit) + " did not exist")
