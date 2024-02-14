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
    print(solution)



def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution
    
    min_combs_surplus = float("inf")
    new_sol = None
    for test_sol in comb_possibles:
        compteur_combs = 0
        test_eval = common.evaluation(combinaison, test_sol)

        for comb in comb_possibles:
            if compteur_combs >= min_combs_surplus:
                break
#  la condition ne marche pas
            # if test_eval != common.evaluation(comb, test_sol):
            #     compteur_combs += 1

        if compteur_combs < min_combs_surplus:
            temp_comb_possibles = comb_possibles.copy()
            common.maj_possibles(temp_comb_possibles, combinaison, test_eval)
            print(len(temp_comb_possibles), compteur_combs)
            min_combs_surplus = compteur_combs
            new_sol = test_sol
    solution = new_sol
    eval_retour = common.evaluation(solution, combinaison)    
    common.maj_possibles(comb_possibles, combinaison, eval_retour)
    print('codemaker', solution, len(comb_possibles))
    return eval_retour
