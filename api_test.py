import requests
import os
from tkinter import *
from tkinter import font
from collections import defaultdict
#import tweepy
# sets the api key as the environment variable in your computerjisung
# api_key = "insert api via developer.riotgames.com"
# twit_api_key =  os.environ["TWIT_API"]
# api_secret = os.environ["TWIT_API_SECRET"]
# bearer = os.environ["TWIT_BEARER"]
# access = os.environ["TWIT_ACCESS"]
# access_secret = os.environ["TWIT_ACCESS_SECRET"]
api_key = os.environ["RIOT_APP_API_KEY"]
# client = tweepy.Client(bearer, api_key, api_secret, access, access_secret)
# auth = tweepy.OAuth1UserHandler(api_key, api_secret, access, access_secret)
# api = tweepy.API(auth)
# ren id
test_id = "1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg"
# ren + jisung + sean + owen id
test_ids = ["1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg",
            "_Mgiig0pdFVXxA2btc4XjF_hVSOW16JzLhZiBZRi6LJdxt-QAZJD5fIY7sGcmKfIzJp37HjQggTR7A",
            "WnHv1ZvlirRiQ6dwX7U8YPuSSElqhbcBhI3QdXbfGh7-NVzPUhrSuUSecKfbk8khPiexI9KFyIS3DQ",
            "F9rgc1D5JAL9w71D8KCa-5z3z9swgTdQcis2-cMu3YZenOT66RjFm-AsDqqA7X1gpe7odktx4f8WwA"]

accountv1url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
tftaccounturl = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/"

# GUI window 
window = Tk()
window.state('zoomed')


# font
graphsFont = font.Font(family = "Helvetica", size=12, weight="bold")
def adjust_wrap(event):
    # Adjust wraplength to half the current width of the window for each label
    resultLabel1.config(wraplength=window.winfo_width() // 2)
    resultLabel2.config(wraplength=window.winfo_width() // 2)



def puuid_finder():
    """
    given name#tagline, returns puuid key
    """
    accountv1url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
    print("finding riotid")
    riotid = gameEntry.get() 
    # riotid = input("What is your Riot ID\n")
    parts = riotid.split('#')
    username = parts[0]
    tagline = parts[1] 
    accountv1url += username + "/" + tagline + "?api_key=" + api_key
    puuidresponse = requests.get(accountv1url)
    puuid = puuidresponse.json()['puuid']
    print(puuid)
    gameLabel.config(text = "How many games would you like to analyze your traits for")
    gameEntry.delete(0, len(riotid))
    history = match_history(puuid)
    gameButton.config(command = lambda: get_info(puuid), text = "Go")
    return puuid

def summoner_id_finder(puuid):
    """
    given puuid, returns summoner id
    """
    id_url = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/" + puuid + "?api_key=" + api_key
    response = requests.get(id_url)
    id = response.json()['id']

    return id

def username_finder(puuid):
    id_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/" + puuid + "?api_key=" + api_key
    response = requests.get(id_url)
    print(response.json())
    name = response.json()['gameName']
    return name

def list_username_finder(puuid_list):
    """
    given list of puuids, returns list of usernames
    """
    username_list = []

    for puuid in puuid_list:
        username_list.append(username_finder(puuid))
    return username_list

def list_username_finder(puuid_list):
    """
    given list of puuids, returns list of usernames
    """
    username_list = []

    for puuid in puuid_list:
        username_list.append(username_finder(puuid))
    return username_list

def rank_finder(puuid):
    """
    given puuid, returns rank and current LP
    """
    name = username_finder(puuid)
    summ_id = summoner_id_finder(puuid)
    tfturl = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/"
    tfturl += summ_id + "?api_key=" + api_key
    tftresponse = requests.get(tfturl)

# checks for empty response (unranked) otherwise returns the rank of the given user.
    if not tftresponse.json():
        return (name + "'s rank in TFT is Unranked")
    else : 
        return name + "'s rank in TFT is", tftresponse.json()[0]['tier'], tftresponse.json()[0]['rank'], tftresponse.json()[0]['leaguePoints'],"LP"

def match_history(puuid): 
    """
    Given puuid, returns match history up to inputted count
    """
    tftgamelisturl = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/'
    count = gameEntry.get()
    gameEntry.delete(0, len(count))
    tftgamelisturl += puuid + '/ids?start=0&' 'count=' +count + '&api_key=' + api_key
    gameresponse = requests.get(tftgamelisturl)

    print(gameresponse.json())
    
    return (gameresponse.json())

# given match id return info json
def match_info(match_id):
    info_url = "https://americas.api.riotgames.com/tft/match/v1/matches/"
    info_url += match_id
    info_url += "?api_key=" + api_key
    match_response_json = requests.get(info_url).json()
    return match_response_json

# given match info json return parsed information about the traits the user used
def get_traits(match_json, puuid):
    participant = {}
    try:
        participant = match_json['info']['participants']
    except KeyError:
        print(match_json)
    traits = []
    for participant in participant:
        if participant["puuid"] == puuid:
            info = participant["traits"]
            for trait in info:
                if trait["style"] > 0:
                    traits.append(trait["name"][6:])              
    return traits

def get_units(match_json, puuid):
    participant = {}
    try:
        participant = match_json['info']['participants']
    except KeyError:
        print(match_json)
    units = []
    for participant in participant:
        if participant["puuid"] == puuid:
            info = participant["units"]
            for trait in info:
                units.append(trait["character_id"][6:])
    return units

def get_placement(match_json, puuid): 
    participant = {}
    try:
        participant = match_json['info']['participants']
    except KeyError:
        print(match_json)
    units = []
    placement = 9
    for participant in participant:
        if participant["puuid"] == puuid:
            placement =  participant["placement"]
    return placement


def get_lastx_units(puuid):
    match_list = match_history(puuid)
    units_dict = dict()
    i = 1
    for match in match_list:
        if get_placement(match_info(match), puuid) < 5:
            for unit in get_units(match_info(match), puuid):
                if unit not in units_dict:
                    units_dict[unit] = 1
                else:
                    units_dict[unit] += 1
        i += 1
    resultLabel2.config(text=format_result(units_dict), wraplength=window.winfo_width() // 2)
    resultLabel2.grid(row=3, column=1, sticky="nsew")
    return units_dict

def get_lastx_traits(puuid):
    match_list = match_history(puuid)
    traits_dict = dict()
    i = 1
    for match in match_list:
        if get_placement(match_info(match), puuid) < 5:
            for trait in get_traits(match_info(match), puuid):
                if trait not in traits_dict:
                    traits_dict[trait] = 1
                else:
                    traits_dict[trait] += 1
        i += 1
    resultLabel1.config(text=format_result(traits_dict), wraplength=window.winfo_width() // 2)
    resultLabel1.grid(row=3, column=0, sticky="nsew")
    return traits_dict

def format_result(traits_dict):
    # Sorting the dictionary by count in descending order and by trait name in ascending order
    sorted_items = sorted(traits_dict.items(), key=lambda item: (-item[1], item[0]))
    
    # Grouping traits by count
    grouped = defaultdict(list)
    for trait, count in sorted_items:
        grouped[count].append(trait)

    # Formatting the grouped data into a single string
    formatted_list = "\n".join(f"{count}: {', '.join(sorted(traits))}" for count, traits in sorted(grouped.items(), reverse=True))
    print(formatted_list)
    return formatted_list

def get_info(puuid):
    get_lastx_traits(puuid)
    get_lastx_units(puuid)

            
def gui_init():
    window.title("TFTGraphs")
    width, height = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry('%dx%d+0+0' % (width,height))
    window.tk.call('tk', 'scaling', 3.0)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    global gameLabel, gameEntry, gameButton, resultLabel1, resultLabel2
    
    gameLabel = Label(window, text="What is your riot id", font=graphsFont)
    gameLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    gameEntry = Entry(width=50, font=graphsFont)
    gameEntry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    gameButton = Button(
        window,
        text="Find PUUID",
        width=10,
        height=3,
        command=puuid_finder,
        font=graphsFont,
        pady=5
    )
    gameButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    resultLabel1 = Label(window, wraplength=width//2, anchor='w', justify='left', font=graphsFont)
    resultLabel1.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

    resultLabel2 = Label(window, wraplength=width//2, anchor='w', justify='left', font=graphsFont)
    resultLabel2.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

    window.bind('<Configure>', adjust_wrap)
    print("gui initialized")
    window.mainloop()
# api_key = 'LzS1qwmphpoIFLR16TkESPaz4'
# api_secret = '2NZcMYcy6PyNP5kRa86KdMXMnXSOLvnSl228nxmtiBR5wsjr1i'
# bearer = 'AAAAAAAAAAAAAAAAAAAAAHHQtgEAAAAA1y8XSXH1dZdq1WNAwYTj0tL5%2FTI%3DNnU6spzmKUWCbGlGyQvQA9OpG2hJsXVdrbf7XdCsV3MTzNLxXO'
# access = '1788257350769422336-22LkKNNwWT15877MGXGCprvhzXHzXS'
# access_secret = 'c8EoSrODgO5sh6dTVpDefbu53Dg5t0JQaPngglbsKNbua'
def tweet_ranks():
    # print(twit_api_key, api_secret, bearer, access, access_secret)
    for puuid in test_ids:
        id = summoner_id_finder(puuid)
        client.create_tweet(text = rank_finder(puuid))
    
    

            



 
if __name__ == "__main__":
    """
    function testing. riot ids used. 
    """
    sean_id = "WnHv1ZvlirRiQ6dwX7U8YPuSSElqhbcBhI3QdXbfGh7-NVzPUhrSuUSecKfbk8khPiexI9KFyIS3DQ"
    ren_id =  "1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg"
    jisung_id =  "_Mgiig0pdFVXxA2btc4XjF_hVSOW16JzLhZiBZRi6LJdxt-QAZJD5fIY7sGcmKfIzJp37HjQggTR7A"

    # print(puuid_finder())

    # print(summoner_id_finder(puuid_finder()))

    # print(username_finder(puuid_finder()))

    # print(list_username_finder(test_ids))

    # print(rank_finder())

    # print(match_history(puuid_finder()))

    #NA1_4956815105 test match from ren
    match = "NA1_4956815105"
    gui_init()
    # tweet_ranks()
    

    
    # print(get_lastx_units(sean_id))
    # print(get_lastx_traits(test_id))
    # print(get_placement(match_info("NA1_4933244113"), test_id))
    # print(match_info(match))
    # print(get_traits(match_info(match), test_id))
    # print(get_units(match_info(match), test_id))
    # print(get_placement(match_info(match), test_id))
    # print(username_finder("1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg"))

