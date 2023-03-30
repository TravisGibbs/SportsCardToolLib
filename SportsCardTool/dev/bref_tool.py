import requests
from bs4 import BeautifulSoup
from time import sleep
from typing import Dict
from typing import List


"""
This File contains tools for searching baseball reference.
"""

import unicodedata


def remove_accents(input: str) -> str:
    """Removes accent marks and capitlization from string.

    Standardizing strings makes matching between cardlists and bref possible.
    Credit To: https://stackoverflow.com/questions/517923

    Args:
        input: A string to be modified.

    Returns:
        An output string that is lowered and removes all non standard characthers.

    """
    nfkd_form = unicodedata.normalize('NFKD', input)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()


def grab_debut_year(year: str) -> Dict:
    """Grabs bref info for all players who debuted in a given year.

    Args:
        year: A string containing a year to be searching on baseball reference
        IE: "2017"

    Returns:
        A dictionary with the players stored in a dictionary keyed by their names.

        Note this function sleeps between each call to respect baseball reference's
        policies, please do not modify.

    """
    year_dictionary = {}
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

        year_dictionary[name] = player
    return year_dictionary


def grab_debut_dict(
    years: List[str], allow_repeats: bool = False, dictionary: Dict = {"years": {}, "players": {}}
) -> dict:
    """Master function that allows users to search accross multiple years

    Args:
        years: A list of strings representing years.
        IE: ["1940",  "1941"]

        allow_repeats: If True will search a year again even if it
        is already in passed in dictionary.

        dictionary: A dict that defualts to empty with the following format:
            {
                "years": {
                    "1939": True
                }
                "players": {
                    "Ted Williams" : {

                    }
                }
            }

    Returns:
        A dictionary in the same format as what is passed in
        with player info from all debut years.

    """
    for year in years:
        if year not in dictionary['years'] or allow_repeats:
            year_dictionary = grab_debut_year(year)
            dictionary['players'].update(year_dictionary)
            # Flag year to avoid repeated searches
            dictionary["years"][year] = True
    return dictionary



