import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args
from Bandit import Bandit



REWARD = 0
ACTION = 1
XI = 2


initial_configuration = bandit_args["initial_configuration"]
class SWUCBC(Bandit):
    def __init__(self):
        #self.look_back = 65
        self.arms = bandit_args["arms"]
        self.knowledge = None
        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
        else:
            bandit_args["knowledge"] = (-1, [], self.arms.index(initial_configuration))
            self.knowledge = bandit_args["knowledge"]

    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        self.look_back = int(formula)

        n_round = self.knowledge[0]
        game_list = self.knowledge[1]
        last_action = self.knowledge[2]

          
        if(self.arms[last_action] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(self.arms[last_action]) + " is not reflected in SWIM's " + str((servers,dimmer)))

        reward, is_bound_diff, bound_delta = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)

        if(is_bound_diff):
            #delta sigma (oldsum) vs sigma delta sum_i
            for game in game_list: game[REWARD] = game[REWARD] * bound_delta
        
        game_list.append([sum(reward)/len(reward), last_action]) #this represents the return of the evaluator() in definition.py and may need to be adjusted.
            
        if((n_round + 1) < (len(self.arms))): #+1 because you are choosing the new action, which could be out of exploration range
          
            n_round = n_round + 1

            new_knowledge = (n_round,game_list,n_round) #the round just also happens to be the index of action since we go through it one by one
            #save_to_pickle(new_knowledge, 'ucb_knowledge')
            bandit_args['knowledge'] = new_knowledge

            return convert_conf(self.arms[n_round], self.arms[last_action])
        else:
            #current_action = ARMS[action_index]
            if(self.arms[last_action] != (servers, dimmer)): 
                raise RuntimeError("Previously chosen configuration " + str(self.arms[last_action]) + " is not reflected in SWIM's " + str((servers,dimmer)))
        
            action_index = self.choose_action(game_list)


            new_knowledge = (n_round, game_list, action_index)

            bandit_args['knowledge'] = new_knowledge



            return convert_conf(self.arms[action_index],self.arms[last_action])



    def choose_action(self,game_list):
        best_arm = None
        best_value = -9999999

        for arm_index in range(len(self.arms)):
            current_value = self.X_t(arm_index,game_list) + self.c_t(arm_index, game_list)
            if(current_value > best_value):
                best_value = current_value
                best_arm = arm_index
        return best_arm

    def N_t(self, i, game_list):

        total_count = len(game_list) #t
        
        start_point = max(0, total_count-self.look_back+1)
        count = 0
        for game_index in range(start_point,total_count):
            if(game_list[game_index][1] == i): #I_s == i in other words arm of game equals given arm
                count += 1

        return count

    def X_t(self, i, game_list):
        total_count = len(game_list) #t
        summated = 0

        start_point = max(0, total_count-self.look_back+1)
        for game_index in range(start_point,total_count):
            current_game = game_list[game_index]
            if(current_game[1] == i): #the games in which i was the arm
                X_s = current_game[0]

                summated+=X_s

        try:
            times_i_played = self.N_t(i, game_list) 
            if(summated == 0 or times_i_played == 0): return 0
            
            return summated/self.N_t(i, game_list)
        except:
            print("Divide by zero error likely")
            print(game_list)
            print("Last tau games are")
            print(game_list[-self.look_back:])
            print("Length of game list is ")
            print(len(game_list))
            print("Result of N_t that was trigger is ")
            print(self.N_t(i, game_list))
            print("and the arm causing it was ")
            print(i)
            print("Value of summated is ")
            print(summated)
            exit(1)

        
    def c_t(self, i, game_list):

        t = len(game_list)
        
        t_or_tau = min(t,self.look_back)
        res = auer2002UCB(self.N_t(i, game_list), t_or_tau)

        return res
    

def asymptotically_optimal(n_k, t):
    
    T_i = n_k

    f_t = 1.0 + (t  * np.square(np.log(t)))

    upper_term = 2.0 * (np.log(f_t))

    lower_term =  T_i

    to_be_sqrt = upper_term/lower_term
    
    return np.sqrt(to_be_sqrt)

def chapter7(n_k, n):
    delta = 1.0 / np.square(n)

    upper_term = 2.0 * (np.log( (1.0 / delta) ))
    
    to_be_sqrt = upper_term/n_k
    
    return np.sqrt(to_be_sqrt)

def auer2002UCB(n_k, n):
    T_i = n_k

    upper_term = 2 * (np.log(n))

    lower_term =  T_i

    to_be_sqrt = upper_term/lower_term
    
    return np.sqrt(to_be_sqrt)