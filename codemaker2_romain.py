import itertools
import random as rd
import common

def init():
    global solution
    solution = ''.join(rd.choices(common.COLORS, k=common.LENGTH))

    global solutions_equivalentes
    solutions_equivalentes = set(map(''.join, itertools.product(common.COLORS, repeat = common.LENGTH)))

    return

def codemaker(combinaison):
    global solution
    global solutions_equivalentes

    solution = trouve_pire_solution(combinaison, solutions_equivalentes)
    eval_comb = common.evaluation(combinaison, solution)
    common.maj_possibles(solutions_equivalentes, combinaison, eval_comb)

    return eval_comb


def trouve_pire_solution(combinaison, solutions_equivalentes):
    dico_len= {}
    memo_eval = set()

    for test_solution in solutions_equivalentes:

        c1 = solutions_equivalentes.copy()
        eval_test = common.evaluation(combinaison, test_solution)

        if eval_test not in memo_eval:

            memo_eval.add(eval_test)
            common.maj_possibles(c1, combinaison, eval_test)
            dico_len[test_solution] = len(c1)

    return max(dico_len, key= lambda x: dico_len[x])
