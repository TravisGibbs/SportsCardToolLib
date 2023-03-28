import requests
from bs4 import BeautifulSoup
from time import sleep
import json

import unicodedata


# Credit To: https://stackoverflow.com/questions/517923
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()


def grab_debut_year(year):
    year_dictionary = {"players": {}}
    print("scraping year " + year)
    url = "https://www.baseball-reference.com/leagues/majors/" + year + "-debuts.shtml"
    # Sleep before firing requests to respect baseball reference guidelines
    sleep(3)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
    # Grab table containing all debuts
    table = soup.find("tbody")
    for row in table.find_all("tr"):
        player = {"debut_year": year}
        player['last_game'] = None
        player['last_year'] = None
        player["debut"] = None
        player['short_name'] = None
        player['href'] = None
        player['draft_year'] = None
        player['WAR'] = None
        for col in row.find_all("td"):
            col_name = col["data-stat"]
            if col_name == "player":
                player_link = col.find("a")
                player['href'] = player_link['href']
                name = remove_accents(player_link.get_text())
                player['short_name'] = col['data-append-csv']
            elif col_name == "debut":
                link = col.find("a")
                if link:
                    link_text = link.get_text()
                    if link_text != "" and link_text is not None:
                        player['debut'] = link.get_text() + ", " + year
            elif col_name == "final_game":
                game_link = col.find("a")
                if game_link:
                    game_link_text = game_link.get_text()
                    if game_link_text != "" and game_link_text is not None:
                        player['last_game'] = game_link_text
                        player['last_year'] = player['last_game'].split(" ")[2]
            elif col_name == "WAR":
                player['WAR'] = col.text
            elif col_name == "draft":
                if "in" in col.text:
                    player['draft_year'] = col.text.split("in ")[1].split(" ")[0][:4]

        year_dictionary["players"][name] = player
    return year_dictionary


def grab_debut_dict(years, allow_repeats=False, dictionary={"years": {}, "players": {}}):
    for year in years:
        if year not in dictionary['years'] or allow_repeats:
            year_dictionary = grab_debut_year(year)
            dictionary['players'].update(year_dictionary['players'])
            # Flag year to avoid repeated searches
            dictionary["years"][year] = True
    return dictionary
