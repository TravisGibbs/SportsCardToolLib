# SportsCardTool

[![Build Status](https://github.com/TravisGibbs/SportsCardTool/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/TravisGibbs/SportsCardTool/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/TravisGibbs/SportsCardTool/branch/main/graph/badge.svg)](https://codecov.io/gh/TravisGibbs/SportsCardTool)
[![PyPI](https://img.shields.io/pypi/v/SportsCardTool)](https://pypi.org/project/SportsCardTool/)

<img src="https://img.shields.io/badge/license-Apache--2.0-green"/>
<img src="https://img.shields.io/github/issues/travisgibbs/SportsCardTool?style=plastic"/>

SportsCardTool is designed to gather card data and track collections of cards. We hope to build the modern dynamic checklist and price book.

Currently SportsCardTool provides the ability to gather all baseball card setlists and to search prescraped data via data API and Querybuilder tool.

Potential contributors should check out [SportsCardToolServer](https://github.com/TravisGibbs/SportsCardToolServer).

## Install it from PyPI

```bash
pip install SportsCardTool
```

## Usage

Scraping a year of data:


```py

from SportsCardTool import grab_card_list, dump_data, grab_year_links

# Find All Cards for 2023 Season, returned as list of dictionaries
year_links = grab_year_links(["2023"])
card_list = grab_card_list(year_link)

# Create CSV to allow for manipulation via pandas
dump_data(mock_data, "2023_cards.csv")

```

Grabbing cards from scraped data

```py

from SportsCardTool import QueryBuilder

qb = QueryBuilder()

# Construct query requesting Barry Bonds cards from 2000 with an autograph and a print run of 25 or 250
qb.add_item({"name": "Barry Bonds", "year": "2000", "auto": "True", "serial": "25,250"})

# Make request and return in form of tuple (list[dict], int)
data = qb.grab_data()

print(data[0])
```
```json
[
    {
      "_id": "641f49185ee984b20a66ef77",
      "auto": true,
      "back_img": null,
      "front_img": null,
      "group": "fleer-ultra",
      "listing": "2000 Fleer Ultra Fresh Ink #11 Barry Bonds",
      "mem": false,
      "name": "Barry Bonds",
      "number": "11",
      "price": 0,
      "rc": false,
      "serial": 250,
      "set": "fleer-ultra-fresh-ink-baseball-trading-card-checklist",
      "team": "San Francisco Giants",
      "year": 2000
    },
    {
      "_id": "641f49185ee984b20a66f5f4",
      "auto": true,
      "back_img": null,
      "front_img": null,
      "group": "fleer-ultra",
      "listing": "2000 Fleer Ultra Fresh Ink #11 Barry Bonds",
      "mem": false,
      "name": "Barry Bonds",
      "number": "11",
      "price": 0,
      "rc": false,
      "serial": 250,
      "set": "fleer-ultra-fresh-ink-baseball-trading-card-checklist",
      "team": "San Francisco Giants",
      "year": 2000
    },
    {
      "_id": "641f49185ee984b20a674b2f",
      "auto": true,
      "back_img": null,
      "front_img": null,
      "group": "upper-deck",
      "listing": "2000 Upper Deck  Game Jersey Autograph Numbered #BB Barry Bonds",
      "mem": true,
      "name": "Barry Bonds",
      "number": "BB",
      "price": 0,
      "rc": false,
      "serial": 25,
      "set": "upper-deck-game-jersey-autograph-numbered-baseball-trading-card-checklist",
      "team": "San Francisco Giants",
      "year": 2000
    },
    {
      "_id": "641f49185ee984b20a678e31",
      "auto": true,
      "back_img": null,
      "front_img": null,
      "group": "upper-deck-pros-and-prospects",
      "listing": "2000 Upper Deck Pros and Prospects Game Jersey Autograph Gold #BB Barry Bonds",
      "mem": true,
      "name": "Barry Bonds",
      "number": "BB",
      "price": 0,
      "rc": false,
      "serial": 25,
      "set": "upper-deck-pros-and-prospects-game-jersey-autograph-gold-baseball-trading-card-checklist",
      "team": "San Francisco Giants",
      "year": 2000
    },
    {
      "_id": "641f49185ee984b20a67958c",
      "auto": true,
      "back_img": null,
      "front_img": null,
      "group": "sp-authentic",
      "listing": "2000 SP Authentic Chirography Gold #GBB Barry Bonds",
      "mem": false,
      "name": "Barry Bonds",
      "number": "GBB",
      "price": 0,
      "rc": false,
      "serial": 25,
      "set": "sp-authentic-chirography-gold-baseball-trading-card-checklist",
      "team": "San Francisco Giants",
      "year": 2000
    }
]
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

### Attribution

This README was adapted from an example [here](https://github.com/rochacbruno/python-project-template/blob/main/README.md)
