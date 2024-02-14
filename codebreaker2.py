import random
import common  # N'utilisez pas la syntaxe "form random import XXX"
import itertools


def init():
    """
    Initialisation de la liste des combinaisons possibles rangées aléatoirement
    """
    
    global comb_possibles
    comb_possibles = {
        ''.join(comb) for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }
    
    return


def codebreaker(evaluation_p):
    """
    L'argument evaluation_p est l'évaluation qu'on reçoit pour la dernière
    combinaison qu'on a proposée (et vaut None si c'est le premier coup de la
    partie). Cette version triviale n'utilise pas cette information, puisqu'
    elle joue au hasard, mais ne propose pas deux fois la même valeur.
    """
    global comb_test

    if evaluation_p is not None:
        common.maj_possibles(comb_possibles, comb_test, evaluation_p)
 
    comb_test = random.choice(tuple(comb_possibles))
    print('codebreaker', comb_test, len(comb_possibles))
    return comb_test
