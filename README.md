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

from SportsCardTool import QueryBuilder

qb = QueryBuilder()

# Construct query requesting Barry Bonds cards from 2000 with an autograph and a print run of 25 or 250
qb.add_item({"Players": "ruthba01", "year": "2020"})

# Make request and return in form of tuple (list[dict], int)
data = qb.grab_data()

print(data[0])
```
```json
[
   {
      "_id":"64551d0ee3e2072a92cb809a",
      "all_star":false,
      "auto":false,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "group":"topps-nowtheshow-baseball-card-checklist",
      "leaders":false,
      "listing":"2020 Topps Throwback Thursday  #206 Babe Ruth",
      "manager":false,
      "mem":false,
      "number":"206",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":1935,
            "name":"Babe Ruth",
            "short_name":"ruthba01"
         }
      ],
      "price":0,
      "rc":false,
      "serial":0,
      "server_pop":0,
      "set":"topps-throwbackthursday-baseball-card-checklist",
      "set_alt":"2020 Topps Throwback Thursday  ",
      "team":"New York Yankees",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2020"
   },
   {
      "_id":"64551d0ee3e2072a92cb7fda",
      "all_star":false,
      "auto":false,
      "back_img":"https://www.gletech.com/StockPhotos/Baseball/2020/184940/back_thumb_8892339.jpg",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"https://www.gletech.com/StockPhotos/Baseball/2020/184940/front_thumb_8892339.jpg",
      "group":"topps-nowtheshow-baseball-card-checklist",
      "leaders":false,
      "listing":"2020 Topps Throwback Thursday  #8 Babe Ruth",
      "manager":false,
      "mem":false,
      "number":"8",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":1935,
            "name":"Babe Ruth",
            "short_name":"ruthba01"
         }
      ],
      "price":0,
      "rc":false,
      "serial":0,
      "server_pop":0,
      "set":"topps-throwbackthursday-baseball-card-checklist",
      "set_alt":"2020 Topps Throwback Thursday  ",
      "team":"New York Yankees",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2020"
   },
   {
      "_id":"64551d0ee3e2072a92cb8068",
      "all_star":false,
      "auto":false,
      "back_img":"None",
      "checklist":false,
      "debut_year":"None",
      "error":false,
      "front_img":"None",
      "group":"topps-nowtheshow-baseball-card-checklist",
      "leaders":false,
      "listing":"2020 Topps Throwback Thursday  #150 Babe Ruth",
      "manager":false,
      "mem":false,
      "number":"150",
      "parallel":false,
      "players":[
         {
            "debut_year":false,
            "last_year":1935,
            "name":"Babe Ruth",
            "short_name":"ruthba01"
         }
      ],
      "price":0,
      "rc":false,
      "serial":0,
      "server_pop":0,
      "set":"topps-throwbackthursday-baseball-card-checklist",
      "set_alt":"2020 Topps Throwback Thursday  ",
      "team":"New York Yankees",
      "team_card":false,
      "umpire":false,
      "user_upload_links":[
         
      ],
      "year":"2020"
   }
]
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

### Attribution

This README was adapted from an example [here](https://github.com/rochacbruno/python-project-template/blob/main/README.md)
