from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tqdm import tqdm
import csv
import json

# This script builds a csv from a baseball set list site into a more parsible csv
# There is a basic descending heiarchy that can be represented by year->group->set->card

# Load in dictionary of debut and bref info
with open('./data/bref_data.json') as json_file:
    bref_info = json.load(json_file)


# Filters a list of links by a given string filter
def filter_hrefs(links, filter):
    hrefs = []
    for link in links:
        href = link.get('href')
        if href:
            if filter in href:
                hrefs.append(href)
    return hrefs


# Gathers the soup given a href
def get_soup(href):
    try:
        req = Request(href)
        html_page = urlopen(req)
        return BeautifulSoup(html_page, "lxml")
    except Exception:
        print("failed to capture " + href)
        return BeautifulSoup("<HTML></HTML>", "lxml")


# Grab links to years from list of selections
def grab_year_links(year_list):
    print(year_list)
    year_links = []

    year_soup = get_soup(
        "https://www.sportscardchecklist.com/sport-baseball/vintage-and-new-release-trading-card-checklists"
    )

    for year in year_list:
        year_links.extend(filter_hrefs(year_soup.find_all('a'), "year-" + year))
    return year_links


# Parses a given indvidual player panel and returns a dictionary representing an individual cards
def parse_panel(panel, year, group, set):
    card = {"year": year, "group": group, "set": set}
    card["serial"] = 0
    card["auto"] = False
    card["mem"] = False
    card["rc"] = False
    card['front_img'] = None
    card['back_img'] = None
    card['price'] = 0

    card['listing'] = panel.find("h5").text.strip()
    name_number = card['listing'].split("#")[1]

    card['number'] = name_number.split(" ")[0]
    card['name'] = " ".join(name_number.split(" ")[1:3])

    if card['name'] in bref_info['players']:
        card_bref = bref_info['players'][card['name']]
        card.update(card_bref)
    else:
        card['debut'] = None
        card['debut_year'] = None
        card['last_year'] = None
        card['last_game'] = None
        card['WAR'] = None
        card['short_name'] = None
        card['href'] = None

    for i, img in enumerate(panel.find_all(class_="img-fluid")):
        if i == 0:
            card['front_img'] = img['src']
        else:
            card['back_img'] = img['src']
    # Panel Area -> team, relic, auto, rc, serial
    badge_panel = panel.find_all("div", class_="border-muted border-bottom mb-3 pb-1")

    card["team"] = str(badge_panel[0]).split(">")[1].split("<")[0].strip()

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

    return card


def process_group_links(group_links, year):
    card_list = []
    for j in tqdm(range(len(group_links))):
        group_href = group_links[j]
        group = str(group_href).split("index-")[1].split("/")[0]
        set_soup = get_soup(group_href)
        set_links = filter_hrefs(set(set_soup.findAll('a')), "set-")
        card_list.extend(process_set_links(set_links, year, group))
    return card_list


def process_set_links(set_links, year, group=None):
    card_list = []
    for set_link in set_links:
        set_ = str(set_link).split(year + "-")[1]
        if group is None:
            group = set_
        player_soup = get_soup(set_link)
        player_panels = player_soup.find_all("div", class_="panel panel-primary")
        for player_panel in player_panels:
            card = parse_panel(player_panel, year, group, set_)
            card_list.append(card)
    return card_list


# Grabs a card list from a list of year links
def grab_card_list(year_links):
    card_list = []
    # Main parsing loop
    for year_link in year_links:
        year = str(year_link).split("year-")[1].split("/")[0]
        print("Finding cards for", year, "hold on this might take a while!")
        group_soup = get_soup(year_link)
        groupus_soupus = set(group_soup.findAll('a'))

        set_links = filter_hrefs(groupus_soupus, "set-")
        group_links = filter_hrefs(groupus_soupus, "index-")

        print("proccessing independent sets")
        card_list.extend(process_set_links(set_links, year))

        print("proccessing multi-sets")
        card_list.extend(process_group_links(group_links, year))

    return card_list


def dump_data(card_list, csv_name='demo_cards.csv'):
    # Dump data into csv
    with open(csv_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, card_list[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(card_list)
