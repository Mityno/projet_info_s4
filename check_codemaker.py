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

    for comb, ev in zip(combs, evs):
        common.maj_possibles(comb_possibles, comb, ev)

        if not comb_possibles:
            print('Le codemaker a triché')
            return False

    print('Le codemaker n\'a pas triché')
    return True


if __name__ == '__main__':
    # print(check_game('log0.txt'))
    # print(check_game('log_triche.txt'))

    for i in range(5):
        print(check_game(f'log/log{i + 1}.txt'))