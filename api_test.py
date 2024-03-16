import requests
import os
# sets the api key as the environment variable in your computer
# api_key = "insert api via developer.riotgames.com"
api_key = os.environ["RIOT_APP_API_KEY"]


accountv1url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
tftaccounturl = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/"
riotid = input("What is your Riot ID\n")
parts = riotid.split('#')
username = parts[0]
tagline = parts[1] 
accountv1url += username + "/" + tagline + "?api_key=" + api_key

puuidresponse = requests.get(accountv1url)
puuid = puuidresponse.json()['puuid']
tftaccounturl += puuid + "?api_key=" + api_key
response = requests.get(tftaccounturl)
id = response.json()['id']

tfturl = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/"
tfturl += response.json()['id'] + "?api_key=" + api_key
tftresponse = requests.get(tfturl)

# checks for empty response (unranked) otherwise returns the rank of the given user.
if not tftresponse.json():
    print(response.json()['name'] + "'s rank in TFT is Unranked")
else : 
    print(response.json()['name'] + "'s rank in TFT is",
      tftresponse.json()[0]['tier'], 
      tftresponse.json()[0]['rank'],
      tftresponse.json()[0]['leaguePoints'],
      "LP")
print(puuid)