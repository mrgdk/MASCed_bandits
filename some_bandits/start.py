from mimetypes import init
from some_bandits.Bandit import Bandit
from some_bandits.utilities import convert_conf, RT_THRESH
from some_bandits.bandit_options import bandit_args

class Cleaner():
    def __init__(self):
        pass

    def clean(self, servers, dimmer):
        return convert_conf((5,0.0), (servers,dimmer))


#We take control over if the bandit is actually called by SWIM or if we clean
def start(bandit,  dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
    if(isinstance(bandit,Bandit)):
        print("\n-----Rounds so far-----")
        print("Cleaning rounds: " + str(bandit_args['round_counter'][0]))
        print("Bandit rounds  : " + str(bandit_args['round_counter'][1]))
        print("-----    End      -----\n")
        #print("this is the state of knowledge according to the meta script")
        #print(bandit_args["knowledge"])
        #print("endo of it")
        
        if(bandit_args['cleaning']):
            
            if(response_time > RT_THRESH): 
                bandit_args['round_counter'][0]+=1
                return "" #continue cleaning
            else:
                print("Cleaning is done -----\n")
                bandit_args['cleaning'] = False
                bandit_args['round_counter'][1]+=1
                x = convert_conf(bandit_args["stored_choice"],(5,0.0)) 
                print("Store choice: " + str(x))

                return x
        else:

            new_choice = bandit.start_strategy(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula)
        #["Add_Server", "Add_Server"]
            #print("Response time: " + str(response_time))
            if(response_time > RT_THRESH): #is the floor dirty
                #clean
                print("\nCleaning in progress -----")
                janitor = Cleaner()

                bandit_args['cleaning'] = True

                bandit_args["stored_choice"] = unconvert_conf(new_choice, [servers,dimmer])
                bandit_args['round_counter'][0]+=1
                return janitor.clean(servers,dimmer)
            else: #dont need to clean
                print("Cleaning was not necessary")
                bandit_args['round_counter'][1]+=1
                return new_choice

    #start_strategy: takes swim variables, returns swim tactics


def unconvert_conf(swim_commands, previous_config):
    new_arm = previous_config
    for command in swim_commands:
        if command == 'add_server':
            new_arm[0]+=1
        elif(command == 'remove_server'):
            new_arm[0]-=1
        elif('set_dimmer' in command ):
            new_arm[1] = float(command.split()[-1])

    return tuple(new_arm)
