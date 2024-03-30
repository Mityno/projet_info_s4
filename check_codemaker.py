import codemaker2 as codemaker
import common
import itertools


def check_game(filename):
    with open(filename, mode='r') as file:
        datas = file.read()

    datas = datas.strip().split()
    # print(repr(datas))
    it = iter(datas)
    combs, evs = zip(*zip(it, it))
    evs = [tuple(map(int, ev.split(','))) for ev in evs]

    comb_possibles = {
        ''.join(comb) for comb in itertools.product(common.COLORS, repeat=common.LENGTH)
    }
    print(len(comb_possibles))
    print()

    for comb, ev in zip(combs, evs):
        print(comb, ev)
        common.maj_possibles(comb_possibles, comb, ev)
        print(len(comb_possibles))
        if len(comb_possibles) <= 10:
            print(comb_possibles)
        print()

        if not comb_possibles:
            print('Le codemaker a triché')
            return False

    print('Le codemaker n\'a pas triché')
    return True


if __name__ == '__main__':
        # log_opti_codemaker2_C=8\107.txt
        # log_opti_codemaker2_C=8\115.txt
    logs_path = r'''
        log_opti_codemaker2_C=8\29.txt
        log_opti_codemaker2_C=8\42.txt
        log_opti_codemaker2_C=8\1.txt
        '''.split()

    for path in logs_path:
        check_game(path)
