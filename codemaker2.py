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
    print('codemaker', solution, len(comb_possibles))



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

    for temp_sol in comb_possibles:
        # on va évaluer si comb est une meilleure solution que best_sol
        temp_eval = common.evaluation(temp_sol, combinaison)
        temp_combs_supprimees = 0

        for other_comb in comb_possibles:
            # on a supprimé plus de possibilité qu'avant, la solution est donc moins bonne
            if temp_combs_supprimees >= best_combs_supprimees:
                break

            if temp_eval != common.evaluation(other_comb, combinaison):
                temp_combs_supprimees += 1

        # si on a moins de combinaisons à supprimer, c'est qu'on a trouvé
        # une "meilleure" solution
        if temp_combs_supprimees < best_combs_supprimees:
            best_sol = temp_sol
            best_combs_supprimees = temp_combs_supprimees

    solution = best_sol

    eval_retour = common.evaluation(solution, combinaison)    
    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    print('codemaker', combinaison, solution, len(comb_possibles))
    return eval_retour
