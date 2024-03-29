import requests
import os
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

def puuid_finder():
    """
    given name#tagline, returns puuid key
    """
    accountv1url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
    riotid = input("What is your Riot ID\n")
    parts = riotid.split('#')
    username = parts[0]
    tagline = parts[1] 
    accountv1url += username + "/" + tagline + "?api_key=" + api_key
    puuidresponse = requests.get(accountv1url)
    puuid = puuidresponse.json()['puuid']

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
    count = input("How many games would you like to see?\n")
    tftgamelisturl += puuid + '/ids?start=0&' 'count=' +count + '&api_key=' + api_key
    gameresponse = requests.get(tftgamelisturl)
    
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
        print(match)
        if get_placement(match_info(match), puuid) < 5:
            for unit in get_units(match_info(match), puuid):
                if unit not in units_dict:
                    units_dict[unit] = 1
                else:
                    units_dict[unit] = units_dict[unit] + 1
            print(units_dict)
        print("Match", i, "placement", get_placement(match_info(match), puuid))
        i +=1
    return units_dict


            
            

            



 
if __name__ == "__main__":
    """
    function testing. riot ids used. 
    """
    #smadgehugers#4985
    #ren#icant
    #jisung#9462

    # print(puuid_finder())

    # print(summoner_id_finder(puuid_finder()))

    # print(username_finder(puuid_finder()))

    # print(list_username_finder(test_ids))

    # print(rank_finder())

    # print(match_history(puuid_finder()))

    #NA1_4956815105 test match from ren
    match = "NA1_4956815105"
    print(get_lastx_units(test_id))
    # print(get_placement(match_info("NA1_4933244113"), test_id))
    # print(match_info(match))
    # print(get_traits(match_info(match), test_id))
    # print(get_units(match_info(match), test_id))
    # print(get_placement(match_info(match), test_id))
    # print(username_finder("1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg"))

