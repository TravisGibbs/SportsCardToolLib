from SportsCardTool import (
    grab_card_list,
    dump_data,
    get_soup,
    filter_hrefs,
    grab_year_links,
    QueryBuilder,
    process_group_links,
    process_set_links,
    grab_debut_dict,
    remove_accents,
)
from bs4 import BeautifulSoup
import pandas as pd


def test_grab_debut_dict():
    years = ["1939"]
    d = grab_debut_dict(years)
    assert len(d) == 2
    assert len(d['players']) > 10
    assert "Ted Williams" in d['players']


def test_remove_accents():
    assert remove_accents("Edwin Díaz") == "Edwin Diaz"
    assert remove_accents("Rafael Devers") == "Rafael Devers"


def test_query_builder():
    qb = QueryBuilder()
    qb.add_item({"name": "Barry Bonds"})
    data = qb.grab_data()
    assert len(data[0]) >= 1000
    assert data[1] >= 1000


def test_grab_year_links():
    assert len(grab_year_links(["2023"])) == 1
    assert len(grab_year_links(["2023", "2022"])) == 2


def test_process_set_links():
    cards = process_set_links(
        ["https://www.sportscardchecklist.com/set-138550/1990-topps-coins-baseball-card-checklist"], "1990"
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


def test_dump_date():
    mock_data = [{"a": "a", "b": "b"}, {"a": "b", "b": "a"}]
    dump_data(mock_data)
    results = pd.read_csv('demo_cards.csv')
    assert len(results) == 2


def test_get_soup():
    mock_soup_success = get_soup(
        "https://www.sportscardchecklist.com/sport-baseball/vintage-and-new-release-trading-card-checklists"
    )
    mock_soup_failure = get_soup("notalink")
    assert type(mock_soup_success) == type(BeautifulSoup('<b class="boldest">Extremely bold</b>', 'lxml'))
    assert len(mock_soup_failure.find_all('a')) == 0


def test_filter_href():
    mock_soup = get_soup(
        "https://www.sportscardchecklist.com/sport-baseball/vintage-and-new-release-trading-card-checklists"
    )
    mock_data = mock_soup.find_all('a')
    result = filter_hrefs(mock_data, "year-")
    assert len(result) > 0 and len(result) < len(mock_data)


def test_integration_grab_and_dump():
    card_list = grab_card_list(grab_year_links(["1950"]))
    expected_length = len(card_list)
    dump_data(card_list)
    results = pd.read_csv('demo_cards.csv')
    assert len(results) == expected_length
