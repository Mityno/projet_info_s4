#!/usr/bin/env python3

import common
import numpy as np
import time


def play(codemaker, codebreaker, quiet=False):
    """
    Fonction principale de ce programme :
    Fait jouer ensemble le codebreaker et le codemaker donnés en arguments
    Renvoie le nombre de coups joués pour trouver la solution

    Attention, il ne *doit* pas être nécessaire de modifier cette fonction
    pour faire fonctionner vos codemaker et codebreaker (dans le cas contraire,
    ceux-ci ne seront pas considérés comme valables)
    """
    n_essais = 0
    codebreaker.init()
    codemaker.init()
    ev = None
    if not quiet:
        print('Combinaisons de taille {}, couleurs disponibles {}'.format(common.LENGTH, common.COLORS))
    while True:
        combinaison = codebreaker.codebreaker(ev)
        ev = codemaker.codemaker(combinaison)
        n_essais += 1
        if ev[0] >= common.LENGTH:
            return n_essais


def play_log(codemaker, codebreaker, nom_fichier):
    """
    Fonction principale de ce programme :
    Fait jouer ensemble le codebreaker et le codemaker donnés en arguments
    Renvoie le nombre de coups joués pour trouver la solution

    Attention, il ne *doit* pas être nécessaire de modifier cette fonction
    pour faire fonctionner vos codemaker et codebreaker (dans le cas contraire,
    ceux-ci ne seront pas considérés comme valables)
    """
    bef = time.perf_counter()
    n_essais = 0
    codebreaker.init()
    codemaker.init()
    ev = None
    liste_comb = []
    liste_eval = []
    while True:
        combinaison = codebreaker.codebreaker(ev)
        ev = codemaker.codemaker(combinaison)
        liste_comb.append(combinaison)
        liste_eval.append(ev)
        n_essais += 1
        if ev[0] >= common.LENGTH:
            break

    aft = time.perf_counter()
    print(aft - bef)
    with open(nom_fichier, mode='w') as fichier:
        for comb, ev in zip(liste_comb, liste_eval):
            fichier.write(f'{comb}\n{ev[0]},{ev[1]}\n')

    return n_essais


if __name__ == '__main__':
    # Les lignes suivantes sont à modifier / supprimer selon ce qu'on veut faire, quelques exemples :

    # Faire jouer ensemble codemaker0.py et codebreaker0.py pour 5 parties :
    # import codebreaker0
    # import codemaker0
    # for i in range(5):
    #     play(codemaker0, codebreaker0)

    #  Faire jouer un humain contre codemaker0.py :
    #import codemaker0
    #import human_codebreaker
    #play(codemaker0, human_codebreaker)

    # Et plus tard, vous pourrez faire jouer vos nouvelles version du codebreaker et codemaker :
    #import codebreaker2
    #import codemaker2
    #play(codemaker2, codebreaker2)

    # Ou encore :
    #import codebreaker1
    #import human_codemaker
    #play(human_codemaker, codebreaker1)

    # import codemaker_triche as codemaker
    # import codebreaker_triche as codebreaker

    # play_log(codemaker, codebreaker, 'log_triche.txt')

    # import codemaker1 as codemaker1
    # import codemaker2 as codemaker2
    # import codebreaker2 as codebreaker
    # import matplotlib.pyplot as plt
    # import time

    # n = 2_000

    # bef = time.perf_counter()
    # nb_essais_c2 = [play(codemaker2, codebreaker, quiet=True) for i in range(n)]
    # mid = time.perf_counter()
    # print(f'codemaker 2 : {mid - bef:.2f}', flush=True)
    # nb_essais_c1 = [play(codemaker1, codebreaker, quiet=True) for i in range(n)]
    # aft = time.perf_counter()
    # print(f'codemaker 1 : {aft - mid:.2f}', flush=True)
    # # print(aft - bef)

    # set_essais = set(nb_essais_c1) | set(nb_essais_c2)
    # print(set_essais)
    # bins = np.array(list(set_essais)) - 0.5
    # print(bins)

    # plt.hist(
    #     (nb_essais_c1, nb_essais_c2),
    #     bins=bins, density=True,
    #     label=('Codemaker 1', 'Codemaker 2'), histtype='bar')
    # # plt.plot(list(range(len(nb_essais))), nb_essais)
    # plt.xlabel('Nombres d\'essais du codebreaker')
    # plt.legend()
    # plt.tight_layout()
    # # plt.show()
    # plt.savefig('Comparaison des codemaker 1 et 2.pdf', dpi=300, format='pdf')
    # print('Finished')

    # import codemaker1 as codemaker
    # import codebreaker1 as codebreaker
    # import matplotlib.pyplot as plt
    # import time

    # bef = time.perf_counter()
    # n_essais = 100
    # nb_essais = [play(codemaker, codebreaker, quiet=True) for i in range(n_essais)]
    # aft = time.perf_counter()
    # print(aft - bef)
    # plt.suptitle(f'Hist of the number of tries before victory for {n_essais} games')
    # plt.hist(nb_essais, bins=16 - 1, density=True, align='left', rwidth=0.6)
    # print(flush=True)
    # plt.tight_layout()
    # plt.show()

    # play(codemaker, codebreaker, quiet=True)

    # import codebreaker3 as codebreaker
    # import codemaker2 as codemaker
    # import os
    # import sys
    # print(f'{common.LENGTH = }')
    # print(f'{len(common.COLORS) = }', flush=True)

    # folder_name = f'log_opti_{codemaker.__name__}_C={len(common.COLORS)}'

    # if folder_name not in os.listdir():
    #     os.mkdir(folder_name)

    # i = int(sys.argv[1])
    # play_log(codemaker, codebreaker, f'log_opti_{codemaker.__name__}_C={len(common.COLORS)}/{i}.txt')
    # print(flush=True)
