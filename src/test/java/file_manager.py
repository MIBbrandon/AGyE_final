from typing import Tuple
from numpy import random
import datetime as dt
import csv
import json

def save_to_csv(data_list, filename):
    # Create new and unique csv file and its writer
    csvfile = open("csv_results/" + filename + ".csv", "w", newline='')
    wr = csv.writer(csvfile, dialect='excel', delimiter=',')
    
    # Write each row from data_list in csv file
    for row in data_list:
        wr.writerow(row)

    # Close csv file
    csvfile.close()

def save_to_sol_csv(row, filename):
    # Create new and unique csv file and its writer
    csvfile = open(filename + ".csv", "a", newline='')
    wr = csv.writer(csvfile, dialect='excel', delimiter=',')
    
    # Append the experiment final resume
    wr.writerow(row)

    # Close csv file
    csvfile.close()

def get_experiment_number() -> str:
    filename = 'store.txt'
    
    # Get from store the experiment number
    store = open(filename, 'r')
    exp_number = int(store.readline())
    store.close()

    # Increase the experiment number for next experiments
    store = open(filename, 'w')
    store.write(str(exp_number + 1))
    store.close()

    # Return the experiment number
    return str(exp_number)
