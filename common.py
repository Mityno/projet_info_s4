#!/usr/bin/env python3

import itertools
import random
import functools

LENGTH = 4  # original : 4
# original : COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
# Notez que vos programmes doivent continuer à fonctionner si on change les valeurs par défaut ci-dessus


@functools.cache
def evaluation(essai, reference):
    # ensure the memoisation is effective for symetric calls
    if reference < essai:
        return evaluation(reference, essai)

    lettres_reference = set(reference)
    lettres_bien_placees = {lettre : 0 for lettre in lettres_reference}
    
    for let_essai, let_ref in zip(essai, reference):
        if let_essai == let_ref:
            lettres_bien_placees[let_ref] += 1
    
    compteur_mal_placees = 0
    for lettre in lettres_reference:
        compteur_ref = reference.count(lettre)
        compteur_essai = essai.count(lettre)
        bien_placees = lettres_bien_placees[lettre]
        mal_place = min(compteur_ref - bien_placees, compteur_essai - bien_placees)
        compteur_mal_placees += mal_place

    compteur_bien_placees = sum(lettres_bien_placees.values())

    return compteur_bien_placees, compteur_mal_placees


def donner_possibles(comb_test, eval_donnee):
    return {comb for comb in itertools.product(COLORS, repeat=LENGTH)
            if evaluation(comb, comb_test) == eval_donnee}


def maj_possibles(comb_possibles, comb_test, eval_donnee):
    comb_a_supprimer = set()
    for comb in comb_possibles:
        if eval_donnee != evaluation(comb_test, comb):
            comb_a_supprimer.add(comb)
    
    comb_possibles.difference_update(comb_a_supprimer)


@functools.cache
def evil_codemaker(comb_possibles, comb_test):
    # la combinaison voulue maximise le nombre de possibilités restantes
    # donc elle minimise le nombre de possibilités supprimées
    # on utilise cette propriété pour effectuer une selection efficace
    # sur la totalité des possibilités restantes

    best_sol = None
    # le pire cas est d'avoir supprimé toutes les combinaisons
    best_combs_supprimees = float('inf')

    comb_a_tester = set(comb_possibles)
    while comb_a_tester:
        temp_sol = next(iter(comb_a_tester))
        comb_a_tester.discard(temp_sol)

        # on va évaluer si comb est une meilleure solution que best_sol
        temp_eval = evaluation(temp_sol, comb_test)
        temp_combs_supprimees = 0

        for other_comb in comb_possibles:
            if temp_eval != evaluation(other_comb, comb_test):
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


if __name__ == '__main__':
    combs_possibles = list(itertools.product(COLORS, repeat=LENGTH))
    solution = random.choice(combs_possibles)
    longueurs = []
    for comb in combs_possibles:
        temp_eval = evaluation(comb, solution)
        longueurs.append(len(donner_possibles(comb, temp_eval)))

    longueurs.sort()
    print(longueurs[-10:])
