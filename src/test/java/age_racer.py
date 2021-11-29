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
        individuals [0][i] = random.gauss(0,3000)

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
    command_line = 'cd /home/ingrid_amalie/Documents/Utveksling/Skoleressurser/Autumn/Algoritmos-genéticos-y-evolutivos-15755/Practices/FinalPractica/AGyE_final/ ; /usr/bin/env /usr/lib/jvm/java-12-openjdk-amd64/bin/java @/tmp/cp_97zas9182i9lux268kwj2eqfs.argfile SkeletonMain'
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
    result  = 0.0
    counter = np.empty([window_size]).astype(int)
    index_counter = 0
    iteration, index_counter = 0, 0
    best_iteration = 0

    # Start EE
    individuals, sigmas = init_experiment(rules_size)
    save_individual(individuals[0], files_config_path[0])
    os.system(command_line + args_array[0])
    result = fit_individual(files_result_path[0])

    try:
        while iteration < max_epochs:
            # Trace print
            print("********************")
            print("Epoch: ",  iteration)
            print("Ind: ", individuals[0])
            print("Sigm: ", sigmas)
            print(result)
            
            # Children generation and evaluation
            individuals[1] = generate_individual(individuals[0], sigmas)
            save_individual(individuals[1], files_config_path[1])
            os.system(command_line + args_array[1])
            new_result = fit_individual(files_result_path[1])

            # Better result update individual
            if new_result < result:
                print(individuals[1])
                individuals[0] = individuals[1]
                print("New result: ",  new_result)
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
                if improval < 1/5:
                    print("Improve")
                    row_data.append("Improve")
                    for i in range(rules_size):
                        sigmas[i] = sigmas[i] * c
                elif improval > 1/5:
                    print("Worsen")
                    row_data.append("Worsen")
                    for i in range(rules_size):
                        sigmas[i] = sigmas[i] / c
                else:
                    print ("Stable")
                    row_data.append("Stable")
            
            experiment.append(row_data)
            index_counter += 1
            iteration += 1

        # Saves iteration data in a csv file
        fm.save_to_csv(experiment, "exp_" + exp_number)
        
        # Saves a resume of experiment in solution file
        individual_sol = [ exp_number, rules_size, result, best_iteration, iteration, max_epochs, window_size, c ]
        fm.save_to_sol_csv(individual_sol, "solutions")

        save_individual(individuals[0], files_config_path[2])
    
    except (KeyboardInterrupt) as err:
        # Saves iteration data in a csv file
        fm.save_to_csv(experiment, "exp_" + exp_number)
        
        # Saves a resume of experiment in solution file
        individual_sol = [ exp_number, rules_size, result, best_iteration, iteration, max_epochs, window_size, c ]
        fm.save_to_sol_csv(individual_sol, "solutions")
        save_individual(individuals[0], files_config_path[2])