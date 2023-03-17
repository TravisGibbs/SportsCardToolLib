from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tqdm import tqdm
import csv

# This script builds a csv from a baseball set list site into a more parsible csv
# There is a basic descending heiarchy that can be represented by year->group->set->card


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
    req = Request(href)
    html_page = urlopen(req)
    return BeautifulSoup(html_page, "lxml")


# Grab links to years from list of selections
def grab_year_links(year_list):
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

    card['listing'] = panel.find("h5").text.strip()
    name_number = card['listing'].split("#")[1]
    card['number'] = name_number.split(" ")[0]
    name = " ".join(name_number.split(" ")[1:])
    if "1st Bowman" in name:
        card["name"] = name.split("1")[0].strip()
        card["rc"] = True
    else:
        card["name"] = name.strip()

    # Panel Area -> team, relic, auto, rc, serial
    badge_panel = panel.find_all("div", class_="border-muted border-bottom mb-3 pb-1")

    card["team"] = str(badge_panel[0]).split(">")[1].split("<")[0].strip()

    for badge in badge_panel[0].find_all("div", class_="badge"):
        txt = badge.text
        if "Serial" in txt:
            card["serial"] = int(txt.split("/")[1])
        elif "AUTO" in txt:
            card["auto"] = True
        elif "MEM" in txt:
            card["mem"] = True
        else:
            card["rc"] = True

    return card


# Grabs a card list from a list of year links
def grab_card_list(year_links):
    card_list = []
    # Main parsing loop
    for i, year_link in enumerate(year_links):
        # Only grab first n years that appear in descending order
        # TODO Change to I/O to select years
        if i > 0:
            break
        year = str(year_link).split("year-")[1].split("/")[0]
        print("Finding cards for", year, "hold on this might take a while!")
        group_soup = get_soup(year_link)
        groupus_soupus = set(group_soup.findAll('a'))
        group_links = filter_hrefs(groupus_soupus, "index-")
        for j in tqdm(range(len(group_links))):
            group_href = group_links[j]
            group = str(group_href).split("index-")[1].split("/")[0]
            set_soup = get_soup(group_href)
            set_links = filter_hrefs(set(set_soup.findAll('a')), "set-")
            for k, set_link in enumerate(set_links):
                set_ = str(set_link).split(year + "-")[1]
                player_soup = get_soup(set_link)
                player_panels = player_soup.find_all("div", class_="panel panel-primary")
                for player_panel in player_panels:
                    card = parse_panel(player_panel, year, group, set_)
                    card_list.append(card)
    return card_list


def dump_data(card_list, csv_name='demo_cards.csv'):
    # Dump data into csv
    with open(csv_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, card_list[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(card_list)


dump_data(grab_card_list(grab_year_links(["2023"])), "Master-Data.csv")
