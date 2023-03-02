from .scraping_tool import filter_hrefs, get_soup, parse_panel, grab_card_list, dump_data

if __name__ == "__main__":
    dump_data(grab_card_list())
