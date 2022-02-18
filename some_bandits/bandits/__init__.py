from some_bandits.bandits.egreedy import egreedy
from some_bandits.bandits.EXP3 import EXP3
from some_bandits.bandits.EXP4 import EXP4
from some_bandits.bandits.UCB import UCB
from some_bandits.bandits.UCBImproved import UCBImproved
from some_bandits.bandits.UCBNorm import UCBNorm

def init_bandit(name, formula=None):
    chosen_bandit = {
        "egreedy": egreedy,
        "UCB": UCB,
        "EXP3": EXP3,
        "UCBImproved": UCBImproved,
        "UCBNorm": UCBNorm
    }.get(name, None)

    if(chosen_bandit):
        return chosen_bandit(formula)
    else:
        raise RuntimeError("Specified Bandit did not exist")
