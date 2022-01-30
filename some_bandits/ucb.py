import numpy as np
import time
from random import sample
from utilities import save_to_pickle, load_from_pickle, truncate, convert_conf, calculate_utility
from bandit_options import bandit_args
from Bandit import Bandit



#formula = "ao"
FORMULA_FUNC = None

REWARD = 0
ACTION = 1



trace_len = 15000 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


initial_configuration = bandit_args["initial_configuration"]
class ucbC(Bandit):
    def __init__(self):
        self.formula = None
        self.arms = bandit_args['arms']
        self.knowledge = None
        if(bandit_args["knowledge"]):
            self.knowledge = bandit_args["knowledge"]
        else:
            bandit_args["knowledge"] = (-1, [], self.arms.index(initial_configuration))
            self.knowledge = bandit_args["knowledge"]
        
        
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        self.formula = self.formula_to_function(formula) #this shouldn't be done every time
        #print(dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula)
        #need an elegant way to handle the first read where knowledge doesn't exist yet 
      
        n_round = self.knowledge[0]
        self.game_list = self.knowledge[1]
        last_action = self.knowledge[2]
        #knowledge = (round, action_reward_pairs)


        if(self.arms[last_action] != (servers, dimmer)): 
            raise RuntimeError("Previously chosen configuration " + str(self.arms[last_action]) + " is not reflected in SWIM's " + str((servers,dimmer)))

        reward, is_bound_diff, bound_delta = calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers)

        if(is_bound_diff):
            #delta sigma (oldsum) vs sigma delta sum_i
            for game in self.game_list: game[REWARD] = game[REWARD] * bound_delta

        self.game_list.append([sum(reward)/len(reward), last_action])

        if((n_round + 1) < (len(self.arms))): #+1 because you are choosing the new action, which could be out of exploration range
            #initial exploration        
            n_round = n_round + 1

            new_knowledge = (n_round,self.game_list,n_round)  #the round just also happens to be the index of action since we go through it one by one
            #save_to_pickle(new_knowledge, 'ucb_knowledge')
            bandit_args['knowledge'] = new_knowledge

            if(bandit_args["record_decisions"]): 
                save_to_pickle(new_knowledge, "ucb_" + str(formula) + "_" + str(bandit_args["start_time"]))

            return convert_conf(self.arms[n_round], self.arms[last_action])
        else:
            n_round = n_round + 1

            new_action = self.choose_action(n_round)

            #don't really need to update the n_round anymore because we're out of initial exploration anyways
            new_knowledge = (n_round, self.game_list, new_action)
            #save_to_pickle(new_knowledge, "ucb_knowledge")
            bandit_args['knowledge'] = new_knowledge

            if(bandit_args["record_decisions"]): 
                save_to_pickle(new_knowledge, "ucb_" + str(formula) + "_" + str(bandit_args["start_time"]))

            return convert_conf(self.arms[new_action],self.arms[last_action])


    def choose_action(self, n_round):
        "Returns index in the pair list of the chosen action"
        best_arm = None
        best_value = -99999999 # - sys.maxsize perhaps (python3 is unbounded)

        for arm_index in range(len(self.arms)):
            current_value = self.reward_average(arm_index) + self.formula(arm_index, n_round)
            if(current_value > best_value):
                best_value = current_value
                best_arm = arm_index
        return best_arm

        #sqrt( (np.log(n)/n_k) * 0.25 * ( (2 * np.log(n))/n_k) ) )
    def formula_to_function(self, choice):
        funcs = {
                "FH": self.chapter7,
                "AO": self.asymptotically_optimal,
                "OG": self.auer2002UCB,
                "TN": self.tuned
            }
            
        func = funcs.get(choice)
        #print(func.__doc__)
        return func

    def reward_average(self, i):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == i): #the games in which i was the arm
                r_sum+=game[REWARD]
     
        times_i_played = self.times_played(i) 
        if(r_sum == 0 or times_i_played == 0): return 0
            
        return r_sum/times_i_played

    
    def sqreward_average(self, i):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == i): #the games in which i was the arm
                r_sum+=np.square(game[REWARD])

        times_i_played = self.times_played(i) 
        if(r_sum == 0 or times_i_played == 0): return 0
            
        return r_sum/times_i_played

    def times_played(self, i):
        return len([game for game in self.game_list if game[ACTION] == i])
       
        



    def chapter7(self, i, n):
        global DELTA

        upper_term = 2 * np.log( (1 / DELTA) )
        
        to_be_sqrt = upper_term/self.times_played(i)
        
        return np.sqrt(to_be_sqrt)

    def asymptotically_optimal(self, i, t):
        T_i = self.times_played(i)

        f_t = 1 + (t  * np.square(np.log(t)))

        upper_term = 2 * (np.log(f_t))

        lower_term =  T_i

        to_be_sqrt = upper_term/lower_term
        
        return np.sqrt(to_be_sqrt)

    def auer2002UCB(self, i, t):
        T_i = self.times_played(i)

        upper_term = 2 * (np.log(t))

        lower_term =  T_i

        to_be_sqrt = upper_term/lower_term
        
        return np.sqrt(to_be_sqrt)

    def tuned(self, i, n):
        n_k = self.times_played(i)

        average_of_squares = self.sqreward_average(i)
        square_of_average = np.square(self.reward_average(i))
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        V_k = estimated_variance + np.sqrt(2 * param)

        return np.sqrt(param * V_k)