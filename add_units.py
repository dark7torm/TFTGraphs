import requests
import os
from tkinter import *
from tkinter import font
from collections import defaultdict
import psycopg2
from config import load_config

# Add your Riot API Key here
api_key = os.environ["RIOT_APP_API_KEY"]

# GUI window initialization
window = Tk()
window.state('zoomed')
graphsFont = font.Font(family = "Helvetica", size=12, weight="bold")

def adjust_wrap(event):
    resultLabel1.config(wraplength=window.winfo_width() // 2)
    resultLabel2.config(wraplength=window.winfo_width() // 2)

def puuid_finder():
    accountv1url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
    riotid = gameEntry.get() 
    parts = riotid.split('#')
    username = parts[0]
    tagline = parts[1]
    accountv1url += f"{username}/{tagline}?api_key={api_key}"
    puuidresponse = requests.get(accountv1url)
    puuid = puuidresponse.json()['puuid']
    gameLabel.config(text="How many games would you like to analyze your traits for")
    gameEntry.delete(0, len(riotid))
    gameButton.config(command=lambda: get_info_and_store(username, puuid), text="Go")
    return puuid

def match_history(puuid): 
    tftgamelisturl = 'https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/'
    count = gameEntry.get()
    gameEntry.delete(0, len(count))
    tftgamelisturl += f'{puuid}/ids?start=0&count={count}&api_key={api_key}'
    gameresponse = requests.get(tftgamelisturl)
    return gameresponse.json()

def match_info(match_id):
    info_url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}"
    match_response_json = requests.get(info_url).json()
    return match_response_json

def get_traits(match_json, puuid):
    participant = match_json['info']['participants']
    traits = []
    for p in participant:
        if p["puuid"] == puuid:
            info = p["traits"]
            for trait in info:
                if trait["style"] > 0:
                    traits.append(trait["name"][6:])
    return traits

def get_units(match_json, puuid):
    participant = match_json['info']['participants']
    units = []
    for p in participant:
        if p["puuid"] == puuid:
            info = p["units"]
            for unit in info:
                units.append(unit["character_id"][6:])
    return units

def get_placement(match_json, puuid): 
    participant = match_json['info']['participants']
    placement = 9
    for p in participant:
        if p["puuid"] == puuid:
            placement = p["placement"]
    return placement

def get_lastx_units(puuid):
    match_list = match_history(puuid)
    units_dict = dict()
    for match in match_list:
        if get_placement(match_info(match), puuid) < 5:
            for unit in get_units(match_info(match), puuid):
                units_dict[unit] = units_dict.get(unit, 0) + 1
    resultLabel2.config(text=format_result(units_dict), wraplength=window.winfo_width() // 2)
    resultLabel2.grid(row=3, column=1, sticky="nsew")
    return units_dict

def get_lastx_traits(puuid):
    match_list = match_history(puuid)
    traits_dict = dict()
    for match in match_list:
        if get_placement(match_info(match), puuid) < 5:
            for trait in get_traits(match_info(match), puuid):
                traits_dict[trait] = traits_dict.get(trait, 0) + 1
    resultLabel1.config(text=format_result(traits_dict), wraplength=window.winfo_width() // 2)
    resultLabel1.grid(row=3, column=0, sticky="nsew")
    return traits_dict

def format_result(traits_dict):
    sorted_items = sorted(traits_dict.items(), key=lambda item: (-item[1], item[0]))
    grouped = defaultdict(list)
    for trait, count in sorted_items:
        grouped[count].append(trait)
    formatted_list = "\n".join(f"{count}: {', '.join(sorted(traits))}" for count, traits in sorted(grouped.items(), reverse=True))
    return formatted_list

# PostgreSQL connection and insertion functions
def connect_and_store(username, puuid, units, traits):
    connection = None
    params = load_config()
    try:
        connection = psycopg2.connect(**params)
        with connection.cursor() as curs:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS tft_player_data (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                puuid VARCHAR(100) NOT NULL,
                units TEXT[] NOT NULL,
                traits TEXT[] NOT NULL
            )'''
            curs.execute(create_table_query)
            insert_query = '''
            INSERT INTO tft_player_data (username, puuid, units, traits)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            '''
            curs.execute(insert_query, (username, puuid, units, traits))
            new_id = curs.fetchone()[0]
            print(f"Inserted data with id: {new_id}")
            connection.commit()
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')

def get_info_and_store(username, puuid):  # Add username parameter
    units_dict = get_lastx_units(puuid)
    traits_dict = get_lastx_traits(puuid)
    units = list(units_dict.keys())
    traits = list(traits_dict.keys())
    connect_and_store(username, puuid, units, traits)  # Pass username

# GUI initialization and elements
def gui_init():
    window.title("TFTGraphs")
    window.geometry(f'{window.winfo_screenwidth()}x{window.winfo_screenheight()}')
    window.tk.call('tk', 'scaling', 3.0)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    
    global gameLabel, gameEntry, gameButton, resultLabel1, resultLabel2
    gameLabel = Label(window, text="What is your riot id", font=graphsFont)
    gameLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    gameEntry = Entry(width=50, font=graphsFont)
    gameEntry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    gameButton = Button(window, text="Find PUUID", width=10, height=3, command=puuid_finder, font=graphsFont, pady=5)
    gameButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    resultLabel1 = Label(window, wraplength=window.winfo_width() // 2, anchor='w', justify='left', font=graphsFont)
    resultLabel1.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

    resultLabel2 = Label(window, wraplength=window.winfo_width() // 2, anchor='w', justify='left', font=graphsFont)
    resultLabel2.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

    window.bind('<Configure>', adjust_wrap)
    print("GUI initialized")
    window.mainloop()

if __name__ == "__main__":
    gui_init()
