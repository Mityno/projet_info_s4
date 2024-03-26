#!/usr/bin/env python3

import sys
import random
import common  # N'utilisez pas la syntaxe "from common import XXX"
import itertools

# explication a demander au prof

def init():
    """
    Cette fonction, appellée à chaque début de partie, initialise un certain nombre de
    variables utilisées par le codemaker
    """
    global comb_possibles, solution

    comb_possibles = {
        ''.join(comb) for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }

    solution = random.choice(tuple(comb_possibles))


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution

    solution = common.evil_codemaker(tuple(comb_possibles), combinaison)

    eval_retour = common.evaluation(solution, combinaison)
    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    return eval_retour
