#!/usr/bin/env python3

import common
import itertools


def init():
    """
    Initialisation de la liste des combinaisons possibles rangées sans ordre
    """
    global comb_possibles, solution

    comb_possibles = {
        ''.join(comb)
        for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }


def codemaker(combinaison):
    """
    Cette version du codemaker change et choisit la solution qui maximise la
    longueur de `comb_possibles` tout en respectant les évaluations
    précédentes.
    Elle renvoie l'évaluation de la combinaison une fois le choix de la
    solution fait.
    """
    global solution
    solution = common.evil_codemaker(frozenset(comb_possibles), combinaison)
    eval_retour = common.evaluation(solution, combinaison)

    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    return eval_retour
