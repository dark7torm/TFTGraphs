import requests
import os 
api_key = os.environ["RIOT_APP_API_KEY"]
champPerCost = [13, 13, 13, 12, 8]
# champPerCost = [13, 13, 13, 13, 8]
numberOfCost = [29, 22, 18, 12, 10] 

costProbs = [		              # level
  [1,    0,    0,    0,    0],    # 1
  [1,    0,    0,    0,    0],    # 2
  [0.75, 0.25, 0,    0,    0],    # 3
  [0.55, 0.30, 0.15, 0,    0],    # 4
  [0.45, 0.33, 0.20, 0.02, 0],    # 5
  [0.30, 0.40, 0.25, 0.05, 0],    # 6
  [0.19, 0.35, 0.35, 0.10, 0.01], # 7
  [0.18, 0.25, 0.36, 0.18, 0.03], # 8
  [0.10, 0.20, 0.25, 0.35, 0.10], # 9
  [0.05, 0.10, 0.20, 0.40, 0.25], # 10
  [0.01, 0.02, 0.12, 0.50, 0.35]  # 11
]



def calculateProbability(numleft, numCostLeft, levelProbability) :
    probability = levelProbability * (numleft / numCostLeft) * 5
    return probability


def getRemaining() :
    # prompt user for the data needed
    level = int(input("What is your level\n"))
    cost = int(input("What cost is your unit\n"))
    desireCount = int(input("How many of this unit do you want\n"))
    copies = int(input("How many copies are gone\n"))
    sameCost = int(input("How many units of the same cost are gone\n"))
    print(numberOfCost[cost - 1])
    # the number of copies of the unit you want, the total number of the individual unit - the copies already out
    desiredAvailable = numberOfCost[cost - 1] - copies
    # number of copies of all of the units with the same cost not including the one you want, 
    # number of champs in the cost - 1 (the unit you want) * number of each cost - number of units in the same cost gone
    sameCostAvailable = (champPerCost[cost] - 1) * numberOfCost[cost - 1] - sameCost
    percentage = calculateProbability(desiredAvailable, sameCostAvailable, costProbs[level - 1][cost - 1])
    print(desiredAvailable, sameCostAvailable, costProbs[level - 1][cost - 1])
    print("The percentage to hit your unit is ", percentage, "%")



getRemaining()
print("ren")