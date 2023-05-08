import csv
import json
from typing import Dict, List, Tuple
import unicodedata
from urllib.request import urlopen, Request
import pybaseball as pyb

from bs4 import BeautifulSoup, Tag


STATCAST_TABLES_BATTER = {
    "Percentile Rankings": [
        "Year",
        "xwOBA",
        "xBA",
        "xSLG",
        "xISO",
        "xOBP",
        "Brl",
        "Brl%",
        "EV",
        "Max EV",
        "Hard Hit%",
        "K%",
        "BB%",
        "Whiff%",
        "Chase Rate",
        "Speed",
        "OAA",
        "Arm Strength",
    ],
    "Statcast Batting Statistics": [
        "Season",
        "Age",
        "Pitches",
        "Batted Balls",
        "Barrels",
        "Barrel %",
        "Barrel/PA",
        "Exit Velocity",
        "Max EV",
        "Launch Angle",
        "Sweet Spot %",
        "XBA",
        "XSLG",
        "WOBA",
        "XWOBA",
        "XWOBACON",
        "HardHit%",
        "K%",
        "BB%",
    ],
    "Batted Ball Profile": [
        "Season",
        "GB %",
        "FB %",
        "LD %",
        "PU %",
        "Pull %",
        "Straight %",
        "Oppo %",
        "Weak %",
        "Topped %",
        "Under %",
        "Flare/Burner %",
        "Solid %",
        "Barrel %",
        "Barrel/PA",
    ],
    "Run Values by Pitch Type": [
        "Year",
        "Pitch Type",
        "Team",
        "RV/100",
        "Run Value",
        "Pitches",
        "%",
        "PA",
        "BA",
        "SLG",
        "wOBA",
        "Whiff%",
        "K%",
        "PutAway %",
        "xBA",
        "xSLG",
        "xwOBA",
        "Hard Hit %",
    ],
    "Plate Discipline": [
        "Season",
        "Pitches",
        "Zone %",
        "Zone Swing %",
        "Zone Contact %",
        "Chase %",
        "Chase Contact %",
        "Edge %",
        "1st Pitch Swing %",
        "Swing %",
        "Whiff %",
        "Meatball %",
        "Meatball Swing %",
    ],
    "Advanced MLB Batting Statistics": [
        "Season",
        "Tm",
        "LG",
        "PA",
        "TB",
        "LOB",
        "SAC",
        "SF",
        "BABIP",
        "XBH",
        "GIDP",
        "GIDPO",
        "NP",
        "P/PA",
        "K/PA",
        "HR/PA",
        "BB/K",
        "ISO",
        "ROE",
        "WO",
    ],
    "Statcast Outs Above Average": [
        "Year",
        "Team",
        "Pos",
        "OAA",
        "In",
        "Lateral toward 3B",
        "Lateral toward 1B",
        "Back",
        "RHB",
        "LHB",
        "Attempts",
        "Success Rate",
        "Estimated Success Rate",
        "Success Rate Added",
    ],
    "Statcast Fielder Positioning": [
        "Season",
        "Team",
        "Pos",
        "PA",
        "Depth (ft.)",
        "Angle",
    ],
    "Statcast Running Statistics": [
        "Season",
        "Age",
        "Sprint Speed (ft/s)",
        "HP to 1st",
        "Bolts",
        "Pos Rank",
        "Age Rank",
        "Lg Rank",
        "% Rank",
    ],
}

STATCAST_TABLES_PITCHER = {
    "Statcast Statistics": [
        "Season",
        "Age",
        "Pitches",
        "Batted Balls",
        "Barrels",
        "Barrel %",
        "Barrel/PA",
        "Exit Velocity",
        "Max EV",
        "Launch Angle",
        "Sweet Spot %",
        "XBA",
        "XSLG",
        "WOBA",
        "XWOBA",
        "XWOBACON",
        "HardHit%",
        "K%",
        "BB%",
        "ERA",
        "xERA",
    ],
    "Batted Ball Profile": [
        "Season",
        "GB %",
        "FB %",
        "LD %",
        "PU %",
        "Pull %",
        "Straight %",
        "Oppo %",
        "Weak %",
        "Topped %",
        "Under %",
        "Flare/Burner %",
        "Solid %",
        "Barrel %",
        "Barrel/PA",
    ],
    "Pitch Movement": [
        ("Unnamed: 0_level_0", "Year"),
        ("Unnamed: 1_level_0", "Pitch"),
        ("Unnamed: 2_level_0", "Team"),
        ("Unnamed: 3_level_0", "Hand"),
        ("Unnamed: 4_level_0", "#"),
        ("Unnamed: 5_level_0", "MPH"),
        ("Vertical Movement (inches)", "Inches of Drop"),
        ("Vertical Movement (inches)", "vs Avg"),
        ("Vertical Movement (inches)", "% vs Avg"),
        ("Horizontal Movement (inches)", "Inches of Break"),
        ("Horizontal Movement (inches)", "vs Avg"),
        ("Horizontal Movement (inches)", "% Break vs Avg"),
    ],
    "Run Values by Pitch Type": [
        "Year",
        "Pitch Type",
        "Team",
        "RV/100",
        "Run Value",
        "Pitches",
        "%",
        "PA",
        "BA",
        "SLG",
        "wOBA",
        "Whiff%",
        "K%",
        "PutAway %",
        "xBA",
        "xSLG",
        "xwOBA",
        "Hard Hit %",
    ],
    "Spin Direction": [
        "Year",
        "Pitch Type",
        "Pitches",
        "MPH",
        "Active Spin %",
        "Total Movement (In.)",
        "Spin-Based",
        "Observed",
        "Deviation",
    ],
    "Swing/Take": [
        ("Unnamed: 0_level_0", "Year"),
        ("Unnamed: 1_level_0", "Team"),
        ("Unnamed: 2_level_0", "PA"),
        ("Unnamed: 3_level_0", "Pitches"),
        ("Runs", "Heart"),
        ("Runs", "Shadow"),
        ("Runs", "Chase"),
        ("Runs", "Waste"),
        ("Runs", "All"),
    ],
    "Plate Discipline": [
        "Season",
        "Pitches",
        "Zone %",
        "Zone Swing %",
        "Zone Contact %",
        "Chase %",
        "Chase Contact %",
        "Edge %",
        "1st Pitch Strike %",
        "Swing %",
        "Whiff %",
        "Meatball %",
        "Meatball Swing %",
    ],
    "Percentile Rankings": [
        "Year",
        "xwOBA  / xERA",
        "xBA",
        "xSLG",
        "xISO",
        "xOBP",
        "Brl",
        "Brl%",
        "EV",
        "Hard Hit%",
        "K%",
        "BB%",
        "Whiff%",
        "Chase Rate",
        "FB Velo",
        "FB Spin",
        "CB Spin",
        "Extension",
    ],
    "Statcast Shift Statistics": [
        ("Unnamed: 0_level_0", "Year"),
        ("Unnamed: 1_level_0", "PA"),
        ("Unnamed: 2_level_0", "wOBA"),
        ("vs RHH", "PA"),
        ("vs RHH", "Shifts"),
        ("vs RHH", "%"),
        ("vs LHH", "PA"),
        ("vs LHH", "Shifts"),
        ("vs LHH", "%"),
    ],
    "Pitch Tempo": [
        ("Unnamed: 0_level_0", "Season"),
        ("Unnamed: 1_level_0", "Team"),
        ("Bases Empty", "Pitches"),
        ("Bases Empty", "Tempo"),
        ("Bases Empty", "Fast %"),
        ("Bases Empty", "Slow %"),
        ("Runners On Base", "Pitches"),
        ("Runners On Base", "Tempo"),
        ("Runners On Base", "Fast %"),
        ("Runners On Base", "Slow %"),
    ],
}

MANAGER_TERMS = ["MG", "CO", "Coach", "Manager"]
ERROR_TERMS = [
    "ERR: No Copyright",
    "UER",
    "ERR",
    "COR",
]
UMPIRE_TERMS = ["UMP", "Umpire"]
LEADERS_TERMS = ["Leaders", "LL"]
CHECKLIST_TERMS = ["Checklist"]
ALL_STAR_TERMS = ["AS", "All Stars", "All Star", "All-Stars", "All-Star"]
ROOKIE_TERMS = ["Rookie Stars", "Rookies", "Rookie", "RS"]
POSITION_TERMS = ["RP", "CL"]
PARALLEL_TERMS = ["Grey Backs", "White Backs", "/66", "/POR"]


def check_remove_terms(name: str, terms: List[str]) -> Tuple[str, bool, bool]:
    """Takes in a string checks for terms in a list and removes them if possible.

    This is used to help parse listing, gaining data about the listing itself and
    trimming unessecary or confounding information.

    Args:
    name: A string representing the name of the card.
    terms: List of case sensitive terms to remove in the card

    Returns:
    A tuple containing the modified name, a bool indication of if a term was detected,
    and the term detected in the word.
    """
    for term in terms:
        if term in name:
            if name == term:
                return name.strip(), True, term
            else:
                name = name.replace(term, "")
                return name.strip(), True, term

    return (name, False, False)


def statcast_clean_column_names(column_name):
    if type(column_name) is tuple:
        if "Unnamed:" in str(column_name[0]):
            return str(column_name[1])
        else:
            return str(column_name[0]) + " " + str(column_name[1])
    else:
        return column_name.strip()


def filter_hrefs(links: List[Tag], filter: str) -> List[str]:
    """Filters tag objects according to filter and returns matching href strings.

    Returns a list of the href strings inside of each tag if they contain the filter string.

    Args:
        links: List of bs4 tag objects that may or may not have href
        filter: String that is used to filter.

    Returns:
        A list of strings, each one an href that contains the filter

    """
    hrefs = set()
    for link in links:
        href = link.get("href")
        if href:
            if filter in href:
                hrefs.add(href)
    return list(hrefs)

def just_soup(response):
    try:
        return BeautifulSoup(response.content, "lxml")
    except Exception:
        print("failed to capture " + response.url)
        return BeautifulSoup("<HTML></HTML>", "lxml")

def get_soup(href) -> BeautifulSoup:
    """Gets a BeautifulSoup object given an href string.

    The BeautifulSoup object is gathered by making a request to the page and
    parsing the response via an lxml parser. If the request fails or the parsing
    fails an empty BeatifulSoup object will be returned.

    Args:
        href: A string containing the href of a webpage to turned to soup.

    Returns:
        A BeautifulSoup object which will contain the contents of the webpage or
        be empty if the request or parsing fails.

    """
    try:
        req = Request(href)
        html_page = urlopen(req)
        return BeautifulSoup(html_page, "lxml")
    except Exception:
        print("failed to capture " + href)
        return BeautifulSoup("<HTML></HTML>", "lxml")


def find_player_ids(bref_id: str) -> dict:
    """Finds a list of ids based on the bref id for future development

    Returns a keyed dict of the player ids from different sources including pybaseball

    Args:
        bref_id: A string indicitive of the cards bref id.

    Returns:
        A dictionary containing the debut information of the player along with ids for linking.

    """
    return pyb.playerid_reverse_lookup([bref_id], "bbref").iloc[0].to_dict()


def remove_accents(input: str) -> str:
    """Removes accent marks and capitlization from string.

    Standardizing strings makes matching between cardlists and bref possible.
    Credit To: https://stackoverflow.com/questions/517923

    Args:
        input: A string to be modified.

    Returns:
        An output string that is lowered and removes all non standard characthers.

    """
    nfkd_form = unicodedata.normalize("NFKD", input)
    only_ascii = nfkd_form.encode("ASCII", "ignore")
    return only_ascii.decode()


def dump_data_csv(card_list: List[Dict], csv_name: str = "demo_cards.csv"):
    """Takes a list of dictionaries and creates a new csv file containing them

    Args:
        card_list: A list of dictionaries representing cards.
        csv_name: A name/path for output file defaults to demo_cards.csv

    """
    with open(csv_name, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, card_list[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(card_list)


def dump_data_json(card_list: List[Dict], json_name: str = "demo_cards.json"):
    """Takes a list of dictionaries and creates a new json file containing them

    Args:
        card_list: A list of dictionaries representing cards.
        json_name: A name/path for output file defaults to demo_cards.json

    """
    with open(json_name, "w") as output_file:
        json.dump(card_list, output_file)
