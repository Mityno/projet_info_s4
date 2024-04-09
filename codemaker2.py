#!/usr/bin/env python3

import sys
import common
import itertools

def init():
    """
    Cette fonction, appellée à chaque début de partie, initialise un certain nombre de
    variables utilisées par le codemaker
    """
    global comb_possibles, solution

    comb_possibles = {
        ''.join(comb) for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution
    solution = common.evil_codemaker(frozenset(comb_possibles), combinaison)
    eval_retour = common.evaluation(solution, combinaison)

    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    return eval_retour
