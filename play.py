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
        print(f'Combinaisons de taille {common.LENGTH}, '
              f'couleurs disponibles {common.COLORS}')
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

    Elle a la particularité d'écrire les logs de la partie dans le fichier dont
    le nom est donné en argument
    """

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

    with open(nom_fichier, mode='w') as fichier:
        for comb, ev in zip(liste_comb, liste_eval):
            fichier.write(f'{comb}\n{ev[0]},{ev[1]}\n')

    return n_essais


if __name__ == '__main__':

    # permet d'éviter une erreur de syntaxe si tous les blocs ci-dessous sont
    # commentés
    ...

    # Test pour vérifier s'il y a triche dans une partie

    # import codemaker_triche
    # import codebreaker_triche

    # play_log(codemaker_triche, codebreaker_triche, 'log_triche.txt')

    # Ci dessous sont disponibles les codes générant les différents graphes
    # présents dans le rapport. Ceux-ci sont séparés par des commentaires
    # désignant chaque question.
    
    # Question 3 : codebreaker 0 contre codemaker 1
    
    # import codemaker1 as codemaker1
    # import codebreaker0 as codebreaker
    # import matplotlib.pyplot as plt
    # import time

    # n = 8_000

    # mid = time.perf_counter()
    # nb_essais_c1 = [play(codemaker1, codebreaker, quiet=True) for i in range(n)]
    # aft = time.perf_counter()
    # print(f'codemaker 1 : {aft - mid:.2f}', flush=True)
    # # print(aft - bef)

    # set_essais = set(nb_essais_c1)
    # # print(set_essais)
    # bins = np.array(sorted(list(set_essais)))[::50] - 0.5
    # moyenne = sum(nb_essais_c1)/len(nb_essais_c1)
    # # print(bins)

    # plt.hist(
    #     nb_essais_c1,
    #     bins=bins, density=True,
    #     histtype='bar')
    # # plt.plot(list(range(len(nb_essais))), nb_essais)
    # plt.axvline(moyenne, color='r', label=moyenne)
    # plt.xlabel('Nombres d\'essais du codebreaker 0 contre codemaker 1')
    # plt.tight_layout()
    # plt.legend()
    # plt.show()
    # # plt.savefig('Images/Codebreaker0 contre codemaker1.jpg', dpi=300, format='jpg')
    # print('Finished')
    # exit()

    # Question 4 codemaker 1 contre codebreaker 1

    # import codemaker1 as codemaker1
    # import codebreaker1 as codebreaker
    # import matplotlib.pyplot as plt
    # import time

    # n = 8_000

    # mid = time.perf_counter()
    # nb_essais_c1 = [play(codemaker1, codebreaker, quiet=True) for i in range(n)]
    # aft = time.perf_counter()
    # print(f'codemaker 1 : {aft - mid:.2f}', flush=True)
    # # print(aft - bef)

    # set_essais = set(nb_essais_c1)
    # # print(set_essais)
    # bins = np.array(sorted(list(set_essais)))[::50] - 0.5
    # moyenne = sum(nb_essais_c1)/len(nb_essais_c1)
    # # print(bins)

    # plt.hist(
    #     nb_essais_c1,
    #     bins=bins, density=True,
    #     histtype='bar')
    # # plt.plot(list(range(len(nb_essais))), nb_essais)
    # plt.axvline(moyenne, color='r', label=moyenne)
    # plt.xlabel('Nombres d\'essais du codebreaker 1 contre codemaker 1')
    # plt.tight_layout()
    # plt.legend()
    # plt.show()
    # # plt.savefig('Images/Codebreaker1 contre codemaker1.jpg', dpi=300, format='jpg')
    # print('Finished')
    
    # Question 7 : codemaker 1 contre codebraker 2
    
    # import codemaker1 as codemaker1
    # import codebreaker2 as codebreaker
    # import matplotlib.pyplot as plt
    # import time

    # n = 2_000

    # mid = time.perf_counter()
    # nb_essais_c1 = [play(codemaker1, codebreaker, quiet=True) for i in range(n)]
    # aft = time.perf_counter()
    # print(f'codemaker 1 : {aft - mid:.2f}', flush=True)

    # set_essais = set(nb_essais_c1)
    # # print(set_essais)
    # bins = np.array(sorted(list(set_essais))) - 0.5
    # # print(bins)

    # print('Mean :', np.array(nb_essais_c1).mean())

    # plt.hist(
    #     nb_essais_c1,
    #     bins=bins, density=True,
    #     histtype='bar')
    # plt.xlabel('Nombres d\'essais du codebreaker 2 contre codemaker 1')
    # plt.tight_layout()
    # plt.show()
    # # plt.savefig('Images/Codebreaker2 contre codemaker1.jpg', dpi=300, format='jpg')
    # print('Finished')

    # Question 8 : comparaison codebreaker 2 contre codemaker 1 et contre codemaker 2

    # import codemaker2 as codemaker2
    # import codemaker1 as codemaker1
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
    # bins = np.array(sorted(list(set_essais))) - 0.5
    # print(bins)

    # plt.hist(
    #     (nb_essais_c1, nb_essais_c2),
    #     bins=bins, density=True,
    #     label=('Codemaker 1', 'Codemaker 2'), histtype='bar')
    # # plt.plot(list(range(len(nb_essais))), nb_essais)
    # plt.xlabel('Nombres d\'essais du codebreaker 2')
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    # # plt.savefig('Images/Comparaison des codemaker 1 et 2.jpg', dpi=300, format='jpg')
    # print('Finished')

    # Question 12 (traitement de données)

    # import matplotlib.pyplot as plt
    
    # nb_essais = []
    # for i in range(150):
    #     filename = f'log_opti_codemaker1_C=8/{i+1}.txt'
    #     with open(filename, mode='r') as file:
    #         datas = file.read()

    #     datas = datas.strip().split()
    #     it = iter(datas)
    #     combs, evs = zip(*zip(it, it))
    #     evs = [tuple(map(int, ev.split(','))) for ev in evs]
    #     nb_essais.append(len(evs))
        
    # bins = np.array(list(set(nb_essais))) - 0.5
    # bins = list(bins)
    # bins.append(max(bins)+1)
    # # print(bins)

    # plt.hist(
    #     nb_essais,
    #     bins=bins, density=True,
    #     histtype='bar')
    # plt.xlabel('Nombres d\'essais du codebreaker 3 contre le codemaker 1')
    
    # plt.tight_layout()
    # # plt.savefig('Images/nombre d\'essaie du codebreaker3 contre le codemaker1.jpg', dpi=300, format='jpg')
    # plt.show()
