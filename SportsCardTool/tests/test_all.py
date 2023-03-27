from SportsCardTool import grab_card_list, dump_data, get_soup, filter_hrefs, grab_year_links, grab_sales, QueryBuilder
from bs4 import BeautifulSoup
import pandas as pd


def test_query_builder():
    qb = QueryBuilder()
    qb.add_item({"name": "Barry Bonds"})
    data = qb.grab_data()
    assert len(data[0]) >= 1000
    assert data[1] >= 1000


def test_grab_year_links():
    assert len(grab_year_links(["2023"])) == 1
    assert len(grab_year_links(["2023", "2022"])) == 2


def test_grab_sales():
    assert len(grab_sales("2022 Mike Trout")) > 0


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
    mock_soup = get_soup(
        "https://www.sportscardchecklist.com/sport-baseball/vintage-and-new-release-trading-card-checklists"
    )
    assert type(mock_soup) == type(BeautifulSoup('<b class="boldest">Extremely bold</b>', 'lxml'))


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
