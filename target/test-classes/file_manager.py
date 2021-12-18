import csv
import os


def save_to_csv(data_list, filename):
    # Primero creamos el directorio si no existe ya
    dir_path = 'csv_results/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, 0o777)
    # Create new and unique csv file and its writer
    with open(dir_path + filename + ".csv", "w", newline='') as csvfile:
        wr = csv.writer(csvfile, dialect='excel', delimiter=',')

        # Write each row from data_list in csv file
        for row in data_list:
            wr.writerow(row)


def save_to_sol_csv(row, filename):
    # Create new and unique csv file and its writer
    with open(filename + ".csv", "a", newline='') as csvfile:
        wr = csv.writer(csvfile, dialect='excel', delimiter=',')

        # Append the experiment final resume
        wr.writerow(row)


def get_experiment_number() -> str:
    filename = 'store.txt'

    # Get from store the experiment number
    with open(filename, 'r') as store:
        exp_number = int(store.readline())

    # Increase the experiment number for next experiments
    with open(filename, 'w') as store:
        store.write(str(exp_number + 1))

    # Return the experiment number
    return str(exp_number)

def set_agent_number(agent_number):
    filename = 'agentnumber.txt'

    # Sets agent number in file
    with open(filename, 'w') as store:
        store.write(str(agent_number))
