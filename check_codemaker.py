import common
import itertools


def check_game(filename):

    """
    Vérifie que la partie jouée dans le fichier log de chemin `filename` n'a
    pas été trichée. Renvoie True si la partie est sans triche, False sinon.
    """

    with open(filename, mode='r') as file:
        datas = file.read()

    # on sépare toutes les lignes
    datas = datas.strip().split()
    it = iter(datas)

    # zip(it, it) permet de récupérer les couples (combinaison, évaluation)
    # le second zip permet de les séparer en deux tuples respectivement
    # de combinaisons et d'évaluations (sous forme de strings)
    combs, evs = zip(*zip(it, it))
    # on convertit les évaluations en des couples d'entiers
    evs = [tuple(map(int, ev.split(','))) for ev in evs]

    # on va simuler le comportement du cobebreaker 2 : on "joue" les coups
    # qui sont présents dans les logs, et on voit si les évaluations mènent
    # à une situation où plus aucun coups n'est possible, auquel cas le
    # codemaker a triché
    comb_possibles = {
        ''.join(comb)
        for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }

    for comb, ev in zip(combs, evs):
        common.maj_possibles(comb_possibles, comb, ev)

        # la "solution" du codemaker n'existe plus dans les combinaisons
        # possibles : il a triché
        if not comb_possibles:
            print('Le codemaker a triché')
            return False

    print('Le codemaker n\'a pas triché')
    return True


if __name__ == '__main__':
    # ajouter les chemins vers les logs à vérifier (on peut mettre plusieurs)
    # chemins de fichier en les séparant par un espace ou retour à la ligne.
    logs_path = r'''log0.txt'''.split()

    for path in logs_path:
        print(f'Path : {path}')
        check_game(path)
        print()

