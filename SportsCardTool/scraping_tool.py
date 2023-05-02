from tqdm import tqdm
from bs4.element import Tag
from typing import Tuple
from typing import List
from typing import Dict
import json
import os
from SportsCardTool.bref_tool import remove_accents
from SportsCardToolLib.SportsCardTool.util import (
    ALL_STAR_TERMS,
    ERROR_TERMS,
    LEADERS_TERMS,
    MANAGER_TERMS,
    PARALLEL_TERMS,
    POSITION_TERMS,
    ROOKIE_TERMS,
    UMPIRE_TERMS,
    check_remove_terms,
    filter_hrefs,
    get_soup,
)

"""
This file contains the main scraping tool and helper functions.
"""
file_path = os.path.join(os.path.dirname(__file__), "data/bref_data.json")

# Load in dictionary of debut and bref info
with open(file_path) as json_file:
    bref_info = json.load(json_file)


def grab_bref_info(name: str) -> Dict:
    """Tries different variations of name to find bref_info

    Args:
        name: A string containing the player name.

    Returns:
        A dict containing bref_info for the given player or
        a placeholder dictionary and a corrected name string when possible!

    """
    card_bref = {"short_name": None, "debut_year": None, "last_year": None}
    return_name = name

    if name in bref_info["players"]:
        card_bref = bref_info["players"][name]
    elif " ".join(name.split(" ")[0:3]) in bref_info["players"]:
        card_bref = bref_info["players"][" ".join(name.split(" ")[0:3])]
        return_name = " ".join(name.split(" ")[0:3])
    elif name.split(" jr.")[0] in bref_info["players"]:
        card_bref = bref_info["players"][name.split(" jr.")[0]]
        return_name = name.split(" jr.")[0] + " jr."
    elif name.split(" sr.")[0] in bref_info["players"]:
        card_bref = bref_info["players"][name.split(" sr.")[0]]
        return_name = name.split(" sr.")[0] + " sr."
    elif " ".join(name.split(" ")[0:2]) in bref_info["players"]:
        card_bref = bref_info["players"][" ".join(name.split(" ")[0:2])]
        return_name = " ".join(name.split(" ")[0:2])
    elif " ".join(name.split(" ")[0:2]) == "hank aaron":
        card_bref = bref_info["players"]["henry aaron"]

    return card_bref, return_name


def grab_year_links(year_list: List[str]) -> List[Tuple[Tag]]:
    """Takes a list of years and finds link Tags for each year on SportsCardsChecklist.com.

    Args:
        year_list: List of strings with each representing a numeric year IE: ['2015', '2016']

    Returns:
        A list of tuples with the first value being an <a> tag that contained any one of
        the years specified and the second value being a str representing the year.

        IE: (bs4.element.Tag, "2015")

        Note that thereis currently a bug where years on the website are parsed based on first year in link
        which could cause unexpected behaviors IE '2003-07' would be parsed as 2003.
    """
    print(year_list)
    year_links = []

    year_soup = get_soup(
        "https://www.sportscardchecklist.com/sport-baseball/vintage-and-new-release-trading-card-checklists"
    )

    for year in year_list:
        year_links.extend(filter_hrefs(year_soup.find_all("a"), "year-" + year))
    return year_links


def parse_panel(panel: Tag, year: str, group: str, set: str) -> Dict:
    """Takes in a panel and other gathered info and creates a card dict to be returned.

    Args:
        panel: A html tag containing all of the players info.
        year: A string representing the year the card belongs to.
        Group: A string representing the group the card belongs to
        Set: A string representing the set the card belongs to.

    Returns:
        A dictionary containing all of the data that was able to extracted.
        If the players name was previously saved and then matched, this
        card will also show how it was created reletive to the players career.

        Note the listing parser to find player names still struggles identifying
        several types of cards (team cards, multi player, checklist).
    """
    card = {"year": year, "group": group, "set": set}
    card["set_alt"] = None
    card["serial"] = 0
    card["auto"] = False
    card["mem"] = False
    card["rc"] = False
    card["front_img"] = None
    card["back_img"] = None
    card["price"] = 0
    card["server_pop"] = 0
    card["user_upload_links"] = []
    card["debut_year"] = None
    card["pre_major"] = None
    card["post_career"] = None
    card["short_names"] = []
    card["manager"] = False
    card["umpire"] = False
    card["team_card"] = False
    card["error"] = False
    card["checklist"] = False
    card["leaders"] = False
    card["all_star"] = False
    card["parallel"] = False
    card["names"] = []
    card_bref = None

    # Panel Area -> team, relic, auto, rc, serial
    badge_panel = panel.find_all("div", class_="border-muted border-bottom mb-3 pb-1")

    for badge in badge_panel[0].find_all("div", class_="badge"):
        txt = badge.text
        if "Serial" in txt:
            card["serial"] = int(txt.split("/")[1].split(" ")[0])
        elif "AUTO" in txt:
            card["auto"] = True
        elif "MEM" in txt:
            card["mem"] = True
        else:
            card["rc"] = True

    card["team"] = str(badge_panel[0]).split(">")[1].split("<")[0].strip()
    card["listing"] = panel.find("h5").text.strip()
    card["set_alt"], name_number = card["listing"].split("#")[:2]

    card["number"] = name_number.split(" ")[0]
    possible_name = remove_accents(" ".join(name_number.split(" ")[1:])).strip()

    if "Checklist" in possible_name:
        card["checklist"] = True
        possible_name.replace("Checklist/", "")

    possible_name, card["umpire"], _ = check_remove_terms(possible_name, UMPIRE_TERMS)
    possible_name, card["manager"], _ = check_remove_terms(possible_name, MANAGER_TERMS)
    possible_name, card["error"], _ = check_remove_terms(possible_name, ERROR_TERMS)
    possible_name, card["leaders"], _ = check_remove_terms(possible_name, LEADERS_TERMS)
    possible_name, card["all_star"], _ = check_remove_terms(
        possible_name, ALL_STAR_TERMS
    )
    possible_name, card["rc"], _ = check_remove_terms(possible_name, ROOKIE_TERMS)
    possible_name, _, _ = check_remove_terms(possible_name, POSITION_TERMS)
    possible_name, _, card["parallel"] = check_remove_terms(
        possible_name, PARALLEL_TERMS
    )

    possible_names = possible_name.split("/")
    for pos_name in possible_names:
        pos_name = pos_name.strip()
        if len(pos_name) > 2:
            card_bref, pos_name = grab_bref_info(pos_name.strip().lower())
            if card_bref["short_name"]:
                card["short_names"].append(card_bref["short_name"])
            if card_bref["debut_year"]:
                card["pre_major"] = int(card_bref["debut_year"]) > int(year[:4])
                card["debut_year"] = card_bref["debut_year"] == year
            if card_bref["last_year"]:
                card["post_career"] = int(card_bref["last_year"]) < int(year[:4])
            card["names"].append(pos_name)

    if card["team"] and len(card["short_names"]) == 0 and len(card["names"]) > 0:
        team_words = card["team"].split(" ")
        if card["names"][0] == card["team"].lower() or any(
            word in possible_names for word in team_words
        ):
            card["team_card"] = True

    for i, img in enumerate(panel.find_all(class_="img-fluid")):
        if i == 0:
            card["front_img"] = img["src"]
        else:
            card["back_img"] = img["src"]

    return card


def process_group_links(group_links: List[str], year: str) -> List[Dict]:
    """Proccesses group links into sets and then returns all cards in the group.

    Args:
        group_links: A list of href strings.
        year: A string representing the year the cards belongs to.

    Returns:
        A list of card dictionaries as proccessed by parse_panel. The cards
        returned will have a reference to the year, group, and set respectively.

    """
    card_list = []
    for j in tqdm(range(len(group_links))):
        group_href = group_links[j]
        group = str(group_href).split("index-")[1].split("/")[0]
        set_soup = get_soup(group_href)
        set_links = filter_hrefs(set(set_soup.findAll("a")), "set-")
        card_list.extend(process_set_links(set_links, year, group))
    return card_list


def process_set_links(set_links: List[str], year: str, group: str = "") -> List[Dict]:
    """Proccesses set links and then returns all cards in the sets.

    Args:
        set_links: A list of href strings.
        year: A string representing the year the cards belongs to.

    Returns:
        A list of card dictionaries as proccessed by parse_panel. The cards
        returned will have a reference to the year, group, and set respectively.

        Note if not group is detected group is set to be equal to set to enable easy
        future searching.
    """
    card_list = []
    for set_link in set_links:
        set_ = str(set_link).split(year + "-")[1]
        if group == "":
            group = set_
        player_soup = get_soup(set_link)
        player_panels = player_soup.find_all("div", class_="panel panel-primary")
        for player_panel in player_panels:
            card = parse_panel(player_panel, year, group, set_)
            card_list.append(card)
    return card_list


def grab_card_list(year_links: List[str]) -> List[Dict]:
    """Finds all groups and sets in a year and returns all cards.

    Args:
        year_links: A list of href strings to different years to be parsed

    Returns:
        A list of all cards from different groups/sets in the year as parsed by
        parse_panel.

        Note performance is still slow due to network calls and the amount of
        data contained in years grows exponentially over time.

    """
    card_list = []
    # Main parsing loop

    for year_link in year_links:
        year = str(year_link).split("year-")[1].split("/")[0]
        print("Finding cards for", year, "hold on this might take a while!")
        group_soup = get_soup(year_link)
        groupus_soupus = set(group_soup.findAll("a"))

        set_links = filter_hrefs(groupus_soupus, "set-")
        group_links = filter_hrefs(groupus_soupus, "index-")

        print("proccessing independent sets")
        card_list.extend(process_set_links(set_links, year))

        print("proccessing multi-sets")
        card_list.extend(process_group_links(group_links, year))

    return card_list
