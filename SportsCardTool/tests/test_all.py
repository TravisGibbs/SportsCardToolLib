from SportsCardTool import grab_card_list, dump_data, get_soup, filter_hrefs
from bs4 import BeautifulSoup
import pandas as pd


def test_grab_data():
    card_list = grab_card_list()
    assert type(card_list) == type(list())
    assert len(card_list) > 100
    assert type(card_list[0]) == type(dict())


def test_dump_date():
    mock_data = [{"a": "a", "b": "b"}, {"a": "b", "b": "a"}]
    dump_data(mock_data)
    results = pd.read_csv('demo_cards.csv')
    assert len(results) == 3


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


def integration_test_grab_and_dump():
    card_list = grab_card_list()
    expected_length = len(card_list) + 1
    dump_data(card_list)
    results = pd.read_csv('demo_cards.csv')
    assert len(results) == expected_length
