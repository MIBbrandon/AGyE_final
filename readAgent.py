import json
import numpy as np

def fitness(AgentData):

    #TODO: DETERMINE WICH ROW HAS TO BE THE PARAMETER

    AgentData = np.where(AgentData < 0, 0, AgentData)

    return np.sum(AgentData[1,:])

def get_json_max(JSONdata):

    max = 0

    for i in JSONdata:
        if len(JSONdata[i]) > max: max = len(JSONdata[i])

    return max

def read_agent(JSONFile):

    try:
        #The JSON data is read
        agent = open(JSONFile)
        agentData = json.load(agent)

        #The JSON data is stored into an array
            #We are assuming that all the data in the JSON is
            #the same type
            #TODO: EDIT ACCORDING TO THE ACTUAL JSON

        #We use the function get_json_max to keep the code clean as
        #it is just finding the largest row in the JSON
        max = get_json_max(agentData)

        #The tile value is '-1' to make it eassier to ignore further
        #down the line
        output = np.tile(-1,[len(agentData),max])

        #As the tuple is stored within the i variable
        #we declare an auxiliary variable to store
        #the vector's index
        aux = 0

        for i in agentData:

            output[aux,0:len(agentData[i])] = agentData[i]
            aux += 1


        agent.close()

        return output

    except OSError as e:
        print(e)


if __name__ == '__main__':

    print("This main class is only meant to be used as a test.\nTest result:")

    example = read_agent("JSONExample.json")

    for i in example:
        print(i)

    print(str(fitness(example)))