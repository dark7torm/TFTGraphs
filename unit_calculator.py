import requests
import os 
api_key = os.environ["RIOT_APP_API_KEY"]

num1Cost = 29
num2Cost = 22
num3Cost = 18
num4Cost = 12
num5Cost = 10

# prompt user for the data needed
level = input("What is your level\n")
cost = input("What cost is your unit\n")
current = input("How many of this unit do you want\n")
copies = input("How many copies are gone\n")
sameCost = input("How many units of the same cost are gone\n")
gold = input("How much gold to roll down")


def getRemaining() :
    match cost:
        case 1:
            available = num1Cost - current
        case 2:
            available = num2Cost - current
        case 3:
            available = num3Cost - current
        case 4:
            available = num4Cost - current
        case 5:
            available = num5Cost - current
        case _:
            print("Invalid unit cost")