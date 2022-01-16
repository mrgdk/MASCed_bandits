import pickle
from bandit_options import bandit_args

OPT_REVENUE = 1.5
BASIC_REVENUE = 1
PRECISION = 10**(-5)
SERVER_COST = 10
RT_THRESH = 0.75
MAX_SERVICE_RATE = 1 / 0.4452713


def assign_utilityfunc():
	func =  {
        "SEAMS2017A": utilitySEAMS2017A,
        "SEAMS2017A_notrunc": utilitySEAMS2017A_notrunc,
        "SEAMS2022": utilitySEAMS2022
    }.get(bandit_args["utility_function"])

	return func
    
    
def say_hi(argument):
	print("Hello! I'm totally with new addition bandits and " + str(argument))
	return "this is the string I returned from say_hi"

def save_to_pickle(data_to_pkl, name):
	"""Takes any variable and a name for the pickle file and pickles it"""
	output = open(str(name) + '.pkl', 'ab+')
	pickle.dump(data_to_pkl, output)
	output.close()

def load_from_pickle(name):
	pkl_file = open(name + ".pkl", 'rb')
	data = pickle.load(pkl_file)
	pkl_file.close()
	return data

def pickle_test(data_to_pkl):
	print("pickling..")
	try:
		#read in data
		pkl_file = open('knowledge.pkl', 'rb')
		knowledge = pickle.load(pkl_file)
		print(knowledge)
		pkl_file.close()

		#adjust data
		knowledge = [item+1 for item in knowledge]
		output = open('knowledge.pkl', 'wb')
		pickle.dump(knowledge, output)
		output.close()
		return
	except IOError:
		#initial time
		initial_data = [0,0,0]
		output = open('knowledge.pkl', 'wb')
		pickle.dump(initial_data, output)
		output.close()
		return

def truncate(utility, bounds):
	lower_bound = bounds[0]
	upper_bound = bounds[1]

	x = utility

	if(x > upper_bound):
		x = upper_bound
	elif(x < lower_bound):
		x = lower_bound
	
	x = x + abs(lower_bound)
	result = float(x/(upper_bound + abs(lower_bound)))

	return result

def convert_conf(new_conf, current_conf):
	#if current (2, 1.0) and new pair is (3,1.0) return "add_server"

	if(new_conf == current_conf): return "do nothing"

	server_difference = new_conf[0] - current_conf[0]

	commands = ['add_server'] * server_difference

	if(not commands): commands = ["remove_server"] * abs(server_difference)

	if(new_conf[1] != current_conf[1]):
		commands.append("set_dimmer " + str(new_conf[1]))
	
	return commands

def utilitySEAMS2017A(arrival_rate, dimmer, avg_response_time, max_servers, servers):
	ur_opt = arrival_rate * OPT_REVENUE
	ur = arrival_rate * ((1-dimmer) * BASIC_REVENUE + (dimmer * OPT_REVENUE))
	#ur = arrival_rate * ( (1-dimmer) * BASIC_REVENUE + dimmer * OPT_REVENUE)
	
	bounds = bandit_args["bounds"]

	if((avg_response_time <= RT_THRESH) and (ur >= ur_opt - PRECISION)):
		uc = SERVER_COST * (max_servers - servers)
		return [truncate(ur + uc, bounds)]
	else:
		if(avg_response_time <= RT_THRESH):
			return [truncate(ur, bounds)]
		else:
			max_throughput = max_servers * MAX_SERVICE_RATE
			return [truncate(min(0, arrival_rate - max_throughput) * OPT_REVENUE, bounds)]

def utilitySEAMS2017A_notrunc(arrival_rate, dimmer, avg_response_time, max_servers, servers):
    ur_opt = arrival_rate * OPT_REVENUE
    ur = arrival_rate * ((1 - dimmer) * BASIC_REVENUE + dimmer * OPT_REVENUE)
    if (avg_response_time <= RT_THRESH) and (ur >= ur_opt - PRECISION):
        uc = SERVER_COST * (max_servers - servers)
        return ur + uc
    else:
        if avg_response_time <= RT_THRESH:
            return ur
        else:
            max_throughput = max_servers * MAX_SERVICE_RATE
            return min(0, arrival_rate - max_throughput) * OPT_REVENUE

def utilitySEAMS2022(arrival_rate, dimmer, avg_response_time, max_servers, servers):
	ur_opt = arrival_rate * OPT_REVENUE
	ur = arrival_rate * ((1 - dimmer) * BASIC_REVENUE + dimmer * OPT_REVENUE)
	uc = SERVER_COST * (max_servers - servers)
	urt = 1 - ((avg_response_time-RT_THRESH)/RT_THRESH)

	bounds = bandit_args["bounds"]
	
	revenue_weight = 0.7
	server_weight = 0.3
	utility = urt*((revenue_weight*ur)+(server_weight*uc))
	
	return [truncate(utility, bounds)]
   

calculate_utility = assign_utilityfunc()
