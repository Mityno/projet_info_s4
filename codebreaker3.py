import random
import common
import itertools


def init():
    """
    Initialisation de la liste des combinaisons possibles rangées aléatoirement
    """

    global comb_possibles, all_combs
    all_combs = {
        ''.join(comb) for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }
    comb_possibles = all_combs.copy()

    return


def codebreaker(evaluation_p):
    """
    L'argument evaluation_p est l'évaluation qu'on reçoit pour la dernière
    combinaison qu'on a proposée (et vaut None si c'est le premier coup de la
    partie).
    """
    global comb_test

    if evaluation_p is not None:
        print(comb_test, evaluation_p)
        common.maj_possibles(comb_possibles, comb_test, evaluation_p)

    if len(comb_possibles) == 1:
        return comb_possibles.pop()

    best_length = float('inf')
    best_comb = None
    # on cherche la combinaison qui minimise la longueur de `comb_possible`
    for comb in all_combs:
        curr_comb_possible = comb_possibles.copy()

        # on simule le comportement de codemaker2 pour trouver une solution
        solution = simu_codemaker_evil(comb_possibles, comb)
        eval_simu = common.evaluation(comb, solution)

        # on met une copie de `comp_possible` à jour avec la solution trouvée
        common.maj_possibles(curr_comb_possible, comb, eval_simu)

        # on fait une sélection de `comb` selon le minimum de la longueur
        # de la copie de `comb_possible` après simulation du codemaker2
        if len(curr_comb_possible) < best_length:
            best_length = len(curr_comb_possible)
            best_comb = comb

    comb_test = best_comb
    print(comb_test, comb_test in comb_possibles)
    return comb_test


def simu_codemaker_evil(comb_possibles, comb_test):

    best_sol = None
    # le pire cas est d'avoir supprimé toutes les combinaisons
    best_combs_supprimees = float('inf')

    comb_a_tester = comb_possibles.copy()
    while comb_a_tester:
        temp_sol = next(iter(comb_a_tester))
        comb_a_tester.discard(temp_sol)

        # on va évaluer si comb est une meilleure solution que best_sol
        temp_eval = common.evaluation(temp_sol, comb_test)
        temp_combs_supprimees = 0

        for other_comb in comb_possibles:
            if temp_eval != common.evaluation(other_comb, comb_test):
                temp_combs_supprimees += 1
            else:
                comb_a_tester.discard(other_comb)

        # si on a moins de combinaisons à supprimer, c'est qu'on a trouvé une
        # "meilleure" solution (elle donne moins d'informations au codebreaker)
        if temp_combs_supprimees < best_combs_supprimees:
            best_sol = temp_sol
            best_combs_supprimees = temp_combs_supprimees

    solution = best_sol

    return solution
