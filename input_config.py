"""
    This function intended to collect necessary input from the user to initialize the arms.
"""
def get_configurations():
    try:
        num_of_arms = int(input("Please specify the number of arms you would like to create:\n"))
        arms_info = []
        for i in range(num_of_arms):
            arm = input("Please enter distribution type along with its parameters seperated by whitespaces:\n")
            arms_info.append(arm)
    except ValueError:
        print("Please make sure to enter numbers.\n")
    finally:
        return arms_info
