import math
import pso
import fuzzy.storage.fcl.Reader
from surfaces import *
from numpy import random


class FuzzyPSO(pso.PSO_new):

	def __init__(self, D=None):
		super(FuzzyPSO, self).__init__()		

		if not isinstance(D, int):
			print "ERROR: please specifiy an integer number >0 for the number of dimensions"
			exit(-1)
		else:
			self.numberofparticles = int(10 + 2*math.sqrt(D))
			self.dimensions = D
			print " * Number of particles automatically set to", self.numberofparticles

		# defaults for membership functions
		self.DER1 = -1.0
		self.DER2 =  1.0
		self.MDP1 = 0.2 
		self.MDP2 = 0.4 
		self.MDP3 = 0.6 
		self.MaxDistance = 0

		self.enabled_settings = [ "cognitive", "social", "inertia", "minvelocity", "maxvelocity" ]


	def solve_with_fstpso(self, max_iter, use_log=False, verbose=False):

		if self.FITNESS == None:
			print "ERROR: cannot solve a problem without a fitness function; use set_fitness()"
			exit(-3)

		if self.Boundaries == []:
			print "ERROR: FST-PSO cannot solve unbounded problems; use set_search_space()"
			exit(-4)

		self.MaxIterations = max_iter
		print " * Max iterations set to", self.MaxIterations
		print " * Launching optimization"

		self.CreateParticles(self.numberofparticles, self.dimensions, use_log=use_log)
		result = self.Solve( None, verbose=verbose )
		return result


	def set_search_space(self, limits):
		self.GenerateFCL(max_distance= calculate_max_distance(limits))
		self.Boundaries = limits		
		print " * Search space boundaries set to:", limits

		self.MaxVelocity = [math.fabs(limits[0][1]-limits[0][0])]*self.dimensions
		print " * Max velocities set to:", self.MaxVelocity


	def set_fitness(self, fitness):	
		try:
			fitness([0])
			self.FITNESS = fitness
			self.ParallelFitness = False
		except:
			print "ERROR: the specified function does not seem to implement a correct fitness function"
			exit(-2)


	def set_parallel_fitness(self, fitness):
		np = pso.Particle()
		np.X = [0]
		try: 
			fitness([np])
			self.FITNESS = fitness
			self.ParallelFitness = True
		except:
			print "ERROR: the specified function does not seem to implement a correct parallel fitness function"
			exit(-3)	
		


	def GenerateFCL(self, max_distance=100):
		"""
			This method creates an FCL file for the problem under optimization. 
		"""

		self.MaxDistance = max_distance

		with open("pso_generated.fcl", "w") as fo:
			with open("pso_1st_half_2.fcl") as fi:
				doc = fi.read()
				fo.write(doc)

			p1 = max_distance*self.MDP1
			p2 = max_distance*self.MDP2
			p3 = max_distance*self.MDP3

			fo.write("FUZZIFY Distance\n")
			fo.write("\tTERM Same := (0,0) (0,1) ("+str(p1)+",1) ("+str(p2)+",0);\n")
			fo.write("\tTERM Near := ("+str(p1)+",0) ("+str(p2)+",1) ("+str(p3)+",0);\n")
			fo.write("\tTERM Far  := ("+str(p2)+",0) ("+str(p3)+",1) ("+str(max_distance)+",1) ("+str(max_distance)+",0);\n")
			fo.write("END_FUZZIFY\n\n")

			# new derivative			
			fo.write("FUZZIFY Derivative\n")
			fo.write("\tTERM Worse :=   ( 0,0) (1,1)   (1,0);\n")
 			# fo.write("\tTERM Same :=    (-0.025,0) (0,1)   ( 0.025,0);\n")
			fo.write("\tTERM Same :=    ("+str(self.DER1)+",0) (0,1)   ("+str(self.DER2)+",0);\n")
			fo.write("\tTERM Better  := (-1.0,0)   (-1,1)  (0,0);\n")
			fo.write("END_FUZZIFY\n\n")
			
			with open("pso_2nd_half_2.fcl") as fi:
				doc = fi.readlines()					
				fo.write("\n".join(doc))
			
		self.InitFuzzy("pso_generated.fcl")



	def InitFuzzy(self, path="pso.fcl"):		
		"""
			Initialize the fuzzy systems according to FST-PSO and problem's settings. 
		"""
		self.fuzzySystem = fuzzy.storage.fcl.Reader.Reader().load_from_file(path)		
		print " * Fuzzy subsystem initialized"


	def phi(self, f_w, f_o, f_n, phi, phi_max):
		""" 
			Calculates the Fitness Incremental Factor (phi).
		"""
		if phi == 0: return 0
		denom = (min(f_w, f_n) - min(f_w, f_o))/f_w			# 0..1
		numer = phi/phi_max									# 0..1		
		return denom*numer






	def UpdateCalculatedFitness(self):
		"""
			Calculate the fitness values for each particle according to user's fitness function,
			and then update the settings of each particle.
		"""

		
		if self.ParallelFitness:
			all_fitness = self.FITNESS(self.Solutions)
		else:
			all_fitness = []
			for s in self.Solutions:
				all_fitness.append( self.FITNESS(s.X) )
			
		#print " * All fitness:", all_fitness


		if True:

			# for each i-th individual "s"...
			for i,s in enumerate(self.Solutions):
				
				prev = s.CalculatedFitness
				#ret = self.FITNESS(s.X)
				ret = all_fitness[i]
				if s.MagnitudeMovement!=0:
					s.DerivativeFitness = (ret-prev)/s.MagnitudeMovement

				s.NewDerivativeFitness = self.phi( self.EstimatedWorstFitness, prev, ret, s.MagnitudeMovement, self.MaxDistance )				
				
				if isinstance(ret, list):
					s.CalculatedFitness = ret[0]
					s.Differential = ret[1]
				else:
					s.CalculatedFitness = ret
				
				my_input = { "Derivative": s.NewDerivativeFitness, "Distance": s.DistanceFromBest }	
				my_output = { "Inertia": 0.0, "Social": 0.0, "Cognitive": 0.0, "Maxspeed": 0.0, "Sigma": 0.0 }

				
				try:
					my_output = sugeno_inference(my_input, self.fuzzySystem, verbose=False)
				except:
					print my_input
					exit(-100)

				if "cognitive" in self.enabled_settings: 	s.CognitiveFactor = my_output["Cognitive"]
				if "social" in self.enabled_settings: 		s.SocialFactor = my_output["Social"]
				if "inertia" in self.enabled_settings: 		s.Inertia = my_output["Inertia"]
				if "maxvelocity" in self.enabled_settings: 	s.MaxSpeedMultiplier = my_output["Maxspeed"]		# because velocities are vectorial
				if "minvelocity" in self.enabled_settings: 	s.MinSpeedMultiplier = my_output["Sigma"]			# because velocities are vectorial
			

	
	def UpdatePositions(self):
		"""
			Update particles' positions and update the internal information.
		"""

		for p in self.Solutions:	

			prev_pos = p.X[:]

			for n in range(len(p.X)):							
				c1 = p.X[n]
				c2 = p.V[n]
				tv = c1+c2
				rnd1 = rnd2 = 0
				if tv > self.Boundaries[n][1]:
					rnd1 = random.random()
					tv = self.Boundaries[n][1] - rnd1 * c2
				if tv < self.Boundaries[n][0]:
					rnd2 = random.random()
					tv = self.Boundaries[n][0] - rnd2 * c2

				p.X[n] = tv

			p.MagnitudeMovement = linalg.norm(array(p.X)-array(prev_pos), ord=2)
			p.DistanceFromBest = linalg.norm(array(p.X)-array(self.G.X), ord=2)


	def UpdateVelocities(self):
		"""
			Update the velocity of all particles, according to their own settings.
		"""

		for p in self.Solutions:

			for n in range(len(p.X)):

				fattore1 = p.Inertia * p.V[n]
				fattore2 = random.random() * p.CognitiveFactor * ( p.B[n] - p.X[n] )
				fattore3 = random.random() * p.SocialFactor * ( self.G.X[n] - p.X[n] )

				newvelocity = fattore1+fattore2+fattore3

				# check max vel
				if ( newvelocity>self.MaxVelocity[n] * p.MaxSpeedMultiplier ):
					newvelocity = self.MaxVelocity[n] * p.MaxSpeedMultiplier 
				elif ( newvelocity<-self.MaxVelocity[n] * p.MaxSpeedMultiplier ):
					newvelocity = -self.MaxVelocity[n] * p.MaxSpeedMultiplier 

				# check min vel
				if ( abs(newvelocity)<self.MaxVelocity[n] * p.MinSpeedMultiplier ):
					newvelocity = copysign( self.MaxVelocity[n] * p.MinSpeedMultiplier, newvelocity)

				# finally set velocity
				p.V[n] = newvelocity


def calculate_max_distance(interval):
	accum = 0
	for i in interval:
		accum += (i[1]-i[0])**2
	return math.sqrt(accum)



if __name__ == '__main__':
	
	print "ERROR: please create a new FuzzyPSO object, specify a fitness function and the search space"

	