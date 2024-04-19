#!/usr/bin/env python3

import itertools
import random
import functools

LENGTH = 4  # original : 4
# original : COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']


@functools.cache
def evaluation(essai, reference):
    # on s'assure qu'on utilise bien la mémoïsation pour des appels où les
    # arguments seraient inversés (la fonction est "symétrique")
    if reference < essai:
        return evaluation(reference, essai)

    # on compte les bons placements de chaque lettre, on crée pour cela le set
    # des lettres présentes dans la solution référence
    lettres_reference = set(reference)
    lettres_bien_placees = {lettre: 0 for lettre in lettres_reference}

    # on va d'abord compter les lettres biens placées (opération aisée)
    for let_essai, let_ref in zip(essai, reference):
        if let_essai == let_ref:  # la lettre est bien placée
            lettres_bien_placees[let_ref] += 1

    # on compte maintenant les lettres mal placées, on va utiliser le
    # nombre de lettre bien placée pour chaque lettre présente dans la
    # référence
    compteur_mal_placees = 0
    for lettre in lettres_reference:
        # nombre de fois où la lettre est présente dans la référence
        compteur_ref = reference.count(lettre)
        # nombre de fois où la lettre est présente dans l'essai
        compteur_essai = essai.count(lettre)
        bien_placees = lettres_bien_placees[lettre]

        # le nombre de mauvais placement de la lettre correspond au minimum de
        # ses apparition dans les deux combinaisons (càd, combien de fois on
        # doit réellement prendre la lettre en compte) auquel on soustrait le
        # nombre de bon placement de la lettre
        mal_place = min(compteur_ref, compteur_essai) - bien_placees

        compteur_mal_placees += mal_place

    compteur_bien_placees = sum(lettres_bien_placees.values())

    return compteur_bien_placees, compteur_mal_placees


def donner_possibles(comb_test, eval_donnee):
    # les combinaisons possibles pour une évaluation sont celles qui ont
    # cette évaluation par rapport à la combinaison testée
    return {
        comb
        for comb in map(''.join, itertools.product(COLORS, repeat=LENGTH))
        if evaluation(comb, comb_test) == eval_donnee
    }


def maj_possibles(comb_possibles, comb_test, eval_donnee):
    # on supprime les combinaisons qui ne respecte pas l'évaluation par rapport
    # à la combinaison de test
    for comb in frozenset(comb_possibles):
        if eval_donnee != evaluation(comb_test, comb):
            comb_possibles.discard(comb)


@functools.cache
def evil_codemaker(comb_possibles, comb_test):
    # la combinaison voulue maximise le nombre de possibilités restantes
    # donc elle minimise le nombre de possibilités supprimées
    # on utilise cette propriété pour effectuer une selection efficace
    # sur la totalité des possibilités restantes avec du backtracking

    best_sol = None
    #best_eval = (0,0)
    # le pire cas est d'avoir supprimé toutes les combinaisons
    best_combs_supprimees = float('inf')

    # on va essayer chaque combinaison possible pour trouver la meilleure
    # (celle qui maximise le nombre de possibilités restantes)
    comb_a_tester = set(comb_possibles)
    while comb_a_tester:
        # on choisit une combinaison à tester, n'importe laquelle
        temp_sol = comb_a_tester.pop()

        # on va évaluer si temp_sol est une meilleure solution que best_sol
        temp_eval = evaluation(temp_sol, comb_test)
        temp_combs_supprimees = 0

        for other_comb in comb_possibles:
            # on supprime les combinaisons qui ne vérifie pas l'évaluation
            # par rapport à comb_test
            if temp_eval != evaluation(other_comb, comb_test):
                temp_combs_supprimees += 1
            else:
                # si la combinaison a la même évaluation que `temp_sol`
                # alors elles jouent le même rôle en temps que solution
                # possibles, donc il ne sert à rien de tester les deux
                # séparément
                # cela réduit considérablement la quantité de "solution"
                # à essayer
                comb_a_tester.discard(other_comb)

        # si on a moins de combinaisons à supprimer, c'est qu'on a trouvé une
        # "meilleure" solution (elle donne moins d'informations au codebreaker)
        if temp_combs_supprimees < best_combs_supprimees:
            best_sol = temp_sol
            best_combs_supprimees = temp_combs_supprimees

    
    # on a choisi une solution non optimale car égale à celle que le codebreaker a essayé alors qu'il en existe d'autres
    if best_sol == comb_test and len(comb_possibles) > 1:
        # on choisit n'importe quelle autre solution
        best_sol = set(comb_possibles - {comb_test}).pop()
    
    solution = best_sol

    return solution


if __name__ == '__main__':

    # ce code (lent à lancer) permet de voir que des combinaisons donnent plus
    # d'information pour une combinaison que d'autres (en réduisant plus la
    # taille) de comb_possibles
    combs_possibles = list(
        map(''.join, itertools.product(COLORS, repeat=LENGTH))
    )
    solution = random.choice(combs_possibles)
    longueurs = []
    for comb in combs_possibles:
        temp_eval = evaluation(comb, solution)
        longueurs.append(len(donner_possibles(comb, temp_eval)))

    longueurs.sort()
    print(longueurs[-10:])
