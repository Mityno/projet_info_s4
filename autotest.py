import common 

# tests sont effectue avec LENGTH = 4  et COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
# sauf en cas de contre indication


#%% tests de la fonction evaluation

reference = 'RVBJ'
test = ['RRNM', 'VROJ', 'MMMM', 'RVBJ']
eval_attendu = [(1,0), (1,2), (0,0), (4,0)]

print(' test de la fonction evaluation \n')

for i in range(len(test)):
    evaluation = common.evaluation(reference, test[i])
    print(f' reference : {reference} \n solution teste : {test[i]} \n evaluation attendu : {eval_attendu[i]} \n evaluation donnee : {evaluation}')
    if evaluation == eval_attendu[i]:
        print(" test valide \n")
    else :
        print('erreur dans la fonction')



#%% tests de la fonction donner_possibles
common.LENGTH = 2
common.COLORS =["a","b","c"]

eval_donne = [(1,0), (0,1)]
comb= ['aa', "ab"]
comb_possibles = [{"ab","ac","ba","ca"}, {"bc", "ca"}]


print('\n test de la fonction donner_possible \n')
for i in range(len(comb)):
    comb_possibles_fonction = common.donner_possibles(comb[i], eval_donne[i])
    print(f' combinaison teste : {comb[i]} \n evaluation donnee : {eval_donne[i]} \n cominaison possibles de l\'evaluation : {comb_possibles[i]} \n combinaison possibles de la fonction : {comb_possibles_fonction}')
    if comb_possibles_fonction == comb_possibles[i] :
        print(' test valide \n')
    else :
        print("/!\\ la fonction a un probleme")

common.LENGTH = 4
common.COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']

#%% tests de la fonction maj_possibles

common.LENGTH = 3
common.COLORS =["a","b","c","d"]

comb_possibles = [{"abc", "cba", "aba", "cbc"}, {"abc", "dab", "acc", "cdb", "aaa", "abc"}, {"abd", "abc", "abb"}]
comb_test = ["abc", "abd", "acd"]
eval_donnee = [(1,2), (1,0), (1,1)]
maj_comb_possibles = [{"cba"}, {"acc", "aaa"}, {"abc"}]

print('\n test de la fonction maj_possible \n')
for i in range(len(comb_possibles)):
    print(f' combinaison teste : {comb_test[i]} \n evaluation donnee : {eval_donnee[i]} \n ensemble des solutions possibles initialement : {comb_possibles[i]}')
    common.maj_possibles(comb_possibles[i], comb_test[i], eval_donnee[i])
    print(f' solution possibles restantes : {maj_comb_possibles[i]} \n solutions possibles de la fonction : {comb_possibles[i]}')
    if maj_comb_possibles[i] == comb_possibles[i]:
        print(" test valide \n")
    else :
        print("/!\\ la fonction a un probleme")


common.LENGTH = 4
common.COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']

#%% tests de la fonction evil_codemaker

common.LENGTH = 3
common.COLORS =["a","b","c","d"]

comb_possibles = [{"aaa","bbb","abc","ccc","cca","acb","bca","bca","abb"}, {"aaa","bbb","abc","ccc","cca","acb","bca","bca","abb"}]
comb_test = ["abc", "aac"]
solutions_optimales = [{"aaa","bbb","ccc"}, {"aaa", "ccc", "abb"}]

print('\n test de la fonction evil_codemaker \n')

for i in range(len(comb_test)):
    print(f' combinaison teste : {comb_test[i]} \n ensemble des solutions possibles initialement : {comb_possibles[i]}')
    sol = common.evil_codemaker(frozenset(comb_possibles[i]), comb_test[i])
    print(f' solution idéales possibles : {solutions_optimales[i]} \n solution propose : {sol}')
    if sol in list(solutions_optimales[i]) :
        print(" test valide \n")
    else :
        print("/!\\ la fonction a un probleme")



common.LENGTH = 4
common.COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']