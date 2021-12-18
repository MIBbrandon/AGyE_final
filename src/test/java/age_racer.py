import os
import subprocess
import sys
import file_manager as fm
import numpy as np
import random
import json

PARAMETER_RANGES = (
(0.3, 1.2), (90, 110), (0.1, 5.0), (0.0001, 0.01), (1000, 3000), (400, 800), (0.1, 5.0), (0.0001, 0.01), (0, 400),
(150, 210))


def init_experiment(rules_size, load_init_individual: str = ''):
    if not load_init_individual:  # If string is empty
        # Initialize the first individual with its sigmas vector
        individuals = [[random.gauss(0, 3000) for _ in range(rules_size)] for _ in range(2)]
        sigmas = [150 - i for i in range(rules_size)]

        for i in range (len(individuals[0])):
            individuals[0][i] = min(PARAMETER_RANGES[i][1],individuals[0][i])
            individuals[0][i] = max(PARAMETER_RANGES[i][0],individuals[0][i])

    else:
        individual1, sigmas = get_individual(load_init_individual)
        individual2, _ = get_individual(load_init_individual)  # Será sobreescrito de todos modos
        individuals = [individual1, individual2]

    return individuals, sigmas


def get_individual(input_path):
    with open(input_path, "r") as input_fd:
        vals_line = input_fd.readline()
        sigma_line = input_fd.readline()
    vals = [float(x) for x in vals_line.split(', ')]
    sigma = [float(x) for x in sigma_line.split(', ')]
    return vals, sigma


def save_individual(individual, sigmas, output_path):
    with open(output_path, "w+") as output_fd:
        for i, val in enumerate(individual):
            output_fd.write(str(float(val)))
            if i != len(individual) - 1:
                output_fd.write(", ")
        output_fd.write("\n")
        for j, sd in enumerate(sigmas):
            output_fd.write(str(sd))
            if j != len(sigmas) - 1:
                output_fd.write(", ")


def fit_individual(result_path):
    with open(result_path, 'r') as agent:
        agentData = json.load(agent)

    fitness = sum(agentData['times'])
    return fitness


def generate_individual(individual, sigmas):
    assert len(individual) == len(sigmas)
    new_individual = []

    for i, (val, sd) in enumerate(zip(individual, sigmas)):
        obtained_value = random.gauss(val, sd)
        # We restrict the values to the limits
        obtained_value = min(PARAMETER_RANGES[i][1], obtained_value)
        obtained_value = max(obtained_value, PARAMETER_RANGES[i][0])
        new_individual.append(obtained_value)

    return new_individual


if __name__ == '__main__':

    try:
        # Experiment hyper-params
        max_epochs = int(sys.argv[1])
        window_size = int(sys.argv[2])
        c = float(sys.argv[3])
    except e:
        print("Call must be as follows: python3 age_racer.py <max_epochs> <window size> <c constant for 1/5 rule>")
        sys.exit(-1)

    # Gets experiment identifier number to store it
    exp_number = fm.get_experiment_number()

    # TODO Fit paths to each computer or if need other configs
    command_line = '/usr/bin/env /usr/lib/jvm/java-11-openjdk-amd64/bin/java @/tmp/cp_7c0lmj2jd1cq9jhk4phi5edyk.argfile SkeletonMain'
    cwd = '/home/cesar/Uni/AGE/e3/AGyE_final'

    # Files' paths
    rules_size = 10
    files_config_path = {
        'individuo': "./individuals_configurations/ag1.txt",
        'mejor': "./individuals_configurations/best_" + exp_number + ".txt"
    }
    files_result_path = {
        'individuo': "./experiments/ag1.json",
    }

    # Creates experiment log
    experiment = []
    experiment.append(["Iteration", "Best_result", "Window"])

    # Creates variables for EE loop
    result = 0.0
    counter = [0 for _ in range(window_size)]
    index_counter = 0
    iteration = 0
    best_iteration = 0

    # Start EE
    individuals, sigmas = init_experiment(rules_size)
    save_individual(individuals[0], sigmas, files_config_path['individuo'])
    #fm.set_agent_number(1)  
    s = subprocess.check_output(command_line, shell=True, cwd=cwd)
    result = fit_individual(files_result_path['individuo'])

    try:
        while iteration < max_epochs:
            # Children generation and evaluation
            individuals[1] = generate_individual(individuals[0], sigmas)
            save_individual(individuals[1], sigmas, files_config_path['individuo'])
            # fm.set_agent_number(2)
            s = subprocess.check_output(command_line, shell=True, cwd=cwd)
            new_result = fit_individual(files_result_path['individuo'])

            # Trace print
            print("********************")
            print("Epoch: ", iteration)
            print("Sigm: ", sigmas)
            print("Ind padre: ", individuals[0], "-->", result)
            print("Ind hijo: ", list(individuals[1]), "-->", new_result)

            # Better result update individual
            if new_result < result:
                print(individuals[1])
                individuals[0] = individuals[1]
                # Guardamos al hijo como si fuera el padre
                # save_individual(individuals[0], sigmas, files_config_path['padre'])
                print("New result: ", new_result)
                result = new_result
                best_iteration = iteration
                counter[index_counter % window_size] = 1
            else:
                counter[index_counter % window_size] = 0

            # Saves data line
            row_data = [iteration, result]

            # Sigma update
            if index_counter >= window_size:
                improval = np.average(counter)
                print(improval)
                if improval < 1 / 5:
                    print("Improve")
                    row_data.append("Improve")
                    for i in range(rules_size):
                        sigmas[i] = sigmas[i] * c
                elif improval > 1 / 5:
                    print("Worsen")
                    row_data.append("Worsen")
                    for i in range(rules_size):
                        sigmas[i] = sigmas[i] / c
                else:
                    print("Stable")
                    row_data.append("Stable")

            experiment.append(row_data)
            index_counter += 1
            iteration += 1

        # Saves iteration data in a csv file
        fm.save_to_csv(experiment, "exp_" + exp_number)

        # Saves a resume of experiment in solution file
        individual_sol = [exp_number, rules_size, result, best_iteration, iteration, max_epochs, window_size, c]
        fm.save_to_sol_csv(individual_sol, "solutions")

        save_individual(individuals[0], sigmas, files_config_path['mejor'])

    except KeyboardInterrupt as err:
        # Saves iteration data in a csv file
        fm.save_to_csv(experiment, "exp_" + exp_number)

        # Saves a resume of experiment in solution file
        individual_sol = [exp_number, rules_size, result, best_iteration, iteration, max_epochs, window_size, c]
        fm.save_to_sol_csv(individual_sol, "solutions")
        save_individual(individuals[0], sigmas, files_config_path['mejor'])