import common 

# tests sont effectue avec LENGTH = 4  et COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
# sauf en cas de contre indication

#%% tests de la fonction evaluation

reference = 'RVBJ'
test1 = 'RRNM'
test2 = 'VROJ'
test3 = 'MMMM'
test4 = 'RVBJ'

eval_test1 = common.evaluation(test1, reference)
if eval_test1 == (1,0):
    print('test1 est valide')
    
eval_test2 = common.evaluation(test2, reference)
if eval_test2 == (1,2):
    print('test2 est valide')
    
eval_test3 = common.evaluation(test3, reference)
if eval_test3 == (0,0):
    print('test3 est valide')

eval_test4 = common.evaluation(test4, reference)
if eval_test4 == (4,0):
    print('test4 est valide')


#%% tests de la fonction donner_possibles
common.LENGTH = 2
common.COLORS =["a","b","c"]

eval_donne1 = (1,0)
comb1= 'aa'

comb_possibles = {"ab","ac","ba","ca"}
comb1_possibles = common.donner_possibles(comb1, eval_donne1)

if comb1_possibles == comb_possibles:
    print("test1 de donner_possible valide")

eval_donne2 = (0,1)
comb2 = "ab"

comb_possibles = {"bc", "ca"}
comb2_possibles = common.donner_possibles(comb2, eval_donne2)

if comb_possibles == comb2_possibles:
    print('test2 de donner_possibles valide')
common.LENGTH = 4
common.COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']

#%% tests de la fonction maj_possibles




#%% tests de la fonction evil_codemaker


