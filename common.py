#!/usr/bin/env python3
import itertools

LENGTH = 4
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
# Notez que vos programmes doivent continuer à fonctionner si on change les valeurs par défaut ci-dessus

def evaluation(essai, reference):
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
        
    return (compteur_bien_placees, compteur_mal_placees)


def donner_possibles(comb_test, eval_donnee):
    return {comb for comb in itertools.product(COLORS, repeat=LENGTH)
            if evaluation(comb, comb_test) == eval_donnee}


def maj_possibles(comb_possibles, comb_test, eval_donnee):
    comb_a_supprimer = set()
    for comb in comb_possibles:
        if eval_donnee != evaluation(comb_test, comb):
            comb_a_supprimer.add(comb)
    
    comb_possibles.difference_update(comb_a_supprimer)


# def remplissage_mal_placees(nombre_mal_placees, lettres_restantes):
#     return set(itertools.permutations(lettres_restantes, r=nombre_mal_placees))


# def fusion_remplissage_aleatoires(remplissage, lettres_possibles, longueur):
#     if longueur == 0:
#         return set()

#     remplissage_final = set()
#     for comb in remplissage:
#         for lettre in lettres_possibles:
#             nouveaux_remplissages = []
#             for i in range(len(comb) + 1):
#                 comb.insert(i, lettre)
#                 nouveaux_remplissages.append(comb[:])
#                 comb.pop(i)

#             if longueur - 1 == 0:  # on a atteint le cas de base
#                 remplissage_final.update(map(tuple, nouveaux_remplissages))
#             else:
#                 remplissage_final.update(fusion_remplissage_aleatoires(
#                     nouveaux_remplissages, lettres_possibles, longueur-1
#                 ))
#     return remplissage_final

# # a reprendre completer
# def remplissage_bien_placees(combinaison_test, evaluation_donnee):
    
    
#     remplissages = remplissage_mal_placees(nombre_mal_placees, lettres_restantes)
    
#     for comb in remplissage:
#         for lettre in comb:
#             lettres_restantes.remove(lettre)
#         lettres_bannies = set(lettres_restantes)
#         remplissage_final(nombre_elements, lettres_bannies)
        
#         lettres_restantes.extend(comb)