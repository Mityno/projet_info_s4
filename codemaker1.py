#!/usr/bin/env python3

import random
import common


def init():
    """
    Initialisation d'une solution choisie aléatoirement parmi les combinaisons
    possibles
    """
    global solution
    solution = ''.join(random.choices(common.COLORS, k=common.LENGTH))


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument) en renvoyant l'évaluation correcte de sa combinaison
    """
    global solution
    return common.evaluation(solution, combinaison)
