from SportsCardTool import (
    grab_card_list,
    dump_data_csv,
    dump_data_json,
    get_soup,
    filter_hrefs,
    grab_year_links,
    query_builder,
    process_group_links,
    process_set_links,
    grab_debut_dict,
    remove_accents,
    grab_debut_year,
    check_remove_terms,
    grab_bref_info,
    EbayTool,
)
from bs4 import BeautifulSoup
import pandas as pd
from os import environ
import json


def test_grab_bref_info():
    bref_info, name = grab_bref_info("ted williams")
    assert bref_info["short_name"] == "willite01"
    assert bref_info["debut_year"] == "1939"
    assert bref_info["last_year"] == "1960"
    assert name == "ted williams"


def test_grab_debut_year():
    d = grab_debut_year("1939")
    assert "Ted Williams" in d
    assert d["Ted Williams"] == {
        "debut_year": "1939",
        "last_game": "Sep 28, 1960",
        "last_year": "1960",
        "debut": "Apr 20, 1939",
        "short_name": "willite01",
        "href": "/players/w/willite01.shtml",
        "draft_year": None,
        "WAR": "121.8",
    }


def test_grab_debut_dict():
    years = ["1939"]
    d = grab_debut_dict(years)
    assert len(d) == 2
    assert len(d["players"]) > 10
    assert "Ted Williams" in d["players"]
    assert d["players"]["Ted Williams"] == {
        "debut_year": "1939",
        "last_game": "Sep 28, 1960",
        "last_year": "1960",
        "debut": "Apr 20, 1939",
        "short_name": "willite01",
        "href": "/players/w/willite01.shtml",
        "draft_year": None,
        "WAR": "121.8",
    }


def test_remove_accents():
    assert remove_accents("Edwin Díaz") == "Edwin Diaz"
    assert remove_accents("Rafael Devers") == "Rafael Devers"


def test_query_builder():
    qb = query_builder()
    qb.add_item({"name": "Barry Bonds"})
    data = qb.grab_data()
    assert len(data[0]) >= 1000
    assert data[1] >= 1000


def test_grab_year_links():
    assert len(grab_year_links(["2023"])) == 1
    assert len(grab_year_links(["2023", "2022"])) == 2


def test_process_set_links():
    cards = process_set_links(
        ["https://www.sportscardchecklist.com/set-138550/1990-topps-coins-baseball-card-checklist"],
        "1990",
    )
    assert len(cards) > 40


def test_process_group_links():
    cards = process_group_links(
        [
            "https://www.sportscardchecklist.com/sport-baseball/year-1990/index-star/trading-card-checklists-and-product-information"
        ],
        "1990",
    )
    assert len(cards) > 100


def test_grab_data():
    card_list = grab_card_list(grab_year_links(["1950"]))
    assert type(card_list) == type(list())
    assert len(card_list) > 100
    assert type(card_list[0]) == type(dict())


def test_dump_data_csv():
    mock_data = [{"a": "a", "b": "b"}, {"a": "b", "b": "a"}]
    dump_data_csv(mock_data)
    results = pd.read_csv("demo_cards.csv")
    assert len(results) == 2


def test_dump_data_json():
    mock_data = [{"a": "a", "b": "b"}, {"a": "b", "b": "a"}]
    dump_data_json(mock_data)
    with open("./demo_cards.json") as file:
        results = json.load(file)
        assert len(results) == 2


def test_get_soup():
    mock_soup_success = get_soup(
        "https://www.sportscardchecklist.com/sport-baseball/vintage-and-new-release-trading-card-checklists"
    )
    mock_soup_failure = get_soup("notalink")
    assert type(mock_soup_success) == type(BeautifulSoup('<b class="boldest">Extremely bold</b>', "lxml"))
    assert len(mock_soup_failure.find_all("a")) == 0


def test_filter_href():
    mock_soup = get_soup(
        "https://www.sportscardchecklist.com/sport-baseball/vintage-and-new-release-trading-card-checklists"
    )
    mock_data = mock_soup.find_all("a")
    result = filter_hrefs(mock_data, "year-")
    assert len(result) > 0 and len(result) < len(mock_data)


def test_integration_grab_and_dump():
    card_list = grab_card_list(grab_year_links(["1950"]))
    expected_length = len(card_list)
    dump_data_csv(card_list)
    results = pd.read_csv("demo_cards.csv")
    assert len(results) == expected_length


def test_ebay_image_capture():
    ET = EbayTool()
    href = ET.parse_ebay_listing(
        "https://www.ebay.com/itm/144732185425?_trkparms=amclksrc%3DITM%26aid%3D777008%26algo%3DPERSONAL.TOPIC%26ao%3D1%26asc%3D20220705100511%26meid%3Dbd9c2ebabd08470cb87f50fa3cfa3759%26pid%3D101524%26rk%3D1%26rkt%3D1%26itm%3D144732185425%26pmt%3D0%26noa%3D1%26pg%3D2380057%26algv%3DRecentlyViewedItemsV2&_trksid=p2380057.c101524.m146925&_trkparms=pageci%3A7921ce0a-de28-11ed-a017-9e22be3a317f%7Cparentrq%3A9613cda81870ac0fbd638439ffff78f6%7Ciid%3A1"
    )
    assert href


def test_imgur_upload():
    ET = EbayTool(environ["IMGUR_SECRET"])
    href = ET.imgur_upload("https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Sheba1.JPG/800px-Sheba1.JPG")
    assert href
