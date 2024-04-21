
import common
import itertools

# tests sont effectués avec les paramètres
# LENGTH = 4 et COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
# sauf en cas de contre indication
# si un test échoue, on lève une erreur et les tests s'arrêtent là

# on conserve les valeurs initiales des paramètres du jeu qui vont être
# modifiés dans les tests afin de pouvoir les remettre en fin de programme
OLD_LENTGTH = common.LENGTH
OLD_COLORS = common.COLORS

# %% tests de la fonction evaluation

reference = "RVBJ"
tests = ["RRNM", "VROJ", "MMMM", "RVBJ"]
evals = [(1, 0), (1, 2), (0, 0), (4, 0)]

print("Test de la fonction evaluation \n")

for comb, eval_attendue in zip(tests, evals):
    evaluation = common.evaluation(reference, comb)
    print(
        f" Référence : {reference} \n  Solution testée : {comb} \n  Évaluation attendue : {eval_attendue} \n  Évaluation donnée : {evaluation}"
    )
    if evaluation == eval_attendue:
        print(" Test valide \n")
    else:
        raise Exception("Erreur dans la fonction d'évaluation")

# %% tests de la fonction donner_possibles
common.LENGTH = 2
common.COLORS = ["a", "b", "c"]

evals = [(1, 0), (0, 1)]
combs = ["aa", "ab"]
all_comb_possibles = [{"ab", "ac", "ba", "ca"}, {"bc", "ca"}]


print("\nTest de la fonction donner_possible\n")
for comb_test, eval_donnee, comb_possibles in zip(combs, evals, all_comb_possibles):
    comb_possibles_fonction = common.donner_possibles(comb_test, eval_donnee)
    print(
        f" Combinaison testée : {comb_test} \n  Évaluation donnée : {eval_donnee} \n  Combinaison possibles de l'évaluation : {comb_possibles} \n  Combinaison possibles de la fonction : {comb_possibles_fonction}"
    )
    if comb_possibles_fonction == comb_possibles:
        print(" Test valide \n")
    else:
        raise Exception(r"/!\ la fonction donner_possible a un probleme")

# %% tests de la fonction maj_possibles

comb_possibles = [
    {"abc", "cba", "aba", "cbc"},
    {"abc", "dab", "acc", "cdb", "aaa", "abc"},
    {"abd", "abc", "abb"},
]
comb_test = ["abc", "abd", "acd"]
eval_donnee = [(1, 2), (1, 0), (1, 1)]
maj_comb_possibles = [{"cba"}, {"acc", "aaa"}, {"abc"}]

print("\nTest de la fonction maj_possible \n")
for i in range(len(comb_possibles)):
    print(
        f" Combinaison testée : {comb_test[i]} \n  Évaluation donnée : {eval_donnee[i]} \n  Ensemble des solutions possibles initialement : {comb_possibles[i]}"
    )
    common.maj_possibles(comb_possibles[i], comb_test[i], eval_donnee[i])
    print(
        f"  Solution possibles restantes : {maj_comb_possibles[i]} \n  Solutions possibles de la fonction : {comb_possibles[i]}"
    )
    if maj_comb_possibles[i] == comb_possibles[i]:
        print(" Test valide \n")
    else:
        raise Exception(r"/!\ la fonction maj_possible a un probleme")

# %% tests de la fonction evil_codemaker

comb_possibles = [
    {"aaa", "bbb", "abc", "ccc", "cca", "acb", "bca", "bca", "abb"},
    {"aaa", "bbb", "abc", "ccc", "cca", "acb", "bca", "bca", "abb"},
]
comb_test = ["abc", "aac"]

# on construit les solutions optimales avec leur définition stricte
solutions_optimales = []
for i in range(len(comb_possibles)):
    curr_comb_possibles = comb_possibles[i].copy()
    curr_comb_test = comb_test[i]
    max_len = 0
    best_combs = []
    for temp_sol in curr_comb_possibles:
        temp_comb_possibles = curr_comb_possibles.copy()
        temp_eval = common.evaluation(curr_comb_test, temp_sol)
        common.maj_possibles(temp_comb_possibles, curr_comb_test, temp_eval)
        if len(temp_comb_possibles) > max_len:
            max_len = len(temp_comb_possibles)
            best_combs = [temp_sol]
        elif len(temp_comb_possibles) == max_len:
            best_combs.append(temp_sol)

    solutions_optimales.append(best_combs)

print("\nTest de la fonction evil_codemaker \n")

for i in range(len(comb_test)):
    print(
        f" Combinaison testée : {comb_test[i]} \n  Ensemble des solutions possibles initialement : {comb_possibles[i]}"
    )
    sol = common.evil_codemaker(frozenset(comb_possibles[i]), comb_test[i])
    curr_comb_possibles = comb_possibles[i].copy()
    common.maj_possibles(
        curr_comb_possibles, comb_test[i], common.evaluation(comb_test[i], sol)
    )
    print(
        f"  Solutions idéales possibles : {solutions_optimales[i]} \n  Solution proposée : {sol}"
    )
    if sol in list(solutions_optimales[i]):
        print(" Test valide \n")
    else:
        raise Exception(r"/!\ la fonction evil_codemaker a un probleme")


common.LENGTH = OLD_LENTGTH
common.COLORS = OLD_COLORS
