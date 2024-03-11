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
    global solution, comb_possibles, all_comb

    comb_possibles = {
        comb for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }

    all_comb = comb_possibles.copy()

    solution = random.choice(tuple(comb_possibles))


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution
    if combinaison is None:
        return (4, 0)  # to allow the simulation to end

    eval_retour = common.evaluation(solution, combinaison)
    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    if comb_possibles:
        solution = random.choice(tuple(all_comb - comb_possibles))
    return eval_retour
