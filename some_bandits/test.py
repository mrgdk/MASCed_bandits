from Bandit import Bandit



def start(bandit,  dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
    if(isinstance(bandit,Bandit)):
        while(True):
            bandit.start_strategy(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula)

    

