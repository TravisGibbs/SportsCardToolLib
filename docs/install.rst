Getting Started
===============

Installation
------------

To use SportsCardTool, first install it using pip:

.. code-block:: console

   pip install SportsCardTool

Usage
-----

Scraping a year of data:


.. code-block:: python

   from SportsCardTool import grab_card_list, dump_data, grab_year_links

   # Find All Cards for 2023 Season, returned as list of dictionaries
   year_links = grab_year_links(["2023"])
   card_list = grab_card_list(year_link)

   # Create CSV to allow for manipulation via pandas
   dump_data(mock_data, "2023_cards.csv")


Grabbing cards from scraped data

.. code-block:: python

   from SportsCardTool import QueryBuilder

   qb = QueryBuilder()

   # Construct query requesting Barry Bonds cards from 2000 with an autograph and a print run of 25 or 250
   qb.add_item({"name": "Barry Bonds", "year": "2000", "auto": "True", "serial": "25,250"})

   # Make request and return in form of tuple (list[dict], int)
   data = qb.grab_data()

   print(data[0])

.. code-block:: json
   

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
