

import time
import json

def checkCapacity(contents,knapsack_cap):
    """ contents is expected as a dictionaryof the form {item_id:(volume,value), ...} """
    """ This function returns True if the knapsack is within capacity; False if the knapsack is overloaded """
    load = 0
    if isinstance(contents,dict):
        for this_key in contents.keys():
            load = load + contents[this_key][0]
        if load <= knapsack_cap:
            return True
        else:
            return False
    else:
        print("function checkCapacity() requires a dictionary")

def knapsack_value(items):
    value = 0.0
    if isinstance(items,dict):
        for this_key in items.keys():
            value = value + items[this_key][1]
        return(value)
    else:
        print("function knapsack_value() requires a dictionary")

def getData():
    f = open('/Users/gracechi/Desktop/knapsack.json','r')
    x = json.load(f)
    f.close()
    for i in range(len(x)):
        myData = x[i]['data']
        x[i]['data'] = {}
        for j in range(len(myData)):
            x[i]['data'][j] = tuple(myData[j]) 
    return x
knapsack = getData()

def loadKnapsack(items,knapsack_cap):
    """ You write this function which is your heuristic knapsack algorithm 
        Indicate items to be included in the backpack by including their dictionary keys within 
        a list data structure and, subsequently, returning that list of IDs from this function  """
    """ Compute existing load in knapsack """
    myUsername = '' # always return this variable as the first item
    nickname = '' # This idenfier will appear on the leaderboard, if you desire to be identified.  This may be left as an empty string.
    items_to_pack = []    # use this list for the indices of the items you load into the knapsack
    n = len(items)        # Number of items in the dictionary
    cap = int(knapsack_cap)
    load = 0.0            # use this variable to keep track of how much volume is already loaded into the backpack
    #value = 0.0           # value in knapsack
    item_list = []        # list of items to potentially use
    result = 0
    table = []
    
    #item_load = [int(l) for k,(l,v) in items.items()] # get all weights
    #item_val = [int(v) for k,(l,v) in items.items()] # get all values
    item_load = []
    item_val = []
    
    for v in items:
        item_load.append(int(items[v][0]))
        item_val.append(int(items[v][1]))
        
    table = [[0 for a in range(int(knapsack_cap)+1)] for i in range(n+1)] #Creates a table for memoization
    
    #loops through and fills table
    for i in range(n+1):
        for x in range(int(knapsack_cap)+1):
            if i==0 or x == 0:
                table[i][x] = 0
            elif item_load[i-1] <= x:
                table[i][x] = max(item_val[i-1] + table[i-1][x-item_load[i-1]], table[i-1][x])
            else:
                table[i][x] = table[i-1][x]

    result = table[n][int(knapsack_cap)]
    #print(table)
    for a in range(n, 0, -1):
        if result <= 0:
            break
        if result == table[a-1][cap]:
            continue
        else:
            item_list.append((item_load[a-1], item_val[a-1]))
            load += item_load[a-1]
            result -= item_val[a-1]
            cap -= item_load[a-1]
            
    for search in item_list:
        for key,value in items.items():
            if value == search:
                items_to_pack.append(key)
    #print(result)   
    #print("Items Packed: " + str(items_to_pack))   
    return myUsername, nickname, items_to_pack       # use this return statement when you have items to load in the knapsack
""" Main code """
""" Get data and define problem ids """
probData = getData()
problems = range(len(probData))
silent_mode = False    # use this variable to turn on/off appropriate messaging depending on student or instructor use
""" Error Messages """
error_bad_list_key = """ 
A list was received from load_knapsack() for the item numbers to be loaded into the knapsack.  However, that list contained an element that was not a key in the dictionary of the items that were not yet loaded.   This could be either because the element was non-numeric, it was a key that was already loaded into the knapsack, or it was a numeric value that didn't match with any of the dictionary keys. Please check the list that your load_knapsack function is returning. It will be assumed that the knapsack is fully loaded with any items that may have already been loaded and a score computed accordingly. 
"""
error_response_not_list = """
load_knapsack() returned a response for items to be packed that was not a list.  Scoring will be terminated   """

for problem_id in problems:
    in_knapsack = {}
    knapsack_cap = probData[problem_id]['cap']
    items = probData[problem_id]['data']
    errors = False
    response = None
    
    startTime = time.time()
    team_num, nickname, response = loadKnapsack(items,knapsack_cap)
    execTime = time.time() - startTime
    if isinstance(response,list):
        for this_key in response:
            if this_key in items.keys():
                in_knapsack[this_key] = items[this_key]
                del items[this_key]
            else:
                errors = True
                if silent_mode:
                    status = "bad_list_key"
                else:
                    print("P"+str(problem_id)+"bad_key_")
                #finished = True
    else:
        if silent_mode:
            status = "P"+str(problem_id)+"_not_list_"
        else:
            print(error_response_not_list)
                
    if errors == False:
        if silent_mode:
            status = "P"+str(problem_id)+"knap_load_"
        else:
            print("Knapsack Loaded for Problem ", str(problem_id)," ....", '    Execution time: ', execTime, ' seconds')
        knapsack_ok = checkCapacity(in_knapsack,knapsack_cap)
        knapsack_result = knapsack_value(in_knapsack)
        if silent_mode:
            print(status+"; knapsack within capacity: "+knapsack_ok)
        else:
            print("knapcap: ", knapsack_ok)
            print("knapsack value : ", knapsack_value(in_knapsack))
            