import numpy as np
from random import sample
from Expert import Expert
from Bandit import Bandit
from bandit_options import bandit_args
from utilities import calculate_utility, convert_conf
from EXP3 import EXP3C
ACTION = 0
REWARD = 1
N_K = 2

#ETA = 1

ETA = None
class exp4C(Bandit):
    def __init__(self):
        self.arms = bandit_args["arms"]
        self.num_exps = bandit_args["number_of_experts"]
        
        self.expert = self.expert_to_class(bandit_args["expert"])

        self.distribution = None
        

        self.experts = []

        self.knowledge = None


        if(bandit_args["knowledge"]):
            print("initialized and grabbing prev knowledge")
            self.knowledge = bandit_args["knowledge"]
        else:
            initial_configuration = bandit_args["initial_configuration"]
            self.distribution = [1.0/self.num_exps] * self.num_exps
    
            print("distribution in initialization")
            print(self.distribution)
            for i in range(self.num_exps):
                exp_instance = self.expert()
                exp_instance.set_functions("FH")
                exp_instance.distr_func(exp_instance.distribution, exp_instance.weights, exp_instance.eta)
                self.experts.append(exp_instance)
            
            bandit_args["knowledge"] = (self.arms.index(initial_configuration), self.distribution, self.experts, 0)
            self.knowledge = bandit_args["knowledge"]
    
    def start_strategy(self, dimmer, response_time, activeServers, servers, max_servers, total_util, arrival_rate, formula):
        
        #print("begin strategy")
        
        #print("old knowledge")
        #print(self.knowledge)

        self.distribution = []
        self.experts = []


        current_action_i = self.knowledge[0]
        self.distribution.extend(self.knowledge[1])
        self.experts.extend(self.knowledge[2])
        previous_expert_chosen = self.knowledge[3]
        #print("distribution at beginning of start_strategy")
        #print(self.distribution)



        #self.expert_status()

        results = []

        results.extend(calculate_utility(arrival_rate, dimmer, response_time, max_servers, servers))

        reward = sum(results)

        #print("reward received")
        #print(reward)
        gamma = 0 #temporary

        E_t = np.matrix([expert.distribution for expert in self.experts])
        EtQt =self.distribution * E_t

        P_t = list(np.array(EtQt).flatten())
        #X^_ti = 1 - I {At = i}/P_ti + gamma (1 - reward)
        #print("pt is ")
        #print(P_t)
        Xhat = []
        for i in range(len(self.arms)):
            x = 1 - ( (1 if self.arms[i] == self.arms[current_action_i] else 0) /P_t[i] + gamma) * (1 - reward)
            Xhat.append(x)
        
        #print("xhat is ")
        #print(Xhat)

        Xtilde = list(np.array(np.matmul(E_t,Xhat)).flatten())
   
        

        self.experts[previous_expert_chosen].propagate_reward(reward, current_action_i)

        ETA = 0.0359 #sqrt(2log(num_exp) / (num_arms * total_rounds))
        #print("xtilde")
        #print(Xtilde)




        oldQ_sum = sum([ np.exp(ETA * Xtilde[j])* self.distribution[j] for j in range(self.num_exps)])
        #print("denom_sum")
        #print(oldQ_sum)
        for odd_index, expert_odd in enumerate(self.distribution):
            etabyx = np.exp(ETA * Xtilde[odd_index])
            #print("etabyx")
            #print(etabyx)
            #print("dist before")
            #print(self.distribution)
            #print("first elem")
            #print((ETA * Xtilde[0]))
            #print("second elem")
            #print(np.exp(ETA * Xtilde[0]))
            #print("third elem")
            #print((np.exp(ETA * Xtilde[0])) * self.distribution[0])

            

            self.distribution[odd_index] = ((etabyx * expert_odd) / oldQ_sum)
            #print("dist after")
            #print(self.distribution)

        #print("arguments for random_choice ")
        #print( (np.arange(0, self.num_exps), self.distribution))
        expert_choice = np.random.choice(np.arange(0, self.num_exps), p= self.distribution) #choose the first expert
        #print("expert chosen is ")
        #print(expert_choice)

        chosen_action = self.experts[expert_choice].sample_action()  #get action from that expert

        #print("action from expert ")
        #print(chosen_action)

        #self.expert_status()
        new_knowledge = (chosen_action, self.distribution, self.experts, expert_choice)
        #print("new knowledge")
        #print(new_knowledge)
        bandit_args['knowledge'] = new_knowledge

        #print("end strategy")
        return convert_conf(self.arms[chosen_action],self.arms[current_action_i])
    
    def expert_to_class(self, choice):
        funcs = {
                "EXP3C": EXP3C
            }
            
        func = funcs.get(choice)
        ##print(func.__doc__)
        return func

    def expert_status(self):
        for expert in self.experts:
            print("-----EXPERT-----")
            print('Distribution: ' + str(expert.distribution))
            print('Weights: ' + str(expert.weights))
            print("-----END EXPERT---")


