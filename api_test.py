import requests
import os

# api_key = os.environ["RIOT_APP_API_KEY"]
api_key = "RGAPI-5b1ac605-ea0b-4e1d-b90a-c4233e0c0b95"
accountv1url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
accountv4url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
riotid = input("What is your Riot ID\n")
parts = riotid.split('#')
username = parts[0]
tagline = parts[1] 
accountv1url += username + "/" + tagline + "?api_key=" + api_key

puuidresponse = requests.get(accountv1url)
puuid = puuidresponse.json()['puuid']

accountv4url += puuid + "?api_key=" + api_key
response = requests.get(accountv4url)

id = response.json()['id']

tfturl = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/"
tfturl += response.json()['id'] + "?api_key=" + api_key
tftresponse = requests.get(tfturl)
if not tftresponse.json():
    print(response.json()['name'] + "'s rank in TFT is Unranked")
else : 
    print(response.json()['name'] + "'s rank in TFT is",
      tftresponse.json()[0]['tier'], 
      tftresponse.json()[0]['rank'],
      tftresponse.json()[0]['leaguePoints'],
      "LP")
