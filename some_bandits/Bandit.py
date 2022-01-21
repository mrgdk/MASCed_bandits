# Abstract interface for a execution strategy
#
# An execution strategy that forms the logic of the experiment.


class Bandit:
    def __init__(self):
        pass
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        """ starts execution """
        pass


