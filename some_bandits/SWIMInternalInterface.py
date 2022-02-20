
from some_bandits.bandits.Bandit import Bandit
from some_bandits.utilities import convert_conf, RT_THRESH, calculate_utility, save_to_pickle
from some_bandits.bandit_options import bandit_args
from some_bandits.bandits import init_bandit

class Cleaner():
    def __init__(self):
        pass

    def clean(self, servers, dimmer):
        return convert_conf((3,0.0), (servers,dimmer))



def print_bounds():
    print("bounds are \n")
    print(bandit_args["bounds"])
    print("bounds done\n")

def print_rounds():
    print("\n-----Rounds so far-----")
    print("Cleaning rounds: " + str(bandit_args['round_counter'][0]))
    print("Bandit rounds  : " + str(bandit_args['round_counter'][1]))
    print("-----    End      -----\n")


bandit_args["arms"] = [(1,1.0), (2,1.0), (3,1.0)]
bandit_args["initial_configuration"] = (1,1.0)

#We take control over if the bandit is actually called by SWIM or if we clean
def start(bandit_name,  dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
    if(bandit_args["bandit_instance"]):
        bandit = bandit_args["bandit_instance"]

        if(isinstance(bandit, Bandit)):
            print_rounds()
            print_bounds()

           
            if(bandit_args['cleaning']):
                
                if(response_time > RT_THRESH): 
                    bandit_args['round_counter'][0]+=1
                    return "" #continue cleaning
                else:
                    print("Cleaning is done -----\n")
                    bandit_args['cleaning'] = False
                    bandit_args['round_counter'][1]+=1
                    x = convert_conf(bandit_args["stored_choice"],(3,0.0)) 
                    print("Store choice: " + str(x))

                    return x
            else:
    #NEED TO CONVERT CONF HERE NOW!
                reward, is_bound_diff, bound_delta = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)
            
                if(is_bound_diff and isInstance(bandit, ucbC) and bandit_args["dynamic_bounds"]):
                #delta sigma (oldsum) vs sigma delta sum_i
                    for game in bandit.game_list: game[REWARD] = game[REWARD] * bound_delta

                print("last action is ")
                print(bandit.last_action)
                print("\n\n\n")
                if(bandit.last_action != (servers, dimmer)): 
                    raise RuntimeError("Previously chosen configuration " + str(bandit.last_action) + " is not reflected in SWIM's" + str((servers,dimmer)))
               
                new_choice = bandit.start_strategy(reward[0])
                #print("new choice is " + str(new_choice))

                if(response_time > RT_THRESH): #is the floor dirty
                    #clean
                    print("\nCleaning in progress -----")
                    janitor = Cleaner()

                    bandit_args['cleaning'] = True

                    bandit_args["stored_choice"] = new_choice
                    bandit_args['round_counter'][0]+=1
                    return janitor.clean(servers,dimmer)
                else: #dont need to clean
                    print("Cleaning was not necessary")
                    bandit_args['round_counter'][1]+=1
                    if(bandit_args["record_decisions"]): 
                        save_to_pickle(bandit, bandit.name + str(formula) + "_" + str(bandit_args["start_time"]))
                    converted =  convert_conf(new_choice, (servers,dimmer))
                    print("converted is " + str(converted))
                    return converted
    else:
        print("first this")
        bandit_args["bandit_instance"] = init_bandit(bandit_name,formula)
        return start(bandit_name,  dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula)

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
