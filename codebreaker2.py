import random
import common
import itertools


def init():
    """
    Initialisation de la liste des combinaisons possibles rangées sans ordre
    """

    global comb_possibles
    comb_possibles = {
        ''.join(comb)
        for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }

    return


def codebreaker(evaluation_p):
    """
    L'argument evaluation_p est l'évaluation qu'on reçoit pour la dernière
    combinaison qu'on a proposée (et vaut None si c'est le premier coup de la
    partie). Elle sert ici à mettre à jour les combinaisons encore possibles.
    """
    global comb_test

    # on met à jour les combinaisons possibles selon l'évaluation donnée
    # par le codemaker
    if evaluation_p is not None:
        common.maj_possibles(comb_possibles, comb_test, evaluation_p)

    # pourrait être remplacé par `comb_possibles.pop()` pour un léger gain en
    # performance et en espace mémoire
    comb_test = random.choice(tuple(comb_possibles))
    return comb_test
