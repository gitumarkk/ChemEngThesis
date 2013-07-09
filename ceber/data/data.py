#===============================================================================
# Data storage for all the runs, will eventually put it in a different
# script file then importing it.
#===============================================================================
	
def data_run(run):
	"""
		I am creating a data dictionary which I will use later
	"""
	data = {}				
	"""
		BELOW IS THE BEST WAY TO ARRANGE THROUGH THE DATA
	"""					
	data[7.3] = {2:[[0, 15, 30, 66, 90, 120, 180],
					[1.381, 1.013, 0.701, 0.763, 0.779, 0.783, 0.807],
					[1.349, 1.316, 1.093, 1.330, 1.306, 1.321, 1.372]],
					
				4: [[0, 15, 30, 66, 90, 120, 180],
				[1.381, 0.737, 0.560, 0.327, 0.272, 0.313, 0.254],
				[1.349, 1.286, 1.299, 1.305, 1.331, 1.322, 1.373]]}
				
	data[7.4] = {2 : [[0, 5, 10, 15, 20, 30, 45, 60],
					[1.357, 1.124, 1.044, 0.978, 0.939, 0.876, 0.873, 0.847],
					[1.334, 1.349, 1.364, 1.326, 1.338, 1.353, 1.368, 1.345]]}
					
	data[7.5] = {2 : [[0, 5, 10, 15, 20, 30, 45, 60],
					[3.060, 2.533, 2.485, 2.590, 2.560, 2.571, 2.453, 2.501],
					[3.055, 2.934, 2.922, 2.919, 3.085, 3.099, 2.878, 2.932]],
				
				4: [[0, 15, 30, 45, 60],
				[2.974, 2.028, 1.979, 1.996, 1.970],
				[3.012, 2.971, 2.959, 2.958, 2.942]]}
				
	data[7.6] = {2 : [[0, 5, 10, 15, 20, 30, 45, 60],
					[1.486, 1.181, 1.122, 0.981, 0.868, 0.865, 0.860, 0.872],
					[1.470, 1.432, 1.435, 1.446, 1.402, 1.425, 1.423, 1.434]]}
					
	if run == "ALL":
		return data
	else:					
		return data[run]
		
def run_keys():
	data_key	= []
	
	for key in data_run("ALL"):
		data_key.append(str(key))
	return data_key
		
def run_key(run):
	data = {}		
	
	data[7.3]	= {'PURPOSE'	: 'To determine the initial leaching rates of Copper',
					'REAGENTS'	: 'Fe2SO4',
					'FE_CONC'	: 'Fe = 9.207 g/L',
					'ASSAY'		: 'FeCl3',
					'DAY'		: 'XX-Feb-2013',
					'START'		: '',
					'END'		: '',
					'RUNS'		: '2 g/L, 4 g/L'}
					
	data[7.4]	= {'PURPOSE'	: 'To determine the initial leaching rates of Copper',
					'REAGENTS'	: 'Fe2SO4',
					'FE_CONC'	: 'Fe = 9.207 g/L',
					'ASSAY'		: 'FeCl3',
					'DAY'		: 'XX-Feb-2013',
					'START'		: '',
					'END'		: '',
					'RUNS'		: '2 g/L, 4 g/L'}
