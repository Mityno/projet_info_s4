#!/usr/bin/env python3

import common


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

    import codemaker2 as codemaker
    import codebreaker2 as codebreaker
    import matplotlib.pyplot as plt
    import time
    
    # bef = time.perf_counter()
    # nb_essais = [play(codemaker, codebreaker, quiet=True) for i in range(100)]
    # aft = time.perf_counter()
    # print(aft - bef)
    # # plt.hist(nb_essais, bins=20)
    # plt.plot(list(range(len(nb_essais))), nb_essais)
    # plt.show()
    
    play_log(codemaker, codebreaker, 'log.txt')
