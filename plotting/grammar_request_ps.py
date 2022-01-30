from lark import Lark
import sys
from sys import exit
import random

traffic_grammar = """

    start: base traffic_type*
        
    traffic_type: (steady | change | noisy)  
    base: "base(" REQUEST_PER_S "," LENGTH ")" 

    steady: "traffic_steady(" LENGTH ")"
    noisy: "traffic_noisy(" DEVIATIONRANGE "," LENGTH ")"
    change: "traffic_change(" REQUEST_PER_S "," LENGTH ")" 

    REQUEST_PER_S: INT
    LENGTH: INT
    DEVIATIONRANGE: UNIT 

    UNIT: "0" "." INT | "1" "." "0" | "1" | "0"     
    %import common.INT

    %import common.WS
    %ignore WS
"""
#this assumes times are specified
def traffic_transition(start, end, length, trace_list):
    x = start

    END_POINT = start 
    #y
    
    
    #0.5 * n_steps * (start + end) == length

    factor = (start+end) * 0.5 

    n_steps = int(length / factor)
    #inc = difference / n_steps
    inc = abs(start-end) / n_steps
    
    if(end < start): inc = -inc

    for i in range(n_steps):
        x+= inc
        trace_list.append(x)


def run_instruction(t, trace_list):
    if(t.data == "base"):
        request, length = t.children

        request = 1/float(request)
        
        n_times = int(int(length) / float(request))
        trace_list.extend([float(request)] * n_times)
    elif(t.data == "steady"):
        length = int(t.children[0])

        previous_level = trace_list[-1]

        n_times = int(int(length) / previous_level)


        trace_list.extend([previous_level] * n_times)

    elif(t.data == "change"):
        request, length = t.children

        previous_level = trace_list[-1]
        traffic_transition(previous_level,1/float(request),int(length),trace_list)
    elif(t.data == "noisy"):
        deviation_factor, length = t.children
        deviation_factor = float(deviation_factor)
        previous_level = trace_list[-1]

        n_times = int(int(length) / previous_level)

        previous_abs = 1/previous_level
        print("previous abs is ")
        print(previous_abs)


        absolute_deviation = previous_abs * deviation_factor

        print("dev is ")
        print(absolute_deviation)


        lower_bound = 1/(previous_abs - absolute_deviation)
        upper_bound = 1/(previous_abs + absolute_deviation)
        budget = int(length)

        difference = lower_bound - upper_bound #backwards because that's how the arrival rate works

        low = 99999
        high = -99999

        noisy_list = []
        mini_budget = 60
        while(budget > previous_level): #until (0 + the last traffic) 
            random_traffic = (random.random() * difference) + upper_bound
            
            abs_random = 1/random_traffic
            if(abs_random < low): low = abs_random
            if(abs_random > high): high = abs_random
        
            n_of_noise = round(mini_budget / random_traffic)
            noisy_list.extend([random_traffic] * n_of_noise)
            budget-=mini_budget

            #noisy_list.append(random_traffic)
            #budget-=random_traffic

        print("low is ")
        print(low)
        print("high is ")
        print(high)



        trace_list.extend(noisy_list)
        trace_list.append(previous_level) #for consistency the final traffic is always not deviated

    elif(t.data == "traffic_type"):
        run_instruction(t.children[0], trace_list)



    else:
        raise SyntaxError('Unknown instruction: %s' % t.data)

help = " Expects two args, <source_code_file> <trace_name> \n  \
    e.g. ./generate_trace smoothincrease.txt smoothincreasetrace "


if(len(sys.argv) != 3): 
    print("Unexpected usage") 
    print(help)
    exit(1)

if("-h" in sys.argv or "--help" in sys.argv): 
    print(help)
    exit(0)
parser = Lark(traffic_grammar)

try:
    with open(sys.argv[1], 'r') as source:
        source_code = source.read()
except IOError:
    print('Something is wrong with the source code file')

try:
    parse_tree = parser.parse(source_code)
except Exception as e:
    print("Syntax error, details below: \n")
    print(e)
    exit(1)

trace = [] #list of floats representing the traffic


for inst in parse_tree.children:
    run_instruction(inst, trace)


f = open(str(sys.argv[2]) + ".delta", "w")

[f.write(str(req) + "\n") for req in trace]

f.close()

print("Total trace length is " + str(sum(trace)) + "s ")