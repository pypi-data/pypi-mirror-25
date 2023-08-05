from pylab import *
import fuzzy
import fuzzy.storage.fcl.Reader
from mpl_toolkits.mplot3d import Axes3D

def process_operators(operator, verbose=False):
	if isinstance(operator, fuzzy.operator.Input.Input):
		if verbose: print "    Simple input", operator.adjective.getName(fuzzySystem), 
		MEMB = operator.adjective.membership
		if verbose: print "membership =", MEMB
		if MEMB==None:
			warnings.warn("input for "+operator.adjective.getName(self.fuzzySystem)[1]+" not specified")
		return MEMB
		
	elif isinstance(operator, fuzzy.operator.Compound.Compound):
		if verbose: print "    Multiple inputs: "			
		BEST = sys.float_info.max
		for inp in operator.inputs:
			MEMB = process_operators(inp, verbose=verbose)
			if MEMB==None: 
					warnings.warn("input for "+inp.adjective.getName(self.fuzzySystem)[1]+" not specified")
			elif MEMB<BEST:
				BEST = MEMB			
		return BEST
				


def get_singleton_value(adj):
	return adj.set.getCOG()

def return_all_output_variable_names(fuzzySystem):
	ret = {}
	for name, i in fuzzySystem.variables.items():
		if isinstance(i , fuzzy.OutputVariable.OutputVariable):
			ret[str(name)]=[0, 0]
	return ret

def actual_sugeno_inference(fuzzySystem, verbose=False):

	all_outputs = return_all_output_variable_names(fuzzySystem)		

	for name, rule in fuzzySystem.rules.items():
		if verbose: print " * Processing rule", name

		MEMB = 0
		DENO = 0
		NUME = 0

		SINGLETON = 0


		if isinstance(rule.adjective, fuzzy.Adjective.Adjective):
			if verbose: print "WARNING: Aggettivo output semplice, non supportato"
			pass
		elif isinstance(rule.adjective,list):
			
			if verbose: print "  * Processing list of OUTPUT adjectives..."

			# what output are we updating?
			for adj in rule.adjective:
				outlabel, outname = adj.getName(fuzzySystem)
				
				if verbose: print "   ", outlabel, outname, 
				SINGLETON = get_singleton_value(adj)
				if verbose: print "whose singleton is", SINGLETON

			# process operators (i.e., input nodes)
			MEMB = process_operators(rule.operator, verbose=verbose)
			if MEMB==None:
				# raise Exception("error: input for "+inp.adjective.getName(self.fuzzySystem)[1]+" not specified")
				# warnings.warn("input for "+inp.adjective.getName(self.fuzzySystem)[1]+" not specified")
				if verbose: print "WARNING: cannot calculate MAX membership value"
				pass
			else:
				DENO += MEMB	
				NUME += MEMB*SINGLETON
				if verbose: print "      Product =", MEMB*SINGLETON

		else:
			raise Exception("rule target not set.")

		all_outputs[outname][0]+=NUME
		all_outputs[outname][1]+=DENO

	if verbose: print all_outputs

	final = {}
	for out, valout in all_outputs.items():
		if valout[1]==0:
			final[out]=0
		else:
			final[out] = valout[0]/valout[1]
	return final

def sugeno_inference(my_input, fuzzySystem, verbose=False):
	"""
		Calculates the Sugeno rule of inference using the specified
		input values and updating the specified output values.
		Appearently, the Sugeno method is not implemented in pyfuzzy. 
		This method replaces pyfuzzy's calculate() method.
	"""

	fuzzySystem.reset()
	fuzzySystem.fuzzify(my_input)
	
	# the following replaces pyfuzzy's inference() method
	my_output = actual_sugeno_inference(fuzzySystem, verbose=verbose)

	# self.fuzzySystem.defuzzify(my_output)
	return my_output



if __name__ == '__main__':
	
	path = "pso_generated.fcl"
	fuzzySystem = fuzzy.storage.fcl.Reader.Reader().load_from_file(path)		


	DETX = 50
	DETY = 50

	DISTANCE = linspace(0,125,DETX)
	FITNESS  = linspace(-1,1,DETY)
	Zinertia = []
	Zsocial = []
	Zcognitive = []
	Zlow = []
	Zhigh = []	
	for d in DISTANCE:
		for f in FITNESS:
			my_input = { "Derivative": f, "Distance": d }	# todo
			my_output = { "Inertia": 0.0, "Social": 0.0, "Cognitive": 0.0, "Maxspeed": 0.0, "Sigma": 0.0 }
			# fuzzySystem.calculate(my_input, my_output)
			my_output = sugeno_inference(my_input, fuzzySystem, verbose=False)
			# print "Phi=", f, "Distance=", d, "Output=", my_output['Inertia']
			Zinertia.append( my_output["Inertia"] )
			Zsocial.append( my_output["Social"] )
			Zcognitive.append( my_output["Cognitive"] )
			Zlow.append( my_output["Sigma"] )
			Zhigh.append( my_output["Maxspeed"] )
	#exit()
	X,Y = meshgrid(FITNESS, DISTANCE)
	Zinertia   = reshape(Zinertia, (DETX,DETY))
	Zsocial    = reshape(Zsocial, (DETX,DETY))
	Zcognitive = reshape(Zcognitive, (DETX,DETY))
	Zlow       = reshape(Zlow, (DETX,DETY))
	Zhigh      = reshape(Zhigh, (DETX,DETY))

	#fig = figure(figsize=(16,9))
	fig = figure(figsize=(14,8.2))


	# inertia
	# ax = fig.add_subplot(2,3,1, projection="3d")	
	#ax.xaxis._axinfo['label']['space_factor'] = 2.0	
	#ax.yaxis._axinfo['label']['space_factor'] = 2.0
	#surf = ax.plot_surface(X,Y,Zinertia, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True, label="Inertia", alpha=.75)
	#cont = ax.contour(X,Y,Zinertia,cmap=cm.jet)
	#ax.set_zlabel("$Inertia$")
	# ax.set_title("$Inertia$")
	#ax.set_xticklabels(["Better", "Same", "Worse"],  verticalalignment='baseline',horizontalalignment='center' ) 
	#ax.set_yticklabels(["Same", "Near", "Far"],  verticalalignment='bottom', horizontalalignment='left' )
	#ax.set_zlim(0.25,1.0)

	last = Y[-1][-1]
	Y /= last

	ax = fig.add_subplot(2,3,1)	
	surf = pcolormesh(X,Y,Zinertia)
	
	#ax.set_ylim(0, last)
	ax.locator_params(nbins=3)
	ax.set_xticklabels(["Better", "Same", "Worse"]) 
	ax.set_yticklabels(["Same", "Near", "Far"])
	ax.set_ylabel("$\delta$", fontsize=15); 
	ax.set_xlabel("$\phi$", fontsize=15)
	cb = fig.colorbar(surf, shrink=0.7, aspect=40, orientation='horizontal', pad=0.15, ticks=[0.3, 0.5, 1.0])
	ax.set_title("$Inertia$")
	surf.set_clim(0.3,1.0)
	cb.ax.set_xticklabels(['LOW', 'MEDIUM', 'HIGH'])
	#ax.set_xticks(["-1", "0", "1"] ); 
	#ax.set_yticks(["0.", "60.", "120.", "121", "122", "123","125"] ); 
	"""
	ax.set_yticks(["0", str(97.5/2.), "97.5"] ); 
	"""
	
	# social
	# ax = fig.add_subplot(2,3,2, projection="3d")	
	ax = fig.add_subplot(2,3,2)	
	ax.locator_params(nbins=3)
	#ax.xaxis._axinfo['label']['space_factor'] = 2.0	
	#ax.yaxis._axinfo['label']['space_factor'] = 2.0
	ax.set_ylabel("$\delta$", fontsize=15); 
	ax.set_xlabel("$\phi$", fontsize=15)
	# surf = ax.plot_surface(X,Y,Zsocial,  rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True, label="Inertia", alpha=.75)
	# cont = ax.contour(X,Y,Zsocial,cmap=cm.jet)
	surf = pcolormesh(X,Y,Zsocial)
	#ax.set_zlabel("$Social$")	
	ax.set_title("$Social$")
	#ax.set_xticks(["-1", "0", "1"] ); ax.set_yticks(["0", str(97.5/2.), "97.5"] ); 
	ax.set_xticklabels(["Better", "Same", "Worse"]); 
	ax.set_yticklabels(["Same", "Near", "Far"] )
	#ax.set_zlim(0.85,3)
	cb = fig.colorbar(surf, shrink=0.7, aspect=40, orientation='horizontal', pad=0.15, ticks=[1,2,3])
	surf.set_clim(1,3)
	cb.ax.set_xticklabels(['LOW', 'MEDIUM', 'HIGH'])
	
	# ax = fig.add_subplot(2,3,3, projection="3d")
	ax = fig.add_subplot(2,3,3)
	ax.locator_params(nbins=3)
	#ax.xaxis._axinfo['label']['space_factor'] = 2.0	
	#ax.yaxis._axinfo['label']['space_factor'] = 2.0
	ax.set_ylabel("$\delta$", fontsize=15); 
	ax.set_xlabel("$\phi$", fontsize=15)
	surf = pcolormesh(X,Y,Zcognitive)
	ax.set_title("$Cognitive$")
	# surf = ax.plot_surface(X,Y,Zcognitive,  rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True, label="Inertia", alpha=.75)
	# cont = ax.contourf(X,Y,Zcognitive,zdir='z', offset=0.1, cmap=cm.jet)
	# cont = ax.contour(X,Y,Zcognitive,cmap=cm.jet)
	# ax.set_xlabel("$\delta_i$"); ax.set_ylabel("$\phi_i$")
	#ax.set_xticks(["-1", "0", "1"] ); ax.set_yticks(["0", str(97.5/2.), "97.5"] ); 
	ax.set_xticklabels(["Better", "Same", "Worse"]); 
	ax.set_yticklabels(["Same", "Near", "Far"] )
	#ax.set_zlabel("$Cognitive$")
	#ax.set_zlim(0.1,3)
	cb = fig.colorbar(surf, shrink=0.7, aspect=40, orientation='horizontal', pad=0.15, ticks=[0.1, 1.5, 3.0])
	surf.set_clim(0.1,3)
	cb.ax.set_xticklabels(['LOW', 'MEDIUM', 'HIGH'])
	
	# ax = fig.add_subplot(2,3,4, projection="3d")
	ax = fig.add_subplot(2,3,4)
	ax.locator_params(nbins=3)
	#ax.xaxis._axinfo['label']['space_factor'] = 2.0	
	#ax.yaxis._axinfo['label']['space_factor'] = 2.0
	#ax.zaxis._axinfo['label']['space_factor'] = 2.0
	#ax.set_xlabel("$\delta$", fontsize=15); 
	#ax.set_ylabel("$\phi$", fontsize=15)
	#surf = ax.plot_surface(X,Y,Zlow,  rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True, label="Inertia", alpha=.75)
	# cont = ax.contourf(X,Y,Zhigh,zdir='z', offset=0, cmap=cm.jet)
	# cont = ax.contour(X,Y,Zlow,cmap=cm.jet)
	surf = pcolormesh(X,Y,Zlow)
	ax.set_title("$\mathcal{L}$")
	ax.set_ylabel("$\delta$", fontsize=15); 
	ax.set_xlabel("$\phi$", fontsize=15)
	#ax.set_xticks(["-1", "0", "1"] ); ax.set_yticks(["0", str(97.5/2.), "97.5"] ); 
	ax.set_xticklabels(["Better", "Same", "Worse"]); 
	ax.set_yticklabels(["Same", "Near", "Far"])
	#ax.set_zlabel("$\mathcal{L}$")
	#ax.set_zlim(-0.001,0.01)
	cb = fig.colorbar(surf, shrink=0.7, aspect=40, orientation='horizontal', pad=0.15, ticks=[0, 0.01])
	surf.set_clim(0,0.01)
	cb.ax.set_xticklabels(['LOW', 'HIGH'])

	# ax = fig.add_subplot(2,3,5, projection="3d")
	ax = fig.add_subplot(2,3,5)
	ax.locator_params(nbins=3)
	#ax.xaxis._axinfo['label']['space_factor'] = 2.0	
	#ax.yaxis._axinfo['label']['space_factor'] = 2.0
	#ax.zaxis._axinfo['label']['space_factor'] = 2.0
	#ax.set_xlabel("$\delta$", fontsize=15); 
	#ax.set_ylabel("$\phi$", fontsize=15)
	# surf = ax.plot_surface(X,Y,Zhigh,  rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True, label="Inertia", alpha=.75)
	# cont = ax.contourf(X,Y,Zlow,zdir='z', offset=0.05, cmap=cm.jet)
	# cont = ax.contour(X,Y,Zhigh,cmap=cm.jet)
	surf = pcolormesh(X,Y,Zhigh)
	ax.set_ylabel("$\delta$", fontsize=15); 
	ax.set_xlabel("$\phi$", fontsize=15)
	#ax.set_xticks(["-1", "0", "1"] ); ax.set_yticks(["0", str(97.5/2.), "97.5"] ); 
	ax.set_xticklabels(["Better", "Same", "Worse"]); 
	ax.set_yticklabels(["Same", "Near", "Far"])
	#ax.set_zlabel("$\mathcal{U}$")
	ax.set_title("$\mathcal{U}$")
	#ax.set_zlim(0.1,0.2)
	cb = fig.colorbar(surf, shrink=0.7, aspect=40, orientation='horizontal', pad=0.15, ticks=[0.1, 0.15, 0.2])
	surf.set_clim(0.1,0.2)
	cb.ax.set_xticklabels(['LOW', 'MEDIUM', 'HIGH'])

	tight_layout()
	#suptitle("Surfaces")
	savefig("C:\\Users\\aresio\\Documents\\papers\\Jfuzzypso\\surfaces.eps")
	#show()
	#savefig("C:\\Users\\aresio\\Documents\\papers\\Jfuzzypso\\surfaces.pdf")
	# savefig("surfaces_new.pdf")
	"""
	INR = reshape(Zinertia, DETX*DETY)
	B = array([(x,y) for x in DISTANCE for y in FITNESS])
	with open("output_surfaces", "w") as fo:
		for x in xrange(DETX):
			for y in xrange(DETY):
				fo.write(str(B[y*DETY+x][0])+"\t")
				fo.write(str(B[y*DETY+x][1])+"\t")
				fo.write(str(INR[y*DETY+x])+"\n")
			fo.write("\n")
	#  FULL = array([ Zinertia, Zcognitive, Zsocial, Zlow, Zhigh ])
	# savetxt("output_surface_inertia", zip(B,) )
	# print FULL.T

	# savetxt("output_surface_compatte", FULL.T)
	"""
