from utilities import *
RT_THRESH = 0.75
NUM_DIM_LEVELS = 5
DIMMER_STEP = 1.0 / (NUM_DIM_LEVELS - 1)

def execute(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate):
    print str(arrival_rate) + " " + str(dimmer) + " " + str(response_time) + " " + str(max_servers) + " " + str(servers)
    #print str(calculate_utility_notrunc(arrival_rate, dimmer, response_time, max_servers, servers)) + "\n"
    return ["do nothing"]
