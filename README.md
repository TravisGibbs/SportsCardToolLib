# SportsCardTool

[![Build Status](https://github.com/TravisGibbs/SportsCardTool/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/TravisGibbs/SportsCardTool/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/TravisGibbs/SportsCardTool/branch/main/graph/badge.svg)](https://codecov.io/gh/TravisGibbs/SportsCardTool)
[![PyPI](https://img.shields.io/pypi/v/SportsCardTool)](https://pypi.org/project/SportsCardTool/)

<img src="https://img.shields.io/badge/license-Apache--2.0-green"/>
<img src="https://img.shields.io/github/issues/travisgibbs/SportsCardTool?style=plastic"/>

SportsCardTool is designed to gather card data and track collections of cards. We hope to build the modern dynamic checklist and price book.

Currently SportsCardTool provides the ability to gather all baseball card setlists. In the future these setlists will be prescraped, allowing for search and tracking capabilities. We would like to drive price tracking via users which would help dectralize some of the larger data collection.

## Install it from PyPI

```bash
pip install SportsCardTool
```

## Usage

```py

from SportsCardTool import grab_card_list, dump_data, grab_year_links

# Find All Cards for 2023 Season, returned as list of dictionaries
year_links = grab_year_links(["2023"])
card_list = grab_card_list(year_link)

# Create CSV to allow for manipulation via pandas
dump_data(mock_data, "2023_cards.csv")

```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

### Attribution

This README was adapted from an example [here](https://github.com/rochacbruno/python-project-template/blob/main/README.md)
