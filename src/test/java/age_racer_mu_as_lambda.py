import os
import sys
import file_manager as fm
import numpy as np
import random
import json


def init_experiment(rules_size):
    # Initialize the first individual with its sigmas vector
    individuals = np.empty([2, rules_size])
    sigmas = np.empty([rules_size])

    # TODO fit numbers
    for i in range(rules_size):
        sigmas[i] = 150 - i
        individuals[0][i] = random.gauss(0, 3000)

    return individuals.astype(int), sigmas


def save_individual(individual, output_path):
    output_fd = open(output_path, "w+")
    for i in range(len(individual)):
        output_fd.write(str(individual[i]))
        if i != len(individual)-1:
            output_fd.write(", ")

    output_fd.close()


def fit_individual(result_path):
    agent = open(result_path)
    agentData = json.load(agent)

    fitness = np.sum(agentData['times'])
    return fitness


def generate_individual(individual, sigmas):
    length = len(sigmas)
    new_individual = np.empty([length])

    for i in range(length):
        new_individual[i] = random.gauss(0, sigmas[i]) + individual[i]

    return new_individual.astype(int)


if __name__ == '__main__':
    # Experiment hyper-params
    max_epochs = int(sys.argv[1])
    window_size = int(sys.argv[2])
    c = float(sys.argv[3])

    # Gets experiment identifier number to store it
    exp_number = fm.get_experiment_number()

    # TODO Fit paths to each computer or if need other configs
    command_line = ''
    args_array = [
        ' 1',
        ' 2'
    ]

    # Files' paths
    rules_size = 2
    files_config_path = [
        "./individuals_configurations/ag1.txt",
        "./individuals_configurations/ag2.txt",
        "./individuals_configurations/best_" + exp_number + ".txt"
    ]
    files_result_path = [
        "./experiments/ag1.json",
        "./experiments/ag2.json"
    ]

    # Creates experiment log
    experiment = []
    experiment.append(["Iteration", "Best_result", "Window"])

    # Creates variables for EE loop
    result = 0.0
    counter = np.empty([window_size]).astype(int)
    index_counter = 0
    iteration = 0
    best_iteration = 0
    lambda_ = 10
    population_size = 50
    # Selection variables
    size_torneo = 5
    size_family = 3
    # Mutation variables
    b = 1 # ?

    # Start EE

    # TODO: generate population
    individuals = [init_experiment() for _ in range(population_size)] # TODO: does this work?
    
    # TODO: connect strategy with java, and possibly save data

    try:
        while iteration < max_epochs:
            # Trace print
            print("********************")
            print("Epoch: ",  iteration)
            print("Ind: ", individuals[0])
            print("Sigm: ", sigmas)
            print(result)  # fitness

            # TODO: create lambda individuals and add them to the population

            # TODO: evaluate the entire population

            # TODO: sort the population by fitness

            # TODO: remove the lambda worst individuals from the population

            # TODO: save data about the generation

            # Saves data line
            row_data = [iteration, result]

            experiment.append(row_data)
            index_counter += 1
            iteration += 1

        # Saves iteration data in a csv file
        fm.save_to_csv(experiment, "exp_" + exp_number)

        # Saves a resume of experiment in solution file
        individual_sol = [exp_number, rules_size, result,
                          best_iteration, iteration, max_epochs, window_size, c]
        fm.save_to_sol_csv(individual_sol, "solutions")

        save_individual(individuals[0], files_config_path[2])

    except (KeyboardInterrupt) as err:
        # Saves iteration data in a csv file
        fm.save_to_csv(experiment, "exp_" + exp_number)

        # Saves a resume of experiment in solution file
        individual_sol = [exp_number, rules_size, result,
                          best_iteration, iteration, max_epochs, window_size, c]
        fm.save_to_sol_csv(individual_sol, "solutions")
        save_individual(individuals[0], files_config_path[2])
