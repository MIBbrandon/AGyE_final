import os
import subprocess
import sys
import file_manager as fm
import numpy as np
import random
import json

PARAMETER_RANGES = ((0.3, 1.2), (90, 110), (0.1, 5.0), (0.0001, 0.01), (1000, 3000), (400, 800), (0.1, 5.0), (0.0001, 0.01), (0, 400), (150, 210))

def init_experiment(rules_size, load_init_individual: str = ''):
    if not load_init_individual:  # If string is empty
        # Initialize the first individual with its sigmas vector
        individuals = np.empty([len(PARAMETER_RANGES), rules_size])
        sigmas = np.empty([rules_size])

        # TODO fit numbers
        for i in range(rules_size):
            sigmas[i] = 150 - i
            individuals[0][i] = round(random.gauss(0, 3000))
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
            if i != len(individual)-1:
                output_fd.write(", ")
        output_fd.write("\n")
        for j, sd in enumerate(sigmas):
            output_fd.write(str(sd))
            if j != len(sigmas) - 1:
                output_fd.write(", ")


def fit_individual(result_path):
    with open(result_path, 'r') as agent:
        agentData = json.load(agent)

    fitness = np.sum(agentData['times'])
    return fitness

def generate_individual(individual, sigmas):
    new_individual = np.empty([len(individual)])

    for i in range(len(individual)):
        obtained_value = random.gauss(individual[i], sigmas[i])
        # We restrict the values to the limits
        obtained_value = min(PARAMETER_RANGES[i][1], obtained_value)
        obtained_value = max(obtained_value, PARAMETER_RANGES[i][0])
        new_individual[i] = obtained_value

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
    command_line = ''
    cwd = '/home/brandon/git/AGyE_final'
    args_array = {
        'padre': '/run/user/1000/doc/2c94fd4c/jre1.8.0_311/bin/java -Dfile.encoding=UTF-8 -classpath /home/brandon/git/AGyE_final/target/test-classes:/home/brandon/git/AGyE_final/target/classes:/home/brandon/.m2/repository/com/codingame/gameengine/core/3.12.0/core-3.12.0.jar:/home/brandon/.m2/repository/com/google/inject/guice/4.0/guice-4.0.jar:/home/brandon/.m2/repository/javax/inject/javax.inject/1/javax.inject-1.jar:/home/brandon/.m2/repository/aopalliance/aopalliance/1.0/aopalliance-1.0.jar:/home/brandon/.m2/repository/com/google/guava/guava/23.0/guava-23.0.jar:/home/brandon/.m2/repository/com/google/code/findbugs/jsr305/1.3.9/jsr305-1.3.9.jar:/home/brandon/.m2/repository/com/google/errorprone/error_prone_annotations/2.0.18/error_prone_annotations-2.0.18.jar:/home/brandon/.m2/repository/com/google/j2objc/j2objc-annotations/1.1/j2objc-annotations-1.1.jar:/home/brandon/.m2/repository/org/codehaus/mojo/animal-sniffer-annotations/1.14/animal-sniffer-annotations-1.14.jar:/home/brandon/.m2/repository/com/google/code/gson/gson/2.8.2/gson-2.8.2.jar:/home/brandon/.m2/repository/commons-logging/commons-logging/1.2/commons-logging-1.2.jar:/home/brandon/.m2/repository/org/apache/logging/log4j/log4j-api/2.10.0/log4j-api-2.10.0.jar:/home/brandon/.m2/repository/org/apache/logging/log4j/log4j-core/2.10.0/log4j-core-2.10.0.jar:/home/brandon/.m2/repository/org/apache/logging/log4j/log4j-jcl/2.10.0/log4j-jcl-2.10.0.jar:/home/brandon/.m2/repository/com/codingame/gameengine/module-entities/3.12.0/module-entities-3.12.0.jar:/home/brandon/.m2/repository/com/codingame/gameengine/runner/3.12.0/runner-3.12.0.jar:/home/brandon/.m2/repository/io/undertow/undertow-core/2.0.25.Final/undertow-core-2.0.25.Final.jar:/home/brandon/.m2/repository/org/jboss/logging/jboss-logging/3.4.0.Final/jboss-logging-3.4.0.Final.jar:/home/brandon/.m2/repository/org/jboss/xnio/xnio-api/3.3.8.Final/xnio-api-3.3.8.Final.jar:/home/brandon/.m2/repository/org/jboss/xnio/xnio-nio/3.3.8.Final/xnio-nio-3.3.8.Final.jar:/home/brandon/.m2/repository/commons-io/commons-io/2.4/commons-io-2.4.jar:/home/brandon/.m2/repository/org/javassist/javassist/3.22.0-GA/javassist-3.22.0-GA.jar:/home/brandon/.m2/repository/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:/home/brandon/.m2/repository/org/yaml/snakeyaml/1.24/snakeyaml-1.24.jar:/home/brandon/.m2/repository/com/codingame/gameengine/module-tooltip/3.12.0/module-tooltip-3.12.0.jar:/home/brandon/.m2/repository/com/codingame/gameengine/module-endscreen/3.12.0/module-endscreen-3.12.0.jar SkeletonMain 1',
        'hijo': '/run/user/1000/doc/2c94fd4c/jre1.8.0_311/bin/java -Dfile.encoding=UTF-8 -classpath /home/brandon/git/AGyE_final/target/test-classes:/home/brandon/git/AGyE_final/target/classes:/home/brandon/.m2/repository/com/codingame/gameengine/core/3.12.0/core-3.12.0.jar:/home/brandon/.m2/repository/com/google/inject/guice/4.0/guice-4.0.jar:/home/brandon/.m2/repository/javax/inject/javax.inject/1/javax.inject-1.jar:/home/brandon/.m2/repository/aopalliance/aopalliance/1.0/aopalliance-1.0.jar:/home/brandon/.m2/repository/com/google/guava/guava/23.0/guava-23.0.jar:/home/brandon/.m2/repository/com/google/code/findbugs/jsr305/1.3.9/jsr305-1.3.9.jar:/home/brandon/.m2/repository/com/google/errorprone/error_prone_annotations/2.0.18/error_prone_annotations-2.0.18.jar:/home/brandon/.m2/repository/com/google/j2objc/j2objc-annotations/1.1/j2objc-annotations-1.1.jar:/home/brandon/.m2/repository/org/codehaus/mojo/animal-sniffer-annotations/1.14/animal-sniffer-annotations-1.14.jar:/home/brandon/.m2/repository/com/google/code/gson/gson/2.8.2/gson-2.8.2.jar:/home/brandon/.m2/repository/commons-logging/commons-logging/1.2/commons-logging-1.2.jar:/home/brandon/.m2/repository/org/apache/logging/log4j/log4j-api/2.10.0/log4j-api-2.10.0.jar:/home/brandon/.m2/repository/org/apache/logging/log4j/log4j-core/2.10.0/log4j-core-2.10.0.jar:/home/brandon/.m2/repository/org/apache/logging/log4j/log4j-jcl/2.10.0/log4j-jcl-2.10.0.jar:/home/brandon/.m2/repository/com/codingame/gameengine/module-entities/3.12.0/module-entities-3.12.0.jar:/home/brandon/.m2/repository/com/codingame/gameengine/runner/3.12.0/runner-3.12.0.jar:/home/brandon/.m2/repository/io/undertow/undertow-core/2.0.25.Final/undertow-core-2.0.25.Final.jar:/home/brandon/.m2/repository/org/jboss/logging/jboss-logging/3.4.0.Final/jboss-logging-3.4.0.Final.jar:/home/brandon/.m2/repository/org/jboss/xnio/xnio-api/3.3.8.Final/xnio-api-3.3.8.Final.jar:/home/brandon/.m2/repository/org/jboss/xnio/xnio-nio/3.3.8.Final/xnio-nio-3.3.8.Final.jar:/home/brandon/.m2/repository/commons-io/commons-io/2.4/commons-io-2.4.jar:/home/brandon/.m2/repository/org/javassist/javassist/3.22.0-GA/javassist-3.22.0-GA.jar:/home/brandon/.m2/repository/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:/home/brandon/.m2/repository/org/yaml/snakeyaml/1.24/snakeyaml-1.24.jar:/home/brandon/.m2/repository/com/codingame/gameengine/module-tooltip/3.12.0/module-tooltip-3.12.0.jar:/home/brandon/.m2/repository/com/codingame/gameengine/module-endscreen/3.12.0/module-endscreen-3.12.0.jar SkeletonMain 2'
    }

    # Files' paths
    rules_size = 3
    files_config_path = {
        'padre': "../../src/test/java/individuals_configurations/ag1.txt",
        'hijo': "../../src/test/java/individuals_configurations/ag2.txt",
        'mejor': "../../src/test/java/individuals_configurations/best_" + exp_number + ".txt"
    }
    files_result_path = {
        'padre': "../../src/test/java/experiments/ag1.json",
        'hijo': "../../src/test/java/experiments/ag2.json"
    }

    # Creates experiment log
    experiment = []
    experiment.append(["Iteration", "Best_result", "Window"])

    # Creates variables for EE loop
    result = 0.0
    counter = np.empty([window_size], dtype=int)
    index_counter = 0
    iteration = 0
    best_iteration = 0

    # Start EE
    individuals, sigmas = init_experiment(rules_size, files_config_path['padre'])
    save_individual(individuals[0], sigmas, files_config_path['padre'])
    # os.system(command_line + args_array['padre'])
    s = subprocess.check_output(args_array['padre'], shell=True, cwd=cwd)
    result = fit_individual(files_result_path['padre'])

    try:
        while iteration < max_epochs:
            # Children generation and evaluation
            individuals[1] = generate_individual(individuals[0], sigmas)
            save_individual(individuals[1], sigmas, files_config_path['hijo'])
            # os.system(command_line + args_array['hijo'])
            s = subprocess.check_output(args_array['hijo'], shell=True, cwd=cwd)
            new_result = fit_individual(files_result_path['hijo'])

            # Trace print
            print("********************")
            print("Epoch: ", iteration)
            print("Sigm: ", sigmas)
            print("Ind padre: ", individuals[0], "-->", result)
            print("Ind hijo: ", individuals[1], "-->", new_result)

            # Better result update individual
            if new_result < result:
                print(individuals[1])
                individuals[0] = individuals[1]
                # Guardamos al hijo como si fuera el padre
                save_individual(individuals[0], sigmas, files_config_path['padre'])
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
