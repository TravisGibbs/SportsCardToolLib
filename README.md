# SportsCardTool

[![Build Status](https://github.com/TravisGibbs/SportsCardTool/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/TravisGibbs/SportsCardTool/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/TravisGibbs/SportsCardToolLib/branch/main/graph/badge.svg?token=D45VY693WQ)](https://codecov.io/gh/TravisGibbs/SportsCardToolLib)[![PyPI](https://img.shields.io/pypi/v/SportsCardTool)](https://pypi.org/project/SportsCardTool/)

<img src="https://img.shields.io/badge/license-Apache--2.0-green"/>
<img src="https://img.shields.io/github/issues/travisgibbs/SportsCardTool?style=plastic"/>

SportsCardTool is designed to gather card data and track collections of cards. We hope to build the modern dynamic checklist and price book.

Currently SportsCardTool provides the ability to gather all baseball card setlists and to search prescraped data via data API and Querybuilder tool.

Potential contributors should check out [SportsCardToolServer](https://github.com/TravisGibbs/SportsCardToolServer) and soon to launch [SportsCardToolApp](https://github.com/TravisGibbs/SportsCardToolApp).

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

Grabbing cards from scraped data via code:
Also accessible directly [here](https://travisapi.pythonanywhere.com/api/v1/sportscards/search?)!

```py

from SportsCardTool import query_builder

qb = query_builder()

# Construct query requesting Barry Bonds cards from 2000 with an autograph and a print run of 25 or 250
qb.add_item({"players": "bondsba01", "year": "2000", "auto": "True", "serial": "25,250"})

# Make request and return in form of tuple (list[dict], int)
data = qb.grab_data()

print(data[0])
```
```json
[
   {
      "_id":"6467d1d3d19b3e7d748c339a",
      "all_star":false,
      "auto":true,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "leaders":false,
      "listing":"2000 Upper Deck MVP Game Used Souvenirs Signed #BBSB Barry Bonds Bat",
      "manager":false,
      "mem":true,
      "number":"BBSB",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":2007,
            "name":"Barry Bonds Bat",
            "short_name":"bondsba01"
         }
      ],
      "price":0,
      "rc":false,
      "release":"upper-deck-mvp",
      "release_alt":"2000 ",
      "serial":25,
      "server_pop":0,
      "set":"upper-deck-mvp-game-used-souvenirs-signed-baseball-trading-card-checklist?release_name=upper-deck-mvp",
      "set_alt":"2000 Upper Deck MVP Game Used Souvenirs Signed",
      "team":"San Francisco Giants",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2000"
   },
   {
      "_id":"6467d1d3d19b3e7d748c3455",
      "all_star":false,
      "auto":true,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "leaders":false,
      "listing":"2000 Upper Deck MVP Game Used Souvenirs Signed #BBSG Barry Bonds Glove",
      "manager":false,
      "mem":true,
      "number":"BBSG",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":2007,
            "name":"Barry Bonds Glove",
            "short_name":"bondsba01"
         }
      ],
      "price":0,
      "rc":false,
      "release":"upper-deck-mvp",
      "release_alt":"2000 ",
      "serial":25,
      "server_pop":0,
      "set":"upper-deck-mvp-game-used-souvenirs-signed-baseball-trading-card-checklist?release_name=upper-deck-mvp",
      "set_alt":"2000 Upper Deck MVP Game Used Souvenirs Signed",
      "team":"San Francisco Giants",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2000"
   },
   {
      "_id":"6467d1dcd19b3e7d748c3f24",
      "all_star":false,
      "auto":true,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "leaders":false,
      "listing":"2000 Upper Deck  Game Jersey Autograph Numbered #BB Barry Bonds",
      "manager":false,
      "mem":true,
      "number":"BB",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":2007,
            "name":"Barry Bonds",
            "short_name":"bondsba01"
         }
      ],
      "price":0,
      "rc":false,
      "release":"upper-deck",
      "release_alt":"2000 upper",
      "serial":25,
      "server_pop":0,
      "set":"upper-deck-game-jersey-autograph-numbered-baseball-trading-card-checklist?release_name=upper-deck",
      "set_alt":"2000 Upper Deck  Game Jersey Autograph Numbered",
      "team":"San Francisco Giants",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2000"
   },
   {
      "_id":"6467d1dcd19b3e7d748c3fd6",
      "all_star":false,
      "auto":true,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "leaders":false,
      "listing":"2000 Fleer Ultra Fresh Ink #11 Barry Bonds",
      "manager":false,
      "mem":false,
      "number":"11",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":2007,
            "name":"Barry Bonds",
            "short_name":"bondsba01"
         }
      ],
      "price":0,
      "rc":false,
      "release":"fleer-ultra",
      "release_alt":"2000 fleer",
      "serial":250,
      "server_pop":0,
      "set":"fleer-ultra-fresh-ink-baseball-trading-card-checklist?release_name=fleer-ultra",
      "set_alt":"2000 Fleer Ultra Fresh Ink",
      "team":"San Francisco Giants",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2000"
   },
   {
      "_id":"6467d1f9d19b3e7d748cb602",
      "all_star":false,
      "auto":true,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "leaders":false,
      "listing":"2000 SP Authentic Chirography Gold #GBB Barry Bonds",
      "manager":false,
      "mem":false,
      "number":"GBB",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":2007,
            "name":"Barry Bonds",
            "short_name":"bondsba01"
         }
      ],
      "price":0,
      "rc":false,
      "release":"sp-authentic",
      "release_alt":"2000 sp",
      "serial":25,
      "server_pop":0,
      "set":"sp-authentic-chirography-gold-baseball-trading-card-checklist?release_name=sp-authentic",
      "set_alt":"2000 SP Authentic Chirography Gold",
      "team":"San Francisco Giants",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2000"
   },
   {
      "_id":"6467d203d19b3e7d748ce35c",
      "all_star":false,
      "auto":true,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "leaders":false,
      "listing":"2000 Upper Deck Pros and Prospects Game Jersey Autograph Gold #BB Barry Bonds",
      "manager":false,
      "mem":true,
      "number":"BB",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":2007,
            "name":"Barry Bonds",
            "short_name":"bondsba01"
         }
      ],
      "price":0,
      "rc":false,
      "release":"upper-deck-pros-and-prospects",
      "release_alt":"2000 upper deck",
      "serial":25,
      "server_pop":0,
      "set":"upper-deck-pros-and-prospects-game-jersey-autograph-gold-baseball-trading-card-checklist?release_name=upper-deck-pros-and-prospects",
      "set_alt":"2000 Upper Deck Pros and Prospects Game Jersey Autograph Gold",
      "team":"San Francisco Giants",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2000"
   }
]
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

### Attribution

This README was adapted from an example [here](https://github.com/rochacbruno/python-project-template/blob/main/README.md)
