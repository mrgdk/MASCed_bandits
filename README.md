# MASCed_bandits

The MASCED_BANDITS framework is meant to be used for experimenting Muti-armed Bandit Algorithms. Currently, the framework supports the algorithms below:

    -> egreedy: (hyp: _float_ between 0-1)
    -> explore_commit: (hyp: _int_ up to ROUNDS (default 100))
    -> UCB: (hyp: string ("OG"))
    -> UCBImproved: (hyp: _string_ ("OG"))
    -> UCBNorm: (hyp: _string_ ("OG"))
    -> SWUCB: (hyp: _int_)
    -> DUCB: (hyp: _float_ between 0-1)
    -> EwS: –
    -> EXP3: (hyp: _float_ between 0-1)
    -> EXP3S: (hyp: _float_ between 0-1)
    -> EXP4: (hyp: _float_ between 0-1)

hyp == hyperparameter type for the associated bandit algorithm

Every bandit algorithm has it's own hyperparameter and the internal operations differ from algorithm to algorithm.


RUNNING AN ALGORITHM with USER SPECIFIED ARMS:

    In order to run a Multi-armed Bandit Algorithm, you will be interacting with "manual_case_generator.py" through the commandline interface.

    Inside MASCED_BANDITS directory, open a terminal and run the "manual_case_generator.py" with python by passing the requested algorithm name and associated hyperparameter listed above.

    Example Run:
    ---> python3 manual_case_generator.py '_BANDITNAME_' _hyperparameter_

    !!! The bandit name must be enclosed with quotation marks(because the framework expects a string).

    Once the program is executed, number of arms must be provided(_int_).
    Then, the corresponding arms should be created in each line in users preference.
    
    Before the program gets terminated, the run is saved in the "log.pkl" file and also, an associated log directory is created under records directory (Refer to OBSERVING RESULTS for more information).




CREATING ARMS:

    To create arms, distribution type along with the relevant parameters must be provided.
    For more information about the parameters, please refer to the hand guide for "python numpy.random" module.

    Example Arm Creation:
    ---> normal 100 10


OBSERVING RESULTS:

    Once the manual_case_generator completed the execution, a new enumerated log directory under the records folder is created for observation and analization purposes in human readable format.

    The newly created directory contains:
        -> a plot of arm selection per round,
        -> a plot of arm/count distribution per arm,
        -> a plot of generated rewards in each round,
        -> a gif dynamically demonstrating the reward change over rounds,
        -> a txt file which contains the relevant information about the corresponding execution(bandit name, hyperparameter–formula–, specified arms, seed, selection frequency of each arm, arm selection and reward distribution over rounds).



HOW TO GENERATE RESULTS:

    To generate test results, a new case should be added to the specified spot in "ResultGenerator.py". In "ResultGeneartor.py", a generator object has already been initialized, hence you do not need to create another generator object to generate a case!

    In order to generate a test result for any given configuration, you can simply follow the previously created test cases inside of "ResultGenerator.py" and change the run's configuration by changing the hyperparameters.

    !!ATTENTION!!

    If a change has been made inside of "ResultGenerator.py", even if you saved the "ResultGenerator.py", you must run "ResultGenerator.py" through the command line interface in order to save your test results.

    After the test results are created and ResultGenerator.py is run, the created results are saved inside of test_results.pkl file and they will be used as ground truth values later for testing purposes.


CREATING TEST CASES FOR ASSOCIATED TEST RESULTS:

    For testing purposes "test_mock.py", "TestController.py" and python unittest module are used. In order to test the framework, you should refer to "test_mock.py" where there exists predefined test_cases associated with the results generated in "ResultGenerator.py". 
    
    In order to create a new test case, you must generate a result first(Refer to HOW TO GENERATE RESULTS). After the result for a specified configuration is generated, an associated test case must be created inside of the "test_mock.py". The parameters which were used to generate the result for the given configuration must be identical with the parameters used to create the test case.

RUNNING THE TESTING FRAMEWORK:

    In order to run the testing framework following command must be used:
        "python3 -m unittest test_mock.py"

    After the command is executed, number of tests failed/passed will be listed.


    !!ATTENTION!!
    Before testing the framework, make sure to be inside of MASCED_BANDITS directory!

