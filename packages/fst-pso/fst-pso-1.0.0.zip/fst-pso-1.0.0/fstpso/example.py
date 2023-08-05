from fstpso import FuzzyPSO

import sys; sys.path.insert(0, ".."); import pso_benchmarks as pb	 # benchmarks
from multiprocessing import Pool

def custom(solutions):
	retlist = []
	for s in solutions:
		retlist.append( pb.Ackley(s.X) )
	return retlist


dims = 10
FP = FuzzyPSO( D=dims )
FP.set_fitness(pb.Ackley)
FP.set_search_space( [[-30, 30]]*dims )	
result =  FP.solve_with_fstpso(max_iter=100)
print "Best solution:", result[0]
print "Whose fitness is:", result[1]
