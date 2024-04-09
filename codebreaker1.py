import random
import common
import itertools


def init():
    """
    Initialisation de la liste des combinaisons possibles rangées aléatoirement
    """

    global liste_possible
    liste_possible = [
        ''.join(comb)
        for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    ]
    # les combinaisons sont rangées aléatoirement
    # on n'a plus besoin de les tirer au hasard
    random.shuffle(liste_possible)
    return


def codebreaker(evaluation_p):
    """
    L'argument evaluation_p est l'évaluation qu'on reçoit pour la dernière
    combinaison qu'on a proposée (et vaut None si c'est le premier coup de la
    partie). Cette version triviale n'utilise pas cette information, puisqu'
    elle joue au hasard, mais ne propose pas deux fois la même valeur.
    """

    return ''.join(liste_possible.pop())
