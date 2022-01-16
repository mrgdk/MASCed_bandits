from persistent_data import bandit_args

def execute():
    initial_configuration = bandit_args["initial_configuration"]
    arms = bandit_args["arms"]

    if(bandit_args["knowledge"]):
        knowledge = bandit_args["knowledge"]
    else:
        action_reward_pairs = [ [arm, 0.0, 0.0] for arm in arms ] 
        bandit_args["knowledge"] = (0, action_reward_pairs, arms.index(initial_configuration))
        knowledge = bandit_args["knowledge"]

    n_round = knowledge[0]
    action_reward_pairs = knowledge[1]
    last_action = knowledge[2]

    n_round = n_round + 5

    bandit_args["knowledge"] = (n_round,action_reward_pairs, last_action)
    
    return str(bandit_args["knowledge"][0])

