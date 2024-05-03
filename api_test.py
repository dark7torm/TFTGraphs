import requests
import os
from tkinter import *
from tkinter import font
from collections import defaultdict
# sets the api key as the environment variable in your computerjisung
# api_key = "insert api via developer.riotgames.com"

api_key = os.environ["RIOT_APP_API_KEY"]
# ren id
test_id = "1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg"
# ren + jisung id
test_ids = ["1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg",
            "_Mgiig0pdFVXxA2btc4XjF_hVSOW16JzLhZiBZRi6LJdxt-QAZJD5fIY7sGcmKfIzJp37HjQggTR7A"]

accountv1url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
tftaccounturl = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/"

# GUI window 
window = Tk()
window.state('zoomed')


# font
graphsFont = font.Font(family = "Helvetica", size=12, weight="bold")
def adjust_wrap(event):
    # Adjust wraplength to the current width of the window
    resultLabel1.config(wraplength=window.winfo_width())
    resultLabel2.config(wraplength=window.winfo_width())



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
    gameButton.config(command = lambda: get_lastx_traits(puuid), text = "Go")
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
    id_url = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/" + puuid + "?api_key=" + api_key
    response = requests.get(id_url)
    name = response.json()['name']
    return name

def list_username_finder(puuid_list):
    """
    given list of puuids, returns list of usernames
    """
    username_list = []

    for puuid in puuid_list:
        username_list.append(username_finder(puuid))
    return username_list

def rank_finder():
    """
    given puuid, returns rank and current LP
    """
    puuid = puuid_finder()
    name = username_finder(puuid)
    summ_id = summoner_id_finder(puuid)

    return name

def list_username_finder(puuid_list):
    """
    given list of puuids, returns list of usernames
    """
    username_list = []

    for puuid in puuid_list:
        username_list.append(username_finder(puuid))
    return username_list

def rank_finder():
    """
    given puuid, returns rank and current LP
    """
    puuid = puuid_finder()
    name = username_finder(puuid)
    summ_id = summoner_id_finder(puuid)
    tfturl = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/"
    tfturl += summ_id + "?api_key=" + api_key
    tftresponse = requests.get(tfturl)

# checks for empty response (unranked) otherwise returns the rank of the given user.
    if not tftresponse.json():
        return (name + "'s rank in TFT is Unranked")
    else : 
        return print(name + "'s rank in TFT is",
                     tftresponse.json()[0]['tier'], 
                     tftresponse.json()[0]['rank'],
                     tftresponse.json()[0]['leaguePoints'],"LP")

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
    participant = match_json["info"]["participants"]
    traits = []
    for participant in participant:
        if participant["puuid"] == puuid:
            info = participant["traits"]
            for trait in info:
                if trait["style"] > 0:
                    traits.append(trait["name"][6:])              
    return traits

def get_units(match_json, puuid):
    participant = match_json["info"]["participants"]
    units = []
    for participant in participant:
        if participant["puuid"] == puuid:
            info = participant["units"]
            for trait in info:
                units.append(trait["character_id"][6:])
    return units

def get_placement(match_json, puuid): 
    if match_json["info"] != NONE:
        participant = match_json["info"]["participants"]
    
    units = []
    for participant in participant:
        if participant["puuid"] == puuid:
            placement =  participant["placement"]
    return placement


def get_lastx_units(puuid):
    match_list = match_history(puuid)
    units_dict = dict()
    i = 1
    for match in match_list:
        #print(match)
        if get_placement(match_info(match), puuid) < 5:
            for unit in get_units(match_info(match), puuid):
                if unit not in units_dict:
                    units_dict[unit] = 1
                else:
                    units_dict[unit] = units_dict[unit] + 1
            # print(units_dict)
        #print("Match", i, "placement", get_placement(match_info(match), puuid))
        i +=1
    return units_dict


def get_lastx_traits(puuid):
    match_list = match_history(puuid)
    traits_dict = dict()
    i = 1
    for match in match_list:
        # print(match)
        if get_placement(match_info(match), puuid) < 5:
            for trait in get_traits(match_info(match), puuid):
                if trait not in traits_dict:
                    traits_dict[trait] = 1
                else:
                    traits_dict[trait] = traits_dict[trait] + 1
                
            # print(units_dict)
        # print("Match", i, "placement", get_placement(match_info(match), puuid))
        i +=1
    resultLabel1.config(text = format_result(traits_dict), wraplength=780)
    resultLabel1.pack(expand=True, fill=BOTH)
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

            
def gui_init():
    
    
    window.title("TFTGraphs")
    width, height = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry('%dx%d+0+0' % (width,height))
    window.tk.call('tk', 'scaling', 3.0)
    global gameLabel, gameEntry, gameButton, resultLabel1, resultLabel2
    
    gameLabel = Label(window, text="What is your riot id", font=graphsFont)
    gameLabel.pack()
    gameEntry = Entry(width = 50, font=graphsFont)
    gameEntry.pack()

    gameButton = Button(
        window,
        text = "Find PUUID",
        width = 10,
        height = 3,
        command = puuid_finder,
        font=graphsFont
    )
    gameButton.pack()
    resultLabel1 = Label(window, wraplength=1000, width=1000, anchor='w', justify='left', font=graphsFont)
    resultLabel1.pack(fill='both', expand = True)

    resultLabel2 = Label(window, wraplength=1000, width=1000, anchor='w', justify='left', font=graphsFont)
    resultLabel2.pack(fill='both', expand = True)
    window.bind('<Configure>', adjust_wrap)
    print("gui initialized")
    window.mainloop()
    
    

            



 
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
    

    
    # print(get_lastx_units(sean_id))
    # print(get_lastx_traits(test_id))
    # print(get_placement(match_info("NA1_4933244113"), test_id))
    # print(match_info(match))
    # print(get_traits(match_info(match), test_id))
    # print(get_units(match_info(match), test_id))
    # print(get_placement(match_info(match), test_id))
    # print(username_finder("1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg"))

