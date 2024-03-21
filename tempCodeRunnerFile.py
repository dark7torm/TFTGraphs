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

print(puuid_finder())