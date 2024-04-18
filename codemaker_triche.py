#!/usr/bin/env python3

import random
import common
import itertools


def init():
    """
    Initialisation de la liste des combinaisons possibles rangées sans ordre
    On garde aussi en mémoire l'entièreté des combinaisons possibles pour les
    paramètres du jeu.
    Le codemaker choisit une solution aléatoirement parmi les combinaisons
    possibles
    """
    global solution, comb_possibles, all_comb

    comb_possibles = {
        comb for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }

    all_comb = comb_possibles.copy()

    solution = random.choice(tuple(comb_possibles))


def codemaker(combinaison):
    """

    """
    global solution
    # le codebreaker a donné la combinaison "bidon" qui indique qu'il n'y pas
    # plus de combinaison possibles pour lui, on arrête donc la partie
    if combinaison is None:
        return (common.LENGTH, 0)  # permet à la partie de se terminer

    # on détermine l'évaluation du codebreaker par rapport à la solution
    # actuelle
    eval_retour = common.evaluation(solution, combinaison)

    # on met à jour les combinaisons possibles et on s'assure de changer la
    # solution par une solution qui n'est **pas** possible (on triche)
    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    if comb_possibles:
        solution = random.choice(tuple(all_comb - comb_possibles))

    return eval_retour
