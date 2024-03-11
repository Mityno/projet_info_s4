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
        comb for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }

    solution = random.choice(tuple(comb_possibles))


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution

    # la combinaison voulue maximise le nombre de possibilités restantes
    # donc elle minimise le nombre de possibilités supprimées
    # on utilise cette propriété pour effectuer une selection efficace
    # sur la totalité des possibilités restantes

    best_sol = None
    # le pire cas est d'avoir supprimé toutes les combinaisons
    best_combs_supprimees = float('inf')

    comb_a_tester = comb_possibles.copy()
    while comb_a_tester:
        temp_sol = next(iter(comb_a_tester))
        comb_a_tester.discard(temp_sol)

        # on va évaluer si comb est une meilleure solution que best_sol
        temp_eval = common.evaluation(temp_sol, combinaison)
        temp_combs_supprimees = 0

        for other_comb in comb_possibles:
            if temp_eval != common.evaluation(other_comb, combinaison):
                temp_combs_supprimees += 1
            else:
                comb_a_tester.discard(other_comb)

        # si on a moins de combinaisons à supprimer, c'est qu'on a trouvé
        # une "meilleure" solution
        if temp_combs_supprimees < best_combs_supprimees:
            best_sol = temp_sol
            best_combs_supprimees = temp_combs_supprimees

    solution = best_sol

    eval_retour = common.evaluation(solution, combinaison)
    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    return eval_retour
